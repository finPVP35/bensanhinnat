import requests
import json
import re
from datetime import datetime

def get_prices():
    res = requests.get("https://polttoaine.net", headers={"User-Agent": "Mozilla/5.0"})
    res.encoding = "latin-1"
    html = res.text

    match = re.search(r'Eilisen keskihinnat[\s\S]*?<tr[^>]*>([\s\S]*?)<\/tr>', html)
    if not match:
        raise Exception("Eilisen keskihinnat -riviä ei löytynyt")

    row = match.group(1)
    prices = re.findall(r'<td[^>]*class="Hinnat"[^>]*>(.*?)<\/td>', row)

    if len(prices) < 3:
        raise Exception(f"Liian vähän hintoja: {len(prices)}")

    return {
        "95E10": prices[0].strip(),
        "98E5": prices[1].strip(),
        "Diesel": prices[2].strip()
    }

def main():
    prices = get_prices()
    data = {
        "paivitetty": datetime.utcnow().isoformat(),
        "lahde": "polttoaine.net",
        "eilisen_keskihinnat": prices
    }
    with open("data.json", "w") as f:
        json.dump(data, f, indent=2)
    print("Päivitetty:", data)

main()
