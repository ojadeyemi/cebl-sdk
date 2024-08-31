# 🏀 CEBL SDK Client

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

The CEBL SDK Client allows you to interact with the CEBL API to retrieve various statistics and data related to the [Canadian Elite Basketball League (CEBL)](https://www.cebl.ca/). This SDK simplifies the process of fetching and utilizing CEBL data in your Python projects.

## Overview

The SDK provides functionalities for:

- Accessing team and player statistics.
- Retrieving game data and other relevant information
- Drawing a visual representation of a basketball court.

## Environment Variables

To run this project, you will need to add the following environment variables to your **.env** file

```bash
CEBL_API_KEY=<A_VALID_API_KEY>
```

## 📥 Installation

Install with pip

```bash
  pip install git+https://@github.com/ojadeyemi/cebl-sdk.git
```

## Classes Overview

### `CEBLClient`

The `CEBLClient` class helps you interact with the CEBL API to get various types of data.

**Methods:**

- `get_games(year, team_name=None)`: Get games for a specific year, with an optional team filter.
- `get_teams(year)`: Get teams for a specific year.
- `get_player_statistics(player_id, mode, career_only=False, competition=None)`: Get statistics for a specific player.
- `get_player_statistics_aggregated(season, mode='TOTALS', competition=None, segment=None, team_short_name=None)`: Get aggregated player statistics for a season.
- `get_team_roster(team_short_name, year)`: Get the roster for a specific team and year.
- `get_team_statistics_aggregated(season, mode, competition=None, segment=None)`: Get aggregated team statistics for a season.

### `CEBLGameDataProvider`

The `CEBLGameDataProvider` class helps you retrieve and process detailed game data from the CEBL API.

**Methods:**

- `get_game_data(stats_url)`: Get detailed game data using a stats URL.
- `get_shot_data(stats_url)`: Extract shot data from the game data.
- `get_team_shot_data(client, year, team_name)`: Get shot data for a specific team in a season.
- `get_player_shot_data(client, year, team_name, player_name)`: Get shot data for a specific player in a season.

### `draw_court`

The `draw_court` function draws a basketball court on a Matplotlib figure.

**Parameters:**

- `ax`: The Matplotlib axes to plot the court on. If `None`, uses the current axes.
- `color`: The color of the court lines.
- `lw`: The line width of the court lines.
- `outer_lines`: Whether to draw the outer lines (half-court line, baseline, side lines).

**Returns:**

- `ax`: The axes with the court drawn.

## Getting Started with the `cebl` Package

This guide will help you get started with using the `cebl` package, including drawing a basketball court and using the `CEBLClient` and `CEBLGameDataProvider` classes.

```python
import os
from dotenv import load_dotenv
import matplotlib.pyplot as plt
from cebl import CEBLClient, CEBLGameDataProvider, draw_court

# Load environment variables
load_dotenv()

# Retrieve the API key
CEBL_API_KEY = os.getenv('CEBL_API_KEY')
assert CEBL_API_KEY, "CEBL_API_KEY not found in environment variables"
```

### Using `CEBLClient` and `CEBLGameDataProvider`

```python
client = CEBLClient(CEBL_API_KEY=CEBL_API_KEY)
game_data_client = CEBLGameDataProvider()

# Get games schedule for Scarborough SHooting Stars in 2024
games = client.get_games(2024, "Scarborough Shooting Stars")

#get team shoots for Scarborough SHooting Stars in 2024
team_shots = game_data_client.get_team_shot_data(client, 2024, 'Scarborough Shooting Stars')
```

### Using `drawcourt` function

```python
# Draw the court
fig, ax = plt.subplots(figsize=(12, 11))
draw_court(ax=ax, outer_lines=True)

# Adjust plot limits to fit only half court
plt.xlim(-10, 510)
plt.ylim(510, -10)

plt.show()
```

## Author

This package was developed by OJ Adeyemi.

## Contributing

Contributions, bug reports, and feature requests are welcome! Please feel free to open an issue or submit a pull request on [GitHub](https://github.com/ojadeyemi/cebl-sdk).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
for details.

---

_The CEBL SDK is designed to be simple and user-friendly. I hope it helps you in your projects and data analysis._
