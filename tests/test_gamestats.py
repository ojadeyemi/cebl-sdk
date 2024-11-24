import pytest

from cebl.gamestats import CEBLGameDataProvider


@pytest.fixture
def client():
    return CEBLGameDataProvider()


@pytest.fixture
def result(client: CEBLGameDataProvider):
    stats_url = "https://fibalivestats.dcd.shared.geniussports.com/u/CEBL/2400360/"
    return client.get_game_data(stats_url)


def test_basic_fields(result):
    assert isinstance(result, dict)
    # Basic fields
    assert result["clock"] == "00:00"
    assert result["period"] == 4
    assert result["periodLength"] == 10
    assert result["periodType"] == "REGULAR"
    assert result["inOT"] == 0


def test_team_details(result):
    # Team details
    assert "tm" in result

    team1 = result["tm"]["1"]
    team2 = result["tm"]["2"]

    assert team1["name"] == "Calgary Surge"
    assert team1["shortName"] == "Calgary"
    assert team2["name"] == "Edmonton Stingers"
    assert team2["shortName"] == "Edmonton"

    # Team codes and coach
    assert team1["code"] == "CGY"
    assert team1["coach"] == "T. Vernon"
    assert team2["code"] == "EDM"
    assert team2["coach"] == "J. Baker"
