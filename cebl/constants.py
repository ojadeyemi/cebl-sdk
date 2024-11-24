from typing import Literal

YearType = Literal["2019", "2020", "2021", "2022", "2023", "2024", "2025"]

ModeType = Literal["PER_GAME", "TOTALS"]

PlayerStatisticsCompetitionType = Literal["REGULAR", "FINALS"]

AggregatedStatisticsCompetitionType = Literal["REGULAR", "PLAYOFFS"]

PlayerSegmentType = Literal["EAST", "WEST", "HOME", "AWAY"]

TeamSegmentType = Literal["HOME", "AWAY", "L7D", "L5G", "L10G", "May", "June", "July", "August"]
