"""API interaction module for Artemis RGB.

This module provides functions for interacting with Artemis RGB API endpoints.
"""

import logging
from typing import Any
from aiohttp import ClientError, ClientSession

from .config import ArtemisConfig
from .exceptions import ArtemisCannotConnectError

_LOGGER = logging.getLogger(__name__)


class Artemis:
    """Class for interacting with Artemis RGB API."""

    def __init__(self, config: ArtemisConfig):
        """Initialize the Artemis API client."""
        self.config = config

    async def _fetch(self, path: str) -> dict[Any]:
        url = f"http://{self.config.ip}:{self.config.port}{path}"
        _LOGGER.debug(f"Fetching {url}")
        try:
            async with ClientSession() as session:
                async with session.get(url) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        raise ArtemisCannotConnectError(
                            f"Server returned status {response.status}: {error_text}"
                        )

                    if "application/json" not in response.headers.get("Content-Type", ""):
                        raise ArtemisCannotConnectError(
                            "Expected JSON response but got different content type"
                        )

                    return await response.json()

        except ClientError as exc:
            raise ArtemisCannotConnectError(f"Failed to fetch {url}") from exc

    async def _get_profiles(self) -> dict[Any]:
        """Fetch raw calendar data for given time period."""
        _LOGGER.info("Getting Artemis RGB profiles")

        endpoints_path = "/profiles"

        return await self._fetch(endpoints_path)
