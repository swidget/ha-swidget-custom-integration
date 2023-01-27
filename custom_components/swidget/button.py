"""Support for Swidget button."""
from __future__ import annotations

import logging

from swidget.exceptions import SwidgetException
from swidget.swidgetdevice import SwidgetDevice

from homeassistant.components.button import ButtonEntity, ButtonEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .coordinator import SwidgetDataUpdateCoordinator
from .entity import CoordinatedSwidgetEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Swidget button based on a config entry."""

    coordinator: SwidgetDataUpdateCoordinator = hass.data[DOMAIN][config_entry.entry_id]

    async_add_entities([SwidgetIdentifyButton(coordinator.device, coordinator)])


class SwidgetIdentifyButton(CoordinatedSwidgetEntity, ButtonEntity):
    """Defines an Swidget identify button."""

    def __init__(
        self,
        device: SwidgetDevice,
        coordinator: SwidgetDataUpdateCoordinator,
    ) -> None:
        """Initialize the button entity."""
        super().__init__(device, coordinator)
        self.entity_description = ButtonEntityDescription(
            key="Blink",
            name="Blink",
            icon="mdi:flash",
            entity_category=EntityCategory.CONFIG,
        )
        self._attr_name = "Blink"
        self._attr_unique_id = f"{self.device}_{self.entity_description.key}"

    async def async_press(self) -> None:
        """Identify the device by making it blink."""
        try:
            await self.device.blink()
        except SwidgetException:
            _LOGGER.exception("An error occurred while identifying the Swidget device")
