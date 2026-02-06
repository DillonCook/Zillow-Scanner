from typing import Dict, List


def fetch_on_market_demo(counties: List[str]) -> List[Dict]:
    county = counties[0] if counties else "Hillsborough_FL"
    return [
        {
            "listing_id": "ON-2001",
            "source": "on_market_demo",
            "lane": "on_market",
            "url": "https://demo.local/on/2001",
            "county": county,
            "price": 589000,
            "sqft": 2210,
            "baths": 3.0,
            "hoa": False,
            "cdd": True,
            "address": "789 Market Rd, Tampa, FL",
        },
        {
            "listing_id": "ON-2002",
            "source": "on_market_demo",
            "lane": "on_market",
            "url": "https://demo.local/on/2002",
            "county": county,
            "price": 640000,
            "sqft": 2000,
            "baths": 2.5,
            "hoa": False,
            "cdd": False,
            "address": "321 Listing Blvd, Tampa, FL",
        },
    ]
