import logging
from typing import Optional

import pandas as pd

from .constants import (
    AggregatedStatisticsCompetitionType,
    ModeType,
    PlayerSegmentType,
    PlayerStatisticsCompetitionType,
    TeamSegmentType,
    YearType,
)
from .utils import build_url, make_request


class CEBLClient:
    """
    A client for interacting with the CEBL API.

    This client simplifies interactions with the CEBL API, allowing users to fetch basketball-related data such as games, teams, player statistics, and team statistics.

    Attributes:
        headers (dict): HTTP headers used for API requests, including the API key for authentication.

    Methods:
        get_games(year, team_name=None) -> pd.DataFrame:
            Fetch games for a given year, optionally filtered by team name.

        get_teams(year) -> pd.DataFrame:
            Fetch all teams for a given year.

        get_player_statistics(player_id, mode, career_only=False, competition=None) -> pd.DataFrame:
            Fetch statistics for a specific player.

        get_player_statistics_aggregated(season, mode='TOTALS', competition=None, segment=None, team_short_name=None) -> pd.DataFrame:
            Fetch aggregated player statistics for a season.

        get_team_roster(team_short_name, year) -> pd.DataFrame:
            Fetch the roster for a specific team in a given year.

        get_team_statistics_aggregated(season, mode, competition=None, segment=None) -> pd.DataFrame:
            Fetch aggregated team statistics for a season.

    Example:
    ```
        client = CEBLClient(CEBL_API_KEY="your-api-key")
        games = client.get_games(year="2023")
        print(games.head())
    ```

    Notes:
        - Errors during API requests are logged using the `logging` module.
        - Dependencies: Requires `pandas` and `requests` libraries.
    """

    def __init__(self, CEBL_API_KEY: str):
        """
        Initialize the CEBL API client.

        Args:
            CEBL_API_KEY (str): API key for authentication.
        """
        if not CEBL_API_KEY:
            raise ValueError("API key must be provided")

        self.headers = {
            "X-Api-Key": CEBL_API_KEY,
            "Accept": "application/json, text/plain, */*",
            "Origin": "https://cebl-stats-hub.web.app",
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                " AppleWebKit/537.36 (KHTML, like Gecko)"
                " Chrome/91.0.4472.124 Safari/537.36"
            ),
        }

    def get_games(self, year: YearType, team_name: Optional[str] = None) -> pd.DataFrame:
        """
        Retrieve games for a specific year, optionally filtered by team name.

        Args:
            year (YearType): The year to fetch games for.
            team_name (str, optional): The name of the team to filter by.

        Returns:
            pd.DataFrame: DataFrame of games for the specified year and optional team.
        """
        params: dict = {}
        if team_name:
            try:
                team_id = self.__get_team_id(team_name, year)
                params["team_id"] = team_id
            except ValueError as e:
                logging.error(f"Error retrieving team ID for {team_name}: {e}")

        endpoint = "games"
        url = build_url(endpoint, year=year)
        data = make_request(url, self.headers, endpoint_name=endpoint, params=params)
        df = pd.DataFrame(data) if data else pd.DataFrame()
        if df.empty:
            logging.error(f"No games data returned for year {year}.")
        return df

    def get_teams(self, year: YearType) -> pd.DataFrame:
        """
        Retrieve teams for a specific year.

        Args:
            year (YearType): The year to fetch teams for.

        Returns:
            pd.DataFrame: DataFrame of teams for the specified year.
        """
        endpoint = "teams"
        url = build_url(endpoint, year=year)
        data = make_request(url, self.headers, endpoint_name=endpoint)
        df = pd.DataFrame(data) if data else pd.DataFrame()
        if df.empty:
            logging.error(f"No teams data returned for year {year}.")
        return df

    def __get_team_id(self, team_name: str, year: YearType) -> int:
        """
        Retrieve the ID of a team based on its name or short name and year.

        Args:
            team_name (str): The name or short name of the team.
            year (YearType): The year to fetch the team ID for.

        Returns:
            int: The ID of the team.

        Raises:
            ValueError: If the team is not found for the specified year.
        """
        teams = self.get_teams(year)
        for _, team in teams.iterrows():
            if team["name_en"].lower() == team_name.lower() or team["short_name_en"].lower() == team_name.lower():
                return team["id"]

        raise ValueError(f"Team {team_name} not found for year {year}")

    def get_player_statistics(
        self,
        player_id: int,
        mode: ModeType,
        career_only: bool = False,
        competition: Optional[PlayerStatisticsCompetitionType] = None,
    ) -> pd.DataFrame:
        """
        Retrieve player statistics.

        Args:
            player_id (int): The ID of the player.
            mode (ModeType): The mode of statistics ('PER_GAME' or 'TOTALS').
            career_only (bool, optional): Whether to fetch career-only statistics. Defaults to False.
            competition (PlayerStatisticsCompetitionType, optional): Optional competition type.

        Returns:
            pd.DataFrame: DataFrame of player statistics.
        """
        params = {"mode": mode, "career_only": str(career_only).lower()}
        if competition:
            params["competition"] = competition

        endpoint = "player_statistics"
        url = build_url(endpoint, player_id=str(player_id))
        data = make_request(url, self.headers, endpoint_name=endpoint, params=params)
        df = pd.DataFrame(data) if data else pd.DataFrame()
        if df.empty:
            logging.error(
                f"No player statistics data returned for player ID {player_id} for competition: {competition}."
            )
        return df

    def get_player_statistics_aggregated(
        self,
        season: YearType,
        mode: ModeType = "TOTALS",
        competition: Optional[AggregatedStatisticsCompetitionType] = None,
        segment: Optional[PlayerSegmentType] = None,
        team_short_name: Optional[str] = None,
    ) -> pd.DataFrame:
        """
        Retrieve aggregated player statistics.

        Args:
            season (YearType): The season year.
            mode (ModeType, optional): The mode of statistics ('PER_GAME' or 'TOTALS'). Defaults to 'TOTALS'.
            competition (AggregatedStatisticsCompetitionType, optional): Optional competition type.
            segment (PlayerSegmentType, optional): Optional segment type.
            team_short_name (str, optional): Optional team short name.

        Returns:
            pd.DataFrame: DataFrame of aggregated player statistics.
        """
        params = {"season": season, "mode": mode}
        if competition:
            params["competition"] = competition
        if segment:
            params["segment"] = segment
        if team_short_name:
            team_id = self.__get_team_id(team_short_name, season)
            params["team_id"] = str(team_id)

        endpoint = "players_statistics_aggregated"
        url = build_url(endpoint)
        data = make_request(url, self.headers, endpoint_name=endpoint, params=params)
        df = pd.DataFrame(data) if data else pd.DataFrame()
        if df.empty:
            logging.error(f"No aggregated player statistics data returned for season {season}.")
        return df

    def get_team_roster(self, team_short_name: str, year: YearType) -> pd.DataFrame:
        """
        Retrieve the roster of a team for a specific year.

        Args:
            team_short_name (str): The short name of the team.
            year (YearType): The year to fetch the roster for.

        Returns:
            pd.DataFrame: DataFrame of the team roster.
        """
        team_id = self.__get_team_id(team_short_name, year)

        endpoint = "team_roster"
        url = build_url(endpoint, team_id=str(team_id), year=year)
        data = make_request(url, self.headers, endpoint_name=endpoint)
        df = pd.DataFrame(data) if data else pd.DataFrame()
        if df.empty:
            logging.error(f"No team roster data returned for team {team_short_name} and year {year}.")
        return df

    def get_team_statistics_aggregated(
        self,
        season: YearType,
        mode: ModeType,
        competition: Optional[AggregatedStatisticsCompetitionType] = None,
        segment: Optional[TeamSegmentType] = None,
    ) -> pd.DataFrame:
        """
        Retrieve aggregated team statistics.

        Args:
            season (YearType): The season year.
            mode (ModeType): The mode of statistics ('PER_GAME' or 'TOTALS').
            competition (AggregatedStatisticsCompetitionType, optional): Optional competition type.
            segment (TeamSegmentType, optional): Optional segment type.

        Returns:
            pd.DataFrame: DataFrame of aggregated team statistics.
        """
        params = {"season": season, "mode": mode}
        if competition:
            params["competition"] = competition
        if segment:
            params["segment"] = segment

        endpoint = "teams_statistics_aggregated"
        url = build_url(endpoint)
        data = make_request(url, self.headers, endpoint_name=endpoint, params=params)
        df = pd.DataFrame(data) if data else pd.DataFrame()
        if df.empty:
            logging.error(f"No aggregated team statistics data returned for season {season}.")
        return df
