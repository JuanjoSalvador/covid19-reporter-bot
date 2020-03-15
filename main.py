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

def get_data():
    r = requests.get("https://www.worldometers.info/coronavirus/")
    soup = BeautifulSoup(r.text, 'html.parser')

    rows = soup.find_all('tr')

    parsed_data = []

    for row in rows:
        cols = row.find_all('td')
        for col in cols:
            if col.text.strip() == COUNTRY.capitalize():
                country_data = row.find_all('td')
                for c_data in country_data:
                    parsed_data.append(c_data.text.lstrip().replace("+", ""))

    return parsed_data

def main():
    
    covid_data = get_data()

    message = "Informe del {} \n\n\
* {} casos confirmados en España ({} hoy).\n\
* {} recuperados.\n\
* {} muertos ({} hoy).\n\n\
Recuerda, es importante quedarse en casa, lavarse las manos \
con regularidad y en caso de síntomas, acudir al teléfono \
habilitado por las autoridades sanitarias de tu comunidad.".format(
        dt.now().strftime("%d/%m/%Y a las %H:%M:%S"),
        covid_data[1], covid_data[2], covid_data[5], covid_data[3], covid_data[4])

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