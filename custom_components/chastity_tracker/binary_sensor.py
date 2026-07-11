"""Binary sensor platform for Chastity Tracker (état verrouillé)."""
from __future__ import annotations

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import ATTR_LOCKED, DOMAIN
from .coordinator import ChastityTrackerCoordinator


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Crée l'entité binary_sensor."""
    coordinator: ChastityTrackerCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([ChastityLockedBinarySensor(coordinator, entry)])


class ChastityLockedBinarySensor(
    CoordinatorEntity[ChastityTrackerCoordinator], BinarySensorEntity
):
    """True (« on ») = déverrouillé, False (« off ») = verrouillé.

    Convention BinarySensorDeviceClass.LOCK : ON = déverrouillé/ouvert.
    """

    _attr_has_entity_name = True
    _attr_device_class = BinarySensorDeviceClass.LOCK
    _attr_translation_key = "locked"
    _attr_name = "Cage"

    def __init__(
        self, coordinator: ChastityTrackerCoordinator, entry: ConfigEntry
    ) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_locked"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name="Cage et Chasteté",
            manufacturer="Verturin",
            model="Chastity Tracker",
            configuration_url=coordinator.base_url,
        )

    @property
    def is_on(self) -> bool | None:
        """ON = déverrouillé (locked: false dans l'API)."""
        if not self.coordinator.data:
            return None
        return not bool(self.coordinator.data.get(ATTR_LOCKED, False))

    @property
    def icon(self) -> str:
        return "mdi:lock" if not self.is_on else "mdi:lock-open-variant"
