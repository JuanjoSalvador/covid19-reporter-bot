import configparser
import urllib3
import os
from datetime import datetime as dt
from bs4 import BeautifulSoup
from mastodon import Mastodon

# Initial config 
config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), 'settings.ini'))
http = urllib3.PoolManager()

# Get the data
r = http.request('GET', "https://www.worldometers.info/coronavirus/country/spain/")
soup = BeautifulSoup(r.text, 'html.parser')

covid_raw = soup.select("div.maincounter-number > span")

message = "Reporte del {} \n \
            {}casos confirmados en España.\n \
            {} recuperados.\n \
            {} muertos.".format(dt.now().strftime("%d/%m/%Y a las %H:%M:%S"),
            covid_raw[0].text, covid_raw[2].text, covid_raw[1].text)

if config['DEFAULT'].getboolean('MASTODON_ENABLED'):
    # Mastodon config
    mastodon = Mastodon(
                access_token = config['MASTODON']['ACCESS_TOKEN'],
                api_base_url = config['MASTODON']['API_BASE_URL']
            )

    mastodon.status_post(message)

if config['DEFAULT'].getboolean('TELEGRAM_ENABLED'):
    URL = "https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}".format(
        config['TELEGRAM']['API_KEY'], 
        config['TELEGRAM']['CHANNEL_NAME'], 
        message)

    try:
        http.request('GET', URL)
    except Exception as ex:
        print("Something went wrong: \n {}".format(ex))