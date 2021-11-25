from urllib.request import urlopen
import json
import sys
import re

BASE_URL = "https://artifacts.videolan.org/vlc/nightly-win64/"
MANIFEST = "bucket/vlc-nightly.json"


def latest_url():
    page = urlopen(BASE_URL).read().decode("utf-8")
    date = re.findall(r"(\d{8}-\d{4})/", page)[0]
    return BASE_URL + date


def read_manifest():
    with open(MANIFEST, "r") as f:
        return json.load(f)


def write_manifest(data):
    with open(MANIFEST, "w") as f:
        json.dump(data, f, indent=4)


def main():
    print("Fetching latest URL...")
    url = latest_url()
    print("Latest URL: " + url)

    data = read_manifest()
    if data["checkver"]["url"] == url:
        print("URL in manifest is already the latest. Exiting...")
        sys.exit(0)

    print("Writing new URL to manifest...")
    data["checkver"]["url"] = url
    write_manifest(data)

    print("Completed successfully")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
        sys.exit(1)
