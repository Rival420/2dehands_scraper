import requests
import re
import argparse
from bs4 import BeautifulSoup
from discord import SyncWebhook, Embed

parser = argparse.ArgumentParser(description='2dehands Scraper')
parser.add_argument('-v', '--verbose', action='store_true', help='verbosity')
parser.add_argument('--min-price', dest="min_price", type=float, help='minimum price')
parser.add_argument('--max-price', dest="max_price", type=float, help='maximum price')
args = parser.parse_args()

servers = ["Dell PowerEdge", "HP Proliant", "Lenovo ThinkServer", "IBM System"]
url = "https://www.2dehands.be/l/computers-en-software/servers"
discord_webhook_url = '<DISCORD WEBHOOK URL HERE>'
webhook = SyncWebhook.from_url(discord_webhook_url)

r = requests.get(url)
r.raise_for_status()
soup = BeautifulSoup(r.text, 'html.parser')

matches = []

for a in soup.find_all("a", class_="hz-Link hz-Link--block hz-Listing-coverLink"):
    img = a.find("img")
    if img:
        title = img.get("title")
        if title:
            for server_name in servers:
                if server_name.lower() in title.lower():
                    matches.append(title)

if len(matches) > 0:
    for match in matches:
        for a in soup.find_all("a", class_="hz-Link hz-Link--block hz-Listing-coverLink"):
            img = a.find("img")
            if img:
                title = img.get("title")
                price_string = a.find("span", class_="hz-Listing-price").text.strip().replace(".", "").replace(",", ".").replace("€", "").strip()
                if price_string not in ["Bieden", "Op aanvraag"]:
                    price = float(price_string)
                    if (not args.min_price or price >= args.min_price) and (not args.max_price or price <= args.max_price):
                        try:
                            link = "https://www.2dehands.be" + a["href"]
                        except KeyError:
                            link = "Link not found"

                        description = a.find("p", class_="hz-Listing-description").text.strip()
                        if title:
                            for server_name in servers:
                                if server_name.lower() in title.lower() and match == title:
                                    embed = Embed(title=title, description=f"{description}\n\nPrice: {price}\n\n[Link]({link})", color=0x00ff00)
                                    webhook.send(embed=embed)

else:
    if args.verbose:
        print("No servers were found.")
