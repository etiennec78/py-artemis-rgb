"""API interaction module for Artemis RGB.

This module provides functions for interacting with Artemis RGB API endpoints.
"""

import logging
from typing import Any
from aiohttp import ClientError, ClientSession

from .config import ArtemisConfig
from .exceptions import ArtemisCannotConnectError
from .types import BoolString

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

                    if "application/json" not in response.headers.get(
                        "Content-Type", ""
                    ):
                        raise ArtemisCannotConnectError(
                            "Expected JSON response but got different content type"
                        )

                    return await response.json()

        except ClientError as exc:
            raise ArtemisCannotConnectError(f"Failed to fetch {url}") from exc

    async def _post(self, path: str, data: Any) -> None:
        url = f"http://{self.config.ip}:{self.config.port}{path}"
        _LOGGER.debug(f"Post sent to {url}")
        try:
            async with ClientSession() as session:
                kwargs = (
                    {"json": data} if isinstance(data, (list, dict)) else {"data": data}
                )
                async with session.post(url, **kwargs) as response:
                    response_text = await response.text()

                if response.status != 204:
                    raise ArtemisCannotConnectError(
                        f"Server returned status {response.status}: {response_text}"
                    )
                _LOGGER.debug(f"Got post response: {response_text}")

        except ClientError as exc:
            raise ArtemisCannotConnectError(f"Failed to push to {url}") from exc

    async def _get_profiles(self) -> dict[Any]:
        """Fetch Artemis profile data."""
        _LOGGER.info("Getting Artemis RGB profiles")

        profiles_path = "/profiles"

        return await self._fetch(profiles_path)

    async def _get_profile_categories(self) -> dict[Any]:
        """Fetch Artemis profile categories."""
        _LOGGER.info("Getting Artemis RGB profile categories")

        categories_path = "/profiles/categories"

        return await self._fetch(categories_path)

    async def _post_bring_to_foreground(self, route="") -> None:
        """Bring Artemis to the foreground, with an optional route to view."""
        _LOGGER.info(f"Bringing Artemis to the foreground with the route '{route}'")

        foreground_path = "/remote/bring-to-foreground"

        await self._post(foreground_path, route)

    async def _post_restart(self, args=[]) -> None:
        """Restart Artemis with optional command line arguments."""
        _LOGGER.info("Restarting Artemis")

        restart_path = "/remote/restart"

        await self._post(restart_path, args)

    async def _post_suspend_profile(
        self, profile_id: str, suspend_state: BoolString
    ) -> None:
        """Suspend or resume an Artemis profile."""
        _LOGGER.info(f"Changing profile {profile_id} suspend state to {suspend_state}")

        suspend_path = f"/profiles/suspend/{profile_id}"
        data = {
            "suspend": suspend_state,
        }

        await self._post(suspend_path, data)
