import os
import platform
from pathlib import Path

class OSUtils:
    def __init__(self) -> None:
        pass

    def get_platform(self) -> str:
        return platform.system().lower()


    def get_sdk_path(self) -> Path:
        sdk_path =  os.environ.get('ANDROID_SDK_ROOT') or os.environ.get('ANDROID_SDK_HOME')
        if sdk_path is not None:
            return Path(sdk_path)
        else:
            raise NotADirectoryError

    def set_sdk_environment(self, sdk_path: Path) -> None:
        os.environ['ANDROID_SDK_ROOT'] = str(sdk_path)
        os.environ['ANDROID_SDK_HOME'] = str(sdk_path)

    def add_to_path(self, sdk_path: Path) -> None:
        cmdline_tools_path = sdk_path / 'cmdline-tools' / 'latest' / 'bin'
        platform_tools_path = sdk_path / 'platform-tools'
        current_path = os.environ.get('PATH', '')

        paths = current_path.split(os.pathsep)
        if str(cmdline_tools_path) not in paths:
            paths.insert(0, str(cmdline_tools_path))
        if str(platform_tools_path) not in paths:
            paths.insert(0, str(platform_tools_path))

        os.environ['PATH'] = os.pathsep.join(paths)
