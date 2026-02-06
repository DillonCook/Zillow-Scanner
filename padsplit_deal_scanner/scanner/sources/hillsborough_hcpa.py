from __future__ import annotations

import re
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple
from urllib.parse import urljoin

import requests
from dbfread import DBF

HCPA_DOWNLOADS_URL = "https://downloads.hcpafl.org/"
PARCEL_PATTERN = re.compile(r"parcel_(\d{2})_(\d{2})_(\d{4})\.zip", re.IGNORECASE)


def _http_session() -> requests.Session:
    session = requests.Session()
    session.trust_env = False
    return session


def _find_latest_parcel_zip(html: str) -> Tuple[str, datetime]:
    matches: Dict[str, datetime] = {}

    for match in re.finditer(r'href=["\']([^"\']+)["\']', html, re.IGNORECASE):
        href = match.group(1)
        file_name = Path(href).name
        date_match = PARCEL_PATTERN.search(file_name)
        if not date_match:
            continue

        month, day, year = map(int, date_match.groups())
        file_date = datetime(year=year, month=month, day=day)
        matches[href] = file_date

    if not matches:
        raise RuntimeError("No parcel_MM_DD_YYYY.zip file links found on HCPA download page.")

    latest_href = max(matches, key=matches.get)
    return latest_href, matches[latest_href]


def _download_file(session: requests.Session, url: str, target_path: Path) -> Path:
    with session.get(url, timeout=180, stream=True) as response:
        response.raise_for_status()
        with target_path.open("wb") as file_handle:
            for chunk in response.iter_content(chunk_size=1024 * 512):
                if chunk:
                    file_handle.write(chunk)
    return target_path


def _extract_zip(zip_path: Path, extract_dir: Path) -> Path:
    extract_dir.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, "r") as zf:
        zf.extractall(extract_dir)
    return extract_dir


def _find_dbf_file(root_dir: Path) -> Path:
    dbf_files = sorted(root_dir.rglob("*.dbf"))
    if not dbf_files:
        raise RuntimeError(f"No .dbf files found under extracted directory: {root_dir}")
    return dbf_files[0]


def fetch_hcpa_parcel_fields(data_root: Path) -> Tuple[List[str], Dict]:
    data_dir = data_root / "hcpa"
    data_dir.mkdir(parents=True, exist_ok=True)

    session = _http_session()
    page_response = session.get(HCPA_DOWNLOADS_URL, timeout=60)
    page_response.raise_for_status()

    latest_href, _ = _find_latest_parcel_zip(page_response.text)
    latest_url = urljoin(HCPA_DOWNLOADS_URL, latest_href)
    zip_name = Path(latest_href).name
    zip_path = data_dir / zip_name

    _download_file(session, latest_url, zip_path)

    extract_dir = data_dir / zip_path.stem
    _extract_zip(zip_path, extract_dir)

    dbf_path = _find_dbf_file(extract_dir)
    table = DBF(str(dbf_path), load=False)

    fields = list(table.field_names)[:50]
    sample_record = {}
    for row in table:
        sample_record = dict(row)
        break

    return fields, sample_record
