# COVID-19 Reporter

Bot that reports whenever you want the COVID-19 status at your country. All the data is taken from [Worldometers](https://www.worldometers.info/coronavirus/).

## Basic config

1. Rename the `settings.example.ini` to `settings.ini`
2. Set your API keys for the service you want, Telegram, Mastodon or both.
3. Set your country in the `main.py` file, under the global variable `COUNTRY`, by default is Spain.
3. If you are using a VPS to host your bot, add a new cronjob like this:

        0 */2 * * * python3 /path/to/your/bot/folder/main.py

    This will run the bot every two hours, you can change this.
4. You can also set the bot to run into AWS Lambda or PythonAnywhere, but there is an SSL issue with the free accounts, so get a paid one.

## The bot in action

My version of this bot is running on my Mastodon instance and serves Mastodona and Telegram. You can see it here:

* [Mastodon](https://hispatodon.club/@covid19_spa)
* [Telegram](https://t.me/covid19_spa)

Updated every two hours!
