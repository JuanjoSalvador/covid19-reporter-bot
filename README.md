# COVID-19 Reporter

Bot that reports whenever you want the COVID-19 status at your country. All the data is taken from [Worldometers](https://www.worldometers.info/coronavirus/).

## Running the bot on your VPS

### Prerequisites

* A VPS (the 5$ Digital Ocean tier will ne nice for this)
* Python 3 installed on your VPS
* For Mastodon, you will need:
    * A Mastodon account for your bot.
    * An API key for your bot. Check Mastodon's docs if you don't know how to do this part.
* For Telegram, you will need:
    * A Telegram bot account.
    * A Telegram's API key. Both can be obtained from Botfather.
    
### Install

1. Clone or download and unzip the repo.
1. Create a virtual environment for the bot (optional) and install the requirements with `pip`.

1. Rename the `settings.example.ini` to `settings.ini`

2. Set your API keys for the service you want, Telegram, Mastodon or both.

3. Set your country in the `main.py` file, under the global variable `COUNTRY`, by default is Spain.

3. To update the bot every 2 hours, add to your crontab something like this:

        0 */2 * * * python3 /path/to/your/bot/folder/main.py

## Other platforms

You can also run this bot on AWS Lambda, Heroku, PythonAnywhere, etc. Just choose your favourite.

## The bot in action

My version of this bot is running on my Mastodon instance and serves Mastodona and Telegram. You can see it here:

* [Mastodon](https://hispatodon.club/@covid19_spa)
* [Telegram](https://t.me/covid19_spa)

Updated every two hours!
