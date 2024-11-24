import logging
from typing import Optional, Tuple

import pandas as pd
from pandas import DataFrame

from .client import CEBLClient
from .constants import YearType
from .utils import make_request


class CEBLGameDataProvider:
    """
    A class to retrieve detailed game data from CEBL API based on stats_url_en.

    Attributes:
        headers (dict): HTTP headers to use for requests.
        data_url_base (str): Base URL for data endpoints.

    Methods:
        get_game_data(stats_url: str) -> Optional[dict]:
            Retrieves detailed game data JSON using stats_url_en.

        get_shot_data(stats_url: str) -> Tuple[DataFrame, DataFrame]:
            Extracts shot data from the game data JSON.

        get_team_shot_data(client: CEBLClient, year: int, team_name: str) -> DataFrame:
            Retrieves shot data for a specific team over a season.

        get_player_shot_data(client: CEBLClient, year: int, team_name: str, player_name: str) -> DataFrame:
            Retrieves shot data for a specific player over a season.
    """

    def __init__(self):
        self.headers = {
            "Accept": "application/json, text/plain, */*",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Sec-Ch-Ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
        }
        self.data_url_base = "https://fibalivestats.dcd.shared.geniussports.com/data"

    def get_game_data(self, stats_url: str) -> Optional[dict]:
        """
        Retrieves detailed game data JSON using stats_url_en.

        Args:
            stats_url (str): The stats_url_en from CEBL API which contains the game ID.

        Returns:
            Optional[dict]: The detailed game data JSON if successful, None otherwise.
        """
        try:
            # Extract game ID from stats_url_en
            game_id = stats_url.split("/")[-2]
            # Construct data URL for detailed game data
            data_url = f"{self.data_url_base}/{game_id}/data.json"

            # Make HTTP GET request to fetch game data
            game_data = make_request(data_url, self.headers)
            if not game_data:
                logging.error("Failed to fetch game data from URL: %s", data_url)
            return game_data

        except Exception as e:
            logging.error("Error fetching game data from URL %s: %s", data_url, e)
            return None

    def get_shot_data(self, stats_url: str) -> Tuple[DataFrame, DataFrame]:
        """
        Extracts shot data from the game data JSON.

        Args:
            stats_url (str): The stats_url_en from CEBL API which contains the game ID.

        Returns:
            Tuple[DataFrame, DataFrame]: DataFrames of shots for home and away teams.
        """
        game_data = self.get_game_data(stats_url)
        if not game_data:
            logging.error("Couldn't find game data for URL: %s", stats_url)
            return pd.DataFrame(), pd.DataFrame()

        try:
            team1_shots = pd.DataFrame(game_data["tm"]["1"]["shot"])
            team2_shots = pd.DataFrame(game_data["tm"]["2"]["shot"])

            if team1_shots.empty:
                logging.error("Home team shots DataFrame is empty for URL: %s", stats_url)
            if team2_shots.empty:
                logging.error("Away team shots DataFrame is empty for URL: %s", stats_url)

            return team1_shots, team2_shots

        except KeyError as e:
            logging.error("Error extracting shot data from game data: %s", e)
            return pd.DataFrame(), pd.DataFrame()

    def get_team_shot_data(self, client: CEBLClient, year: YearType, team_name: str) -> DataFrame:
        """
        Retrieves shot data for a specific team over a season.

        Args:
            client (CEBLClient): The API client to use for fetching games.
            year (int): The year of the season.
            team_name (str): The name of the team.

        Returns:
            DataFrame: DataFrame of all shots for the team over the season.
        """
        try:
            games = client.get_games(year, team_name)
            team_shots = []

            for _, game in games.iterrows():
                if game["status"] == "COMPLETE" and (
                    game["home_team_name"] == team_name or game["away_team_name"] == team_name
                ):
                    game_data = self.get_game_data(game["stats_url_en"])
                    if game_data:
                        home_shots, away_shots = self.get_shot_data(game["stats_url_en"])
                        if game["home_team_name"] == team_name:
                            team_shots.append(home_shots)
                        else:
                            team_shots.append(away_shots)

            if not team_shots:
                logging.error("No shot data found for team %s in year %d.", team_name, year)

            team_shots_df = pd.concat(team_shots, ignore_index=True) if team_shots else pd.DataFrame()

            if team_shots_df.empty:
                logging.error(
                    "Resulting DataFrame for team %s in year %d is empty.",
                    team_name,
                    year,
                )

            return team_shots_df

        except Exception as e:
            logging.error(
                "Error retrieving team shot data for team %s in year %d: %s",
                team_name,
                year,
                e,
            )
            return pd.DataFrame()

    def get_player_shot_data(self, client: CEBLClient, year: YearType, team_name: str, player_name: str) -> DataFrame:
        """
        Retrieves shot data for a specific player over a season.

        Args:
            client (CEBLClient): The API client to use for fetching games.
            year (int): The year of the season.
            team_name (str): The name of the team.
            player_name (str): The name of the player.

        Returns:
            DataFrame: DataFrame of all shots for the player over the season.
        """
        try:
            games = client.get_games(year, team_name)
            player_shots = []

            for _, game in games.iterrows():
                if game["status"] == "COMPLETE" and (
                    game["home_team_name"] == team_name or game["away_team_name"] == team_name
                ):
                    game_data = self.get_game_data(game["stats_url_en"])
                    if game_data:
                        home_shots, away_shots = self.get_shot_data(game["stats_url_en"])
                        shots = home_shots if game["home_team_name"] == team_name else away_shots
                        player_shots.append(shots[shots["player"] == player_name])

            if not player_shots:
                logging.error(
                    "No shot data found for player %s on team %s in year %d.",
                    player_name,
                    team_name,
                    year,
                )

            player_shots_df = pd.concat(player_shots, ignore_index=True) if player_shots else pd.DataFrame()

            if player_shots_df.empty:
                logging.error(
                    "Resulting DataFrame for player %s on team %s in year %d is empty.",
                    player_name,
                    team_name,
                    year,
                )

            return player_shots_df

        except Exception as e:
            logging.error(
                "Error retrieving player shot data for player %s on team %s in year %d: %s",
                player_name,
                team_name,
                year,
                e,
            )
            return pd.DataFrame()
