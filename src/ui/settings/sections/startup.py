import platform
import sys


WINDOWS_PLATFORM = "Windows"
MACOS_PLATFORM = "Darwin"
LINUX_PLATFORM = "Linux"
REGISTRY_PATH = r"Software\Microsoft\Windows\CurrentVersion\Run"
REGISTRY_VALUE_NAME = "JustTodoIt"


class StartupManager:
    """Registers the application to start when the user signs in."""

    def is_windows(self) -> bool:
        return platform.system() == WINDOWS_PLATFORM

    def is_supported(self) -> bool:
        return self.is_windows() and getattr(sys, "frozen", False)

    def enable(self) -> None:
        system = platform.system()

        if system == WINDOWS_PLATFORM:
            self._enable_windows()
        elif system == MACOS_PLATFORM:
            self._enable_macos()
        elif system == LINUX_PLATFORM:
            self._enable_linux()

    def disable(self) -> None:
        system = platform.system()

        if system == WINDOWS_PLATFORM:
            self._disable_windows()
        elif system == MACOS_PLATFORM:
            self._disable_macos()
        elif system == LINUX_PLATFORM:
            self._disable_linux()

    def _enable_windows(self) -> None:
        """Adds the packaged executable to the current user's startup registry key."""
        import winreg

        try:
            executable_path = f'"{sys.executable}"'
            with winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                REGISTRY_PATH,
                0,
                winreg.KEY_SET_VALUE,
            ) as key:
                winreg.SetValueEx(
                    key, REGISTRY_VALUE_NAME, 0, winreg.REG_SZ, executable_path
                )
        except OSError as error:
            print(f"Error enabling boot startup: {error}")

    def _disable_windows(self) -> None:
        """Removes the application from the current user's startup registry key."""
        import winreg

        try:
            with winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                REGISTRY_PATH,
                0,
                winreg.KEY_SET_VALUE,
            ) as key:
                winreg.DeleteValue(key, REGISTRY_VALUE_NAME)
        except OSError as error:
            print(f"Error disabling boot startup: {error}")

    def _enable_macos(self) -> None:
        print("macOS boot startup not yet implemented")

    def _disable_macos(self) -> None:
        print("macOS boot startup not yet implemented")

    def _enable_linux(self) -> None:
        print("Linux boot startup not yet implemented")

    def _disable_linux(self) -> None:
        print("Linux boot startup not yet implemented")
