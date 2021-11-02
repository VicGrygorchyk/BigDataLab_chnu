"""Implementation of map function."""
from datetime import datetime
from typing import List, TypedDict


class ResultDict(TypedDict):
    campaign: str
    city: str
    country: str
    payment: str
    userid: str


class CityMappedDict(TypedDict):
    city: dict


def map_data(data: List[ResultDict]) -> List[CityMappedDict]:
    """Gets data from DB and maps it by cities.
    :return List[Dict[campaign: campaign, payment: payment]]
    """
    return data


def map_to_worker(data):
    return data