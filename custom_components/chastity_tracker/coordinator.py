"""DataUpdateCoordinator for Chastity Tracker."""
from __future__ import annotations

import logging
from datetime import timedelta

import async_timeout
from aiohttp import ClientError

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import API_PATH, CONF_API_TOKEN, CONF_BASE_URL, DEFAULT_SCAN_INTERVAL, DOMAIN

_LOGGER = logging.getLogger(__name__)


class ChastityTrackerCoordinator(DataUpdateCoordinator):
    """Récupère périodiquement les données depuis l'API Chastity Tracker."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        self.hass = hass
        self.entry = entry
        self.base_url: str = entry.data[CONF_BASE_URL].rstrip("/")
        self.api_token: str = entry.data[CONF_API_TOKEN]

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL),
        )

    @property
    def api_url(self) -> str:
        return f"{self.base_url}{API_PATH}"

    async def _async_update_data(self) -> dict:
        session = async_get_clientsession(self.hass)
        try:
            async with async_timeout.timeout(15):
                resp = await session.get(
                    self.api_url, params={"token": self.api_token}
                )
                if resp.status in (401, 403):
                    raise ConfigEntryAuthFailed("Token API invalide ou révoqué")
                resp.raise_for_status()
                return await resp.json()
        except ConfigEntryAuthFailed:
            raise
        except (ClientError, TimeoutError) as err:
            raise UpdateFailed(f"Erreur de connexion à l'API Chastity Tracker : {err}") from err
