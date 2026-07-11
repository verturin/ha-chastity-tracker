"""Config flow for Chastity Tracker."""
from __future__ import annotations

import logging
from typing import Any

import async_timeout
import voluptuous as vol
from aiohttp import ClientError

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import API_PATH, CONF_API_TOKEN, CONF_BASE_URL, DEFAULT_BASE_URL, DOMAIN

_LOGGER = logging.getLogger(__name__)

STEP_USER_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_BASE_URL, default=DEFAULT_BASE_URL): str,
        vol.Required(CONF_API_TOKEN): str,
    }
)


async def _validate(hass: HomeAssistant, base_url: str, token: str) -> dict[str, Any]:
    """Appelle l'API pour vérifier que l'URL et le token sont valides."""
    session = async_get_clientsession(hass)
    url = f"{base_url.rstrip('/')}{API_PATH}"
    async with async_timeout.timeout(15):
        resp = await session.get(url, params={"token": token})
        if resp.status in (401, 403):
            raise InvalidAuth
        resp.raise_for_status()
        return await resp.json()


class ChastityTrackerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow pour Chastity Tracker."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        errors: dict[str, str] = {}

        if user_input is not None:
            base_url = user_input[CONF_BASE_URL]
            token = user_input[CONF_API_TOKEN]

            await self.async_set_unique_id(f"{base_url}:{token}")
            self._abort_if_unique_id_configured()

            try:
                await _validate(self.hass, base_url, token)
            except InvalidAuth:
                errors["base"] = "invalid_auth"
            except ClientError:
                errors["base"] = "cannot_connect"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Erreur inattendue lors de la validation")
                errors["base"] = "unknown"
            else:
                return self.async_create_entry(
                    title="Cage et Chasteté",
                    data=user_input,
                )

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_SCHEMA, errors=errors
        )


class InvalidAuth(Exception):
    """Token API invalide."""
