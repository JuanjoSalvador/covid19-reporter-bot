import configparser
import requests
import urllib3
import os
from datetime import datetime as dt
from bs4 import BeautifulSoup
from mastodon import Mastodon

# Initial config 
config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), 'settings.ini'))
urllib3.disable_warnings()

COUNTRY = "spain" # Change this!

def tg_send(message):
    URL = "https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}".format(
        config['TELEGRAM']['API_KEY'], 
        config['TELEGRAM']['CHANNEL_NAME'], 
        message)

    try:
        r = requests.get(URL)
    except Exception as ex:
        print("Something went wrong: \n {}".format(ex))

    return r.json()

def tg_delete(message_id):
    URL = "https://api.telegram.org/bot{}/deleteMessage?chat_id={}&message_id={}".format(
        config['TELEGRAM']['API_KEY'], 
        config['TELEGRAM']['CHANNEL_NAME'], 
        message_id)

    try:
        r = requests.get(URL)
    except Exception as ex:
        print("Something went wrong: \n {}".format(ex))

def main():
    # Get the data
    r = requests.get("https://www.worldometers.info/coronavirus/country/{}/".format(COUNTRY))
    soup = BeautifulSoup(r.text, 'html.parser')

    covid_raw = soup.select("div.maincounter-number > span")

    message = "Informe del {} \n\n\
    * {}casos confirmados en España.\n\
    * {} recuperados.\n\
    * {} muertos.\n\n\
    Recuerda, es importante quedarse en casa, lavarse las manos \
    con regularidad y en caso de síntomas, acudir al teléfono \
    habilitado por las autoridades sanitarias de tu comunidad.".format(
        dt.now().strftime("%d/%m/%Y a las %H:%M:%S"),
        covid_raw[0].text, covid_raw[2].text, covid_raw[1].text)

    if config['DEFAULT'].getboolean('MASTODON_ENABLED'):
        # Mastodon config
        mastodon = Mastodon(
                    access_token = config['MASTODON']['ACCESS_TOKEN'],
                    api_base_url = config['MASTODON']['API_BASE_URL']
                )

        mastodon.status_post(message)

    if config['DEFAULT'].getboolean('TELEGRAM_ENABLED'):
        response = tg_send(message)
        
        if response['ok']:
            try:
                message_log = open('message_id.log')
                last_message = message_log.read()
                tg_delete(last_message)
            except FileNotFoundError as err:
                pass
            
            log = open('message_id.log', 'w')
            log.write(str(response['result']['message_id']))
            log.close()

if __name__ == "__main__":
    main()
