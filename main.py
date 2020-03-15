import requests
from datetime import datetime as dt
from bs4 import BeautifulSoup
from mastodon import Mastodon

mastodon = Mastodon(
            access_token = 'YOUR API KEY HERE',
            api_base_url = 'https://hispatodon.club/'
        )

r = requests.get("https://www.worldometers.info/coronavirus/country/spain/")
soup = BeautifulSoup(r.text, 'html.parser')

covid_raw = soup.select("div.maincounter-number > span")

mastodon.status_post("""
Reporte del {} 
{}casos confirmados en España.
{} recuperados.
{} muertos.""".format(
    dt.now().strftime("%d/%m/%Y a las %H:%M:%S"),
    covid_raw[0].text,
    covid_raw[2].text,
    covid_raw[1].text,)
)
