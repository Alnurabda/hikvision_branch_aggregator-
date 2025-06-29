
import json
import requests
import pandas as pd
from requests.auth import HTTPDigestAuth
from datetime import datetime
from pathlib import Path

CONFIG_PATH = "branches_config.json"
OUTPUT_PATH = "camera_metadata_all_branches.csv"


def load_config(path):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def fetch_camera_metadata(ip, port, username, password):
    url = f"http://{ip}:{port}/ISAPI/Streaming/channels"
    try:
        response = requests.get(url, auth=HTTPDigestAuth(username, password), timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Could not retrieve data from {ip}: {e}")
        return None


def normalize_metadata(raw_data, branch_name):
    results = []
    channels = raw_data.get("StreamingChannelList", {}).get("StreamingChannel", [])

    for ch in channels:
        cam_id = ch.get("id", "unknown")
        name = ch.get("channelName", "Unnamed Camera").strip()
        enabled = ch.get("enabled", True)
        video = ch.get("video", {})
        codec = video.get("videoCodecType", "unknown")
        resolution = video.get("videoResolution", "unknown")

        # German to English translation if needed
        if name.lower().startswith("kamera"):
            name = name.replace("Kamera", "Camera")

        results.append({
            "Branch": branch_name,
            "CameraID": cam_id,
            "CameraName": name,
            "Enabled": enabled,
            "Codec": codec,
            "Resolution": resolution,
            "LastChecked": datetime.now().isoformat()
        })
    return results


def main():
    print("[INFO] Starting metadata aggregation...")
    if not Path(CONFIG_PATH).exists():
        print(f"[ERROR] Config file not found: {CONFIG_PATH}")
        return

    config = load_config(CONFIG_PATH)
    all_metadata = []

    for branch in config:
        print(f"[INFO] Connecting to {branch['branch']} ({branch['ip']})...")
        raw_data = fetch_camera_metadata(
            ip=branch['ip'],
            port=branch.get('port', 80),
            username=branch['username'],
            password=branch['password']
        )
        if raw_data:
            normalized = normalize_metadata(raw_data, branch['branch'])
            all_metadata.extend(normalized)

    if all_metadata:
        df = pd.DataFrame(all_metadata)
        df.to_csv(OUTPUT_PATH, index=False, encoding='utf-8-sig')
        print(f"[SUCCESS] Data aggregated and saved to {OUTPUT_PATH}")
    else:
        print("[WARN] No data collected from any branch.")


if __name__ == "__main__":
    main()
