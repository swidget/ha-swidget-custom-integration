from .device import (
    DeviceType,
    SwidgetDevice
)
from 


class SwidgetDimmer(SwidgetDevice):

    def __init__(self, host,  secret_key: str, ssl: bool) -> None:
        super().__init__(host=host, secret_key=secret_key, ssl=ssl)
        self._device_type = DeviceType.Dimmer

    @property  # type: ignore
    def brightness(self) -> int:
        """Return current brightness on dimmers.

        Will return a range between 0 - 100.
        """
        if not self.is_dimmable:
            raise SwidgetException("Device is not dimmable.")

        sys_info = self.sys_info
        return int(sys_info["brightness"])

    async def set_brightness(self, brightness):
        """Set the brightness of the device."""
        await self.send_command(
            assembly="host", component="0", function="level", command={"now": brightness}
        )

    @property  # type: ignore
    def is_on(self) -> bool:
        """Return whether device is on."""
        return True
