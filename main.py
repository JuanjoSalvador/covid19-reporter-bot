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
#urllib3.disable_warnings()

COUNTRY = "spain" # Change this!

log_file = open(os.path.join(os.path.dirname(__file__), 'error.log'), 'a+')

def tg_send(message):
    url = "https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}".format(
        config['TELEGRAM']['API_KEY'], 
        config['TELEGRAM']['CHANNEL_NAME'], 
        message)

    try:
        r = requests.get(url)
    except Exception as ex:
        date = dt.now().strftime("%d/%m/%Y %H:%M:%S")
        log_file.write(f"[{date}] - Error while sending last message: {ex}\n")

    return r.json()

def tg_delete(message_id):
    URL = "https://api.telegram.org/bot{}/deleteMessage?chat_id={}&message_id={}".format(
        config['TELEGRAM']['API_KEY'], 
        config['TELEGRAM']['CHANNEL_NAME'], 
        message_id)

    try:
        r = requests.get(URL)
    except Exception as ex:
        date = dt.now().strftime("%d/%m/%Y %H:%M:%S")
        log_file.write(f"[{date}] - Error while deleting last message: {ex}\n")

def get_data():
    parsed_data = []

    try:
        r = requests.get("https://www.worldometers.info/coronavirus/")
    except Exception as ex:
        date = dt.now().strftime("%d/%m/%Y %H:%M:%S")
        log_file.write(f"[{date}] - Error while retrieving data: {ex}\n")

    if r.status_code == 200:
        soup = BeautifulSoup(r.text, 'html.parser')
        rows = soup.find_all('tr')

        for row in rows:
            cols = row.find_all('td')
            for col in cols:
                if col.text.strip() == COUNTRY.capitalize():
                    country_data = row.find_all('td')
                    for c_data in country_data:
                        n = c_data.text.strip()
                        n = n.replace("+", "")
                        n = n.replace(",", "")

                        parsed_data.append(n)
    
    return parsed_data

def main():

    try:
        covid_data = get_data()

        dead_percent = "%.2f" % (float(covid_data[4])/float(covid_data[2]) * 100)

        message = "Informe del {} \n\n\
* {} casos confirmados en España ({} casos reportados hoy).\n\
* {} muertos ({} muertes reportadas hoy).\n\n\
La tasa de mortalidad es un {}%\n\
Recuerda, es importante quedarse en casa, lavarse las manos \
con regularidad y en caso de síntomas, acudir al teléfono \
habilitado por las autoridades sanitarias de tu comunidad.".format(
        dt.now().strftime("%d/%m/%Y a las %H:%M:%S"),
        covid_data[2], covid_data[3] if covid_data[3] else "sin", 
        covid_data[4], covid_data[5] if covid_data[5] else "sin", dead_percent)

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
                if config['TELEGRAM'].getboolean('DELETE_LAST_MESSAGE'):
                    try:
                        message_log = open('message_id.log')
                        last_message = message_log.read()
                        tg_delete(last_message)
                        log = open('message_id.log', 'w')
                        log.write(str(response['result']['message_id']))
                        log.close()

                    except FileNotFoundError as err:
                        pass

    except Exception as ie:
        date = dt.now().strftime("%d/%m/%Y %H:%M:%S")
        log_file.write(f"[{date}] - An error ocurred: {ie}\n")

    log_file.close()

if __name__ == "__main__":
    main()
