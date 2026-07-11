"""Sensor platform for Chastity Tracker."""
from __future__ import annotations

from dataclasses import dataclass

from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    ATTR_DAYS_CURRENT,
    ATTR_DAYS_CURRENT_YEAR,
    ATTR_DAYS_SINCE_LAST,
    ATTR_STATUS,
    ATTR_TAGLINE,
    ATTR_TOTAL_DAYS,
    DOMAIN,
)
from .coordinator import ChastityTrackerCoordinator


@dataclass(frozen=True, kw_only=True)
class ChastitySensorDescription(SensorEntityDescription):
    """Description étendue avec la clé JSON source."""

    json_key: str = ""


SENSOR_TYPES: tuple[ChastitySensorDescription, ...] = (
    ChastitySensorDescription(
        key="status",
        json_key=ATTR_STATUS,
        translation_key="status",
        name="Statut",
        icon="mdi:lock-question",
    ),
    ChastitySensorDescription(
        key="days_current",
        json_key=ATTR_DAYS_CURRENT,
        translation_key="days_current",
        name="Jours en cours",
        icon="mdi:calendar-clock",
        native_unit_of_measurement="j",
    ),
    ChastitySensorDescription(
        key="days_since_last",
        json_key=ATTR_DAYS_SINCE_LAST,
        translation_key="days_since_last",
        name="Jours depuis la dernière période",
        icon="mdi:calendar-remove",
        native_unit_of_measurement="j",
    ),
    ChastitySensorDescription(
        key="total_days",
        json_key=ATTR_TOTAL_DAYS,
        translation_key="total_days",
        name="Total cumulé",
        icon="mdi:calendar-check",
        native_unit_of_measurement="j",
        state_class="total_increasing",
    ),
    ChastitySensorDescription(
        key="days_current_year",
        json_key=ATTR_DAYS_CURRENT_YEAR,
        translation_key="days_current_year",
        name="Jours cette année",
        icon="mdi:calendar-star",
        native_unit_of_measurement="j",
    ),
    ChastitySensorDescription(
        key="tagline",
        json_key=ATTR_TAGLINE,
        translation_key="tagline",
        name="Phrase personnalisée",
        icon="mdi:message-text",
        entity_registry_enabled_default=False,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Crée les entités sensor."""
    coordinator: ChastityTrackerCoordinator = hass.data[DOMAIN][entry.entry_id]

    entities = [
        ChastityTrackerSensor(coordinator, entry, description)
        for description in SENSOR_TYPES
        if description.json_key in (coordinator.data or {})
        or description.key != "tagline"
    ]
    async_add_entities(entities)


class ChastityTrackerSensor(CoordinatorEntity[ChastityTrackerCoordinator], SensorEntity):
    """Représente une valeur exposée par l'API Chastity Tracker."""

    entity_description: ChastitySensorDescription
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: ChastityTrackerCoordinator,
        entry: ConfigEntry,
        description: ChastitySensorDescription,
    ) -> None:
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{entry.entry_id}_{description.key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name="Cage et Chasteté",
            manufacturer="Verturin",
            model="Chastity Tracker",
            configuration_url=coordinator.base_url,
        )

    @property
    def native_value(self):
        if not self.coordinator.data:
            return None
        return self.coordinator.data.get(self.entity_description.json_key)
