import os
from pathlib import Path
import subprocess

class SdkManager:
    def __init__(self, sdk_path: str, platform: str):
        self.sdk_path = Path(sdk_path)

        match platform:
            case "Windows":
                # sdkmanager.bat is the real entrypoint on Windows
                self.manager_path = (
                    self.sdk_path
                    / "cmdline-tools"
                    / "latest"
                    / "bin"
                    / "sdkmanager.bat"
                )

            case "Linux" | "Darwin":
                # macOS reports as "Darwin"
                self.manager_path = (
                    self.sdk_path
                    / "cmdline-tools"
                    / "latest"
                    / "bin"
                    / "sdkmanager"
                )


    def query_packages(self):
        result = subprocess.run([str(self.manager_path), "--list"], capture_output= True).stdout.decode("utf-8")
        # print(f"Query Result {result}")

        installed, available, updates = self._parse_result(result=result)

        # print(f"Installed Packages: {installed}")
        # print(f"Available Packages: {available}")
        print(f"Available Updates: {updates}")


    def _parse_result(self, result: str):
        """Parse SDK manager output into three tuples of dicts.

        Returns:
            tuple: (installed, available, updates)
        """
        lines = result.split('\n')
        installed = []
        available = []
        updates = []

        mode = None
        i = 0
        n = len(lines)

        while i < n:
            line = lines[i]

            # Detect section changes
            if 'Installed packages:' in line:
                mode = 'installed'
                i += 2  # Skip header and separator
                continue
            elif 'Available Packages:' in line:
                mode = 'available'
                i += 2
                continue
            elif 'Available Updates:' in line:
                mode = 'updates'
                i += 2
                continue

            # Parse data lines
            if mode and '|' in line:
                parts = line.split('|')
                if len(parts) >= 3:
                    p0 = parts[0].strip()
                    p1 = parts[1].strip()
                    p2 = parts[2].strip()

                    # Skip header/separator rows
                    if not p0 or p0 in ('Path', 'ID', '-------'):
                        i += 1
                        continue

                    if mode == 'installed':
                        installed.append({
                            'path': p0,
                            'version': p1,
                            'desc': p2,
                            'location': parts[3].strip() if len(parts) > 3 else None
                        })
                    elif mode == 'available':
                        available.append({
                            'path': p0,
                            'version': p1,
                            'desc': p2,
                            'location': None
                        })
                    elif mode == 'updates':
                        updates.append({
                            'path': p0,  # ID column
                            'version': p1,  # Installed version
                            'desc': p2,  # Available version
                            'location': None
                        })

            i += 1

        return tuple(installed), tuple(available), tuple(updates)


if __name__ == "__main__":
    import platform
    import os
    sdk_path = os.environ.get("ANDROID_SDK_ROOT") or os.environ.get("ANDROID_SDK_HOME")
    if sdk_path != None:
        print(f"SDK Path: {sdk_path}")
        sdk = SdkManager(sdk_path= sdk_path, platform=platform.system())

        sdk.query_packages()
