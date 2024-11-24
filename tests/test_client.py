import os

import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from cebl.client import CEBLClient
from cebl.utils import build_url

from .test_data import create_specific_player_mock_response


@pytest.fixture
def api_client():
    api_key = os.getenv("CEBL_API_KEY")
    return CEBLClient(CEBL_API_KEY=api_key)


def test_build_url():
    endpoint_name = "games"
    year = 2024
    expected_url = f"https://api.data.cebl.ca/games/{year}"
    url = build_url(endpoint_name, year=year)
    assert url == expected_url


def test_get_games(api_client):
    year = 2024
    result = api_client.get_games(year)
    assert isinstance(result, pd.DataFrame)
    assert not result.empty
    assert "home_team_id" in result.columns
    assert "away_team_score" in result.columns
    assert "venue_name" in result.columns


def test_get_teams(api_client):
    year = 2024
    result = api_client.get_teams(year)
    assert isinstance(result, pd.DataFrame)
    assert not result.empty
    assert "id" in result.columns
    assert "short_name_en" in result.columns
    assert "name" in result.columns


def test_get_player_statistics(api_client):
    player_id = 1
    mode = "PER_GAME"
    career_only = False
    result = api_client.get_player_statistics(player_id, mode, career_only)
    assert isinstance(result, pd.DataFrame)
    assert not result.empty
    assert "id" in result.columns
    assert "points" in result.columns
    assert "rebounds" in result.columns
    assert "assists" in result.columns
    assert "target_scores" in result.columns


def test_get_player_statistics_aggregated(api_client):
    season = 2024
    mode = "PER_GAME"
    result = api_client.get_player_statistics_aggregated(season, mode)
    assert isinstance(result, pd.DataFrame)
    assert not result.empty
    assert "id" in result.columns
    assert "points" in result.columns
    assert "rebounds" in result.columns


def test_get_team_roster(api_client):
    team_short_name = "Calgary"
    year = 2024
    result = api_client.get_team_roster(team_short_name, year)
    assert isinstance(result, pd.DataFrame)
    assert not result.empty
    assert "id" in result.columns
    assert "full_name" in result.columns
    assert "position" in result.columns
    assert "jersey_number" in result.columns


def test_get_team_statistics_aggregated(api_client):
    season = 2024
    mode = "PER_GAME"
    result = api_client.get_team_statistics_aggregated(season, mode)
    assert isinstance(result, pd.DataFrame)
    assert not result.empty
    assert "id" in result.columns
    assert "points" in result.columns
    assert "fouls_drawn" in result.columns


def test_verify_player_statistics(api_client):
    real_data = create_specific_player_mock_response()
    player_id = 145
    mode = "TOTALS"
    competition = "REGULAR"
    result = api_client.get_player_statistics(player_id=player_id, mode=mode, competition=competition)

    assert isinstance(result, pd.DataFrame)
    assert not result.empty

    expected_df = pd.DataFrame(real_data)
    actual_df = result.head(1).reset_index(drop=True)

    assert_frame_equal(actual_df, expected_df, check_dtype=False)
