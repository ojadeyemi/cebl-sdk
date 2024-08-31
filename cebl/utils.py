import json
import logging
import os
from typing import Optional, TypedDict

import requests
from requests import Request, Session

# Configure logging to show info level messages
logging.basicConfig(level=logging.INFO)


class EndpointConfig(TypedDict):
    path: str
    params: dict[str, list[str]]


config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")

# Load configuration from config.json
with open(config_path, "r") as file:
    config = json.load(file)

BASE_URL: str = config["base_url"]
ENDPOINTS: dict[str, EndpointConfig] = config["endpoints"]


def build_url(
    endpoint_name: str,
    **kwargs: str,
) -> str:
    """
    Construct a URL from a base URL, endpoint configuration, and additional parameters.

    :param endpoint_name: The name of the endpoint to use.
    :param kwargs: Additional parameters to format the endpoint path.
    :return: The full URL as a string.
    :raises ValueError: If the endpoint name is not found.
    """
    endpoint = ENDPOINTS.get(endpoint_name)
    if not endpoint or not isinstance(endpoint, dict) or "path" not in endpoint:
        raise ValueError(f"Endpoint {endpoint_name} not found in configuration.")

    # Validate parameters
    if not validate_params(endpoint, kwargs):
        raise ValueError(f"Invalid parameters for endpoint: {endpoint_name}. Check logs for details.")

    path = endpoint["path"].format(**kwargs)
    return f"{BASE_URL}{path}"


def make_request(
    url: str,
    headers: dict[str, str],
    endpoint_name: Optional[str] = None,
    params: Optional[dict[str, str]] = None,
    timeout: int = 20,
) -> Optional[dict]:
    """
    Make an HTTP GET request and return the JSON response.

    :param url: The URL to send the request to.
    :param headers: Headers to include in the request.
    :param endpoint_name: The name of the endpoint to use for validation.
    :param params: Optional query parameters to include in the request.
    :param timeout: Timeout for the request in seconds (default is 20 seconds).
    :return: The JSON response if successful, otherwise None.
    """
    if endpoint_name:
        endpoint = ENDPOINTS.get(endpoint_name)
        if not endpoint:
            raise ValueError(f"Endpoint '{endpoint_name}' not found in configuration.")

        # Validate parameters
        if not validate_params(endpoint, params or {}):
            raise ValueError(f"Invalid parameters for endpoint: {endpoint_name}. Check logs for details.")

    try:
        response = requests.get(url, headers=headers, params=params, timeout=timeout)
        if response.status_code == 200:
            return response.json()
        else:
            logging.error(f"Request to {url} failed with status code {response.status_code}. Response: {response.text}")
            return None
    except requests.RequestException as e:
        logging.error(f"Request failed: {e}")
        return None


def print_request_headers(url: str, headers: dict[str, str]) -> None:
    """
    Print the headers of a prepared HTTP GET request.

    :param url: The URL for the request.
    :param headers: Headers to include in the request.
    """

    session = Session()
    req = Request("GET", url, headers=headers)
    prepared_req = session.prepare_request(req)

    logging.info("Request Headers:")
    for key, value in prepared_req.headers.items():
        logging.info(f"{key}: {value}")


def validate_params(endpoint_config: EndpointConfig, params: dict[str, list[str]]) -> bool:
    """
    Validates the parameters against the endpoint configuration, skipping specific keys.

    Args:
        endpoint_config (dict): The configuration of the endpoint.
        params (dict): The parameters to validate.

    Returns:
        bool: True if all parameters are valid, False otherwise.
    """
    valid_params: dict = endpoint_config.get("params", {})
    ignore_keys = {"team_id", "player_id"}

    all_valid = True

    for key, value in params.items():
        if key in ignore_keys:
            continue

        if key not in valid_params:
            logging.error(f"Parameter '{key}' is not valid for this endpoint.")
            all_valid = False
            continue

        # Check if the value is in the list of valid values for this key
        valid_values = valid_params.get(key, {})
        if valid_values and str(value) not in valid_values:
            logging.error(f"Value '{value}' for parameter '{key}' is not valid. Valid values are: {valid_values}.")
            all_valid = False

    return all_valid
