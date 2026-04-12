"""Update entities for the Netgear Plus integration."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.update import UpdateDeviceClass, UpdateEntity
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import NetgearSwitchConfigEntry
from .netgear_switch import NetgearAPICoordinatorEntity

if TYPE_CHECKING:
    from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
    from .netgear_switch import HomeAssistantNetgearSwitch


class NetgearFirmwareUpdateEntity(NetgearAPICoordinatorEntity, UpdateEntity):
    """Represent firmware updates for a switch."""

    _attr_device_class = UpdateDeviceClass.FIRMWARE
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        switch: HomeAssistantNetgearSwitch,
    ) -> None:
        """Initialize the firmware update entity."""
        super().__init__(coordinator, switch)
        self._name = f"{switch.device_name} Firmware"
        self._unique_id = f"{switch.unique_id}-firmware"
        self.async_update_device()

    @callback
    def async_update_device(self) -> None:
        """Update entity state from coordinator data."""
        data = self.coordinator.data or {}
        self._attr_installed_version = data.get("installed_version")
        self._attr_latest_version = data.get("latest_version")
        self._attr_release_url = data.get("release_url")
        self._attr_release_summary = data.get("release_summary")
        self._attr_title = data.get("release_title")


async def async_setup_entry(
    hass: HomeAssistant,
    entry: NetgearSwitchConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the firmware update entity."""
    del hass
    async_add_entities(
        [
            NetgearFirmwareUpdateEntity(
                coordinator=entry.runtime_data.coordinator_firmware,
                switch=entry.runtime_data.gs_switch,
            )
        ]
    )
