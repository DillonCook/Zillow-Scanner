from typing import Dict, List


def fetch_off_market_demo(counties: List[str]) -> List[Dict]:
    county = counties[0] if counties else "Hillsborough_FL"
    return [
        {
            "listing_id": "OFF-1001",
            "source": "off_market_demo",
            "lane": "off_market",
            "url": "https://demo.local/off/1001",
            "county": county,
            "price": 410000,
            "sqft": 2450,
            "baths": 3.0,
            "hoa": False,
            "cdd": False,
            "address": "123 Demo St, Tampa, FL",
        },
        {
            "listing_id": "OFF-1002",
            "source": "off_market_demo",
            "lane": "off_market",
            "url": "https://demo.local/off/1002",
            "county": county,
            "price": 520000,
            "sqft": 1850,
            "baths": 2.0,
            "hoa": True,
            "cdd": False,
            "address": "456 Sample Ave, Tampa, FL",
        },
    ]
