# 2dehands_scraper
python script to scrape 2dehands.be for articles and send over to a discord webhook.

## manual adaptations:
- add your webhook to "discord_webhook_url" variable
- change servers = [] to the articles your looking for
- change url to your specific page on 2dehands.be you want to scrape

usage:
```python
python3 scraper.py --min-price 100 --max-price 1000
```
