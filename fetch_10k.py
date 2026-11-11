"""Fetch the latest 10-K filing for a company from SEC EDGAR.

Usage:
    python fetch_10k.py
"""
import time
from pathlib import Path

import requests

# The SEC requires a User-Agent that identifies you: "Full Name email@domain.com"
HEADERS = {"User-Agent": "Siddarth Sivasubramanian siddarthsivasubramanian@gmail.com"}
DATA_DIR = Path("data/raw")


def fetch(url: str, retries: int = 3) -> requests.Response:
    """GET a URL with simple retries and exponential backoff."""
    for attempt in range(1, retries + 1):
        resp = requests.get(url, headers=HEADERS, timeout=30)
        if resp.status_code == 200:
            return resp
        print(f"Attempt {attempt} failed (HTTP {resp.status_code}), retrying...")
        time.sleep(2 ** attempt)
    resp.raise_for_status()
    return resp


def latest_10k(cik: str) -> dict:
    """Return metadata for the company's most recent 10-K."""
    data = fetch(f"https://data.sec.gov/submissions/CIK{cik.zfill(10)}.json").json()
    recent = data["filings"]["recent"]
    for i, form in enumerate(recent["form"]):
        if form == "10-K":
            return {
                "company": data["name"],
                "accession": recent["accessionNumber"][i],
                "filing_date": recent["filingDate"][i],
                "document": recent["primaryDocument"][i],
            }
    raise ValueError(f"No 10-K found for CIK {cik}")


def download(cik: str, filing: dict) -> Path:
    """Download the 10-K document, skipping it if already saved."""
    accession = filing["accession"].replace("-", "")
    url = (
        f"https://www.sec.gov/Archives/edgar/data/"
        f"{int(cik)}/{accession}/{filing['document']}"
    )
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    out = DATA_DIR / f"{cik}_{filing['filing_date']}_10-K.htm"

    if out.exists():
        print(f"Already downloaded: {out}")
        return out

    time.sleep(0.2)  # stay well under the SEC limit of 10 requests/second
    out.write_text(fetch(url).text, encoding="utf-8")
    return out


if __name__ == "__main__":
    APPLE_CIK = "320193"
    filing = latest_10k(APPLE_CIK)
    print(f"{filing['company']}: latest 10-K filed {filing['filing_date']}")
    path = download(APPLE_CIK, filing)
    print(f"Saved to {path} ({path.stat().st_size / 1e6:.1f} MB)")
