import os
import platform


APP_NAME = "JustTodoIt"

WINDOWS_PLATFORM = "Windows"
LOCAL_APP_DATA_ENV_VAR = "LOCALAPPDATA"
WINDOWS_APP_DATA_DIRECTORY = "AppData"
WINDOWS_LOCAL_DATA_DIRECTORY = "Local"

MACOS_PLATFORM = "Darwin"
MACOS_LIBRARY_DIRECTORY = "Library"
MACOS_APP_SUPPORT_DIRECTORY = "Application Support"

XDG_DATA_HOME_ENV_VAR = "XDG_DATA_HOME"
LINUX_LOCAL_DIRECTORY = ".local"
LINUX_SHARE_DIRECTORY = "share"

HOME_DIRECTORY = "~"


def get_app_data_dir() -> str:
    """Return the platform-appropriate directory for user data."""
    system = platform.system()

    if system == WINDOWS_PLATFORM:
        base_dir = os.environ.get(LOCAL_APP_DATA_ENV_VAR)
        if not base_dir:
            base_dir = os.path.join(
                os.path.expanduser(HOME_DIRECTORY),
                WINDOWS_APP_DATA_DIRECTORY,
                WINDOWS_LOCAL_DATA_DIRECTORY,
            )
    elif system == MACOS_PLATFORM:
        base_dir = os.path.join(
            os.path.expanduser(HOME_DIRECTORY),
            MACOS_LIBRARY_DIRECTORY,
            MACOS_APP_SUPPORT_DIRECTORY,
        )
    else:
        base_dir = os.environ.get(XDG_DATA_HOME_ENV_VAR)
        if not base_dir:
            base_dir = os.path.join(
                os.path.expanduser(HOME_DIRECTORY),
                LINUX_LOCAL_DIRECTORY,
                LINUX_SHARE_DIRECTORY,
            )

    return os.path.join(base_dir, APP_NAME)


def get_data_file_path(filename: str) -> str:
    return os.path.join(get_app_data_dir(), filename)
