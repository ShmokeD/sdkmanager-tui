from pathlib import Path
import requests
import zipfile
import io

class SdkDownloader:
    def __init__(self, platform: str):
        match platform:
            case "Windows":
                self.download_link = "https://dl.google.com/android/repository/commandlinetools-win-8512546_latest.zip"

            case "Linux":
                # macOS reports as "Darwin"
                self.download_link = "https://dl.google.com/android/repository/commandlinetools-linux-8512546_latest.zip"
            case "Darwin":
                self.download_link = "https://dl.google.com/android/repository/commandlinetools-mac-8512546_latest.zip"
            case _:
                raise ValueError(f"Unsupported platform: {platform}")


    def download_cmdline_tools(self, sdk_root: Path):

        extract_path = sdk_root / "cmdline-tools" / "latest"
        extract_path.mkdir(parents=True, exist_ok=True)

        print(f"Downloading command line tools from {self.download_link}...")
        response = requests.get(self.download_link)
        response.raise_for_status()

        print("Extracting command line tools...")
        with zipfile.ZipFile(io.BytesIO(response.content)) as z:
            z.extractall(extract_path)

        print(f"Command line tools downloaded and extracted to {extract_path}")
