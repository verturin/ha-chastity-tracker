"""Binary sensor platform for Chastity Tracker."""
from __future__ import annotations

from dataclasses import dataclass

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    ATTR_HAS_ACTIVE_CONTRACT,
    ATTR_HAS_ACTIVE_KH,
    ATTR_HIDE_STATUS,
    ATTR_IS_KEYHOLDER,
    ATTR_LOCKED,
    DOMAIN,
)
from .coordinator import ChastityTrackerCoordinator


@dataclass(frozen=True, kw_only=True)
class ChastityBinarySensorDescription(BinarySensorEntityDescription):
    """Description étendue avec la clé JSON source."""

    json_key: str = ""
    invert: bool = False  # True = on quand la valeur JSON est False


BINARY_SENSOR_TYPES: tuple[ChastityBinarySensorDescription, ...] = (
    ChastityBinarySensorDescription(
        key="locked",
        json_key=ATTR_LOCKED,
        translation_key="locked",
        name="Cage",
        device_class=BinarySensorDeviceClass.LOCK,
        invert=True,  # ON (device_class LOCK) = déverrouillé = locked:false
    ),
    ChastityBinarySensorDescription(
        key="is_keyholder",
        json_key=ATTR_IS_KEYHOLDER,
        translation_key="is_keyholder",
        name="Est Keyholder",
        icon="mdi:key-chain",
    ),
    ChastityBinarySensorDescription(
        key="has_active_kh",
        json_key=ATTR_HAS_ACTIVE_KH,
        translation_key="has_active_kh",
        name="A une KH active",
        icon="mdi:account-key",
    ),
    ChastityBinarySensorDescription(
        key="has_active_contract",
        json_key=ATTR_HAS_ACTIVE_CONTRACT,
        translation_key="has_active_contract",
        name="A un contrat actif",
        icon="mdi:file-document-check",
    ),
    ChastityBinarySensorDescription(
        key="hide_status",
        json_key=ATTR_HIDE_STATUS,
        translation_key="hide_status",
        name="Statut masqué",
        icon="mdi:eye-off",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Crée les entités binary_sensor."""
    coordinator: ChastityTrackerCoordinator = hass.data[DOMAIN][entry.entry_id]

    entities = [
        ChastityTrackerBinarySensor(coordinator, entry, description)
        for description in BINARY_SENSOR_TYPES
        if description.json_key in (coordinator.data or {})
        or description.entity_registry_enabled_default is not False
    ]
    async_add_entities(entities)


class ChastityTrackerBinarySensor(
    CoordinatorEntity[ChastityTrackerCoordinator], BinarySensorEntity
):
    """Représente un booléen exposé par l'API Chastity Tracker."""

    entity_description: ChastityBinarySensorDescription
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: ChastityTrackerCoordinator,
        entry: ConfigEntry,
        description: ChastityBinarySensorDescription,
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
    def is_on(self) -> bool | None:
        if not self.coordinator.data:
            return None
        value = bool(self.coordinator.data.get(self.entity_description.json_key, False))
        return (not value) if self.entity_description.invert else value

    @property
    def icon(self) -> str | None:
        if self.entity_description.key == "locked":
            return "mdi:lock-open-variant" if self.is_on else "mdi:lock"
        return self.entity_description.icon
