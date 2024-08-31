"""
CEBL SDK Package

This package provides tools for interacting with the CEBL API, including:
- `CEBLClient`: For retrieving data from the CEBL API.
- `CEBLGameDataProvider`: For fetching and processing detailed game data.
- `draw_court`: For drawing a basketball court on a Matplotlib figure.

Usage:
- Import classes and functions from this package to work with CEBL data and visualizations.
"""

from .client import CEBLClient
from .court import draw_court
from .gamestats import CEBLGameDataProvider

__all__ = ["CEBLClient", "CEBLGameDataProvider", "draw_court"]
