from flask import Flask, request
from telebot import TeleBot
from telebot import types
from requests import post
import auth_data

MIN_CHAR_COUNT = 20

bot = TeleBot(token=auth_data.BOT_TOKEN)
app = Flask(__name__)

# Handle the /start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id,
                     '''Hi! I'm the News Categorizer Bot.\n\nSend me a news headline and I will tell you what category such a news belongs to.
                     
I know 15 news categories:
- ACTIVISM & EQUALITY
- CRIME
- CULTURE
- ECONOMY
- ENTERTAINMENT
- FOOD & DRINK
- HEALTH
- LIFESTYLE
- MISCELLANEOUS
- POLITICS
- SCIENCE & TECH
- SPORTS
- STYLE & BEAUTY
- TRAVEL
- WORLD NEWS

Keep in mind that the news I've been trained on were written in the US from 2012 to 2022. I may misinterpret cultural differences and have limited world knowledge. Beware that no AI is 100 percent accurate.
                     
I've been trained on this dataset of over 200,000 real news articles: https://www.kaggle.com/datasets/rmisra/news-category-dataset''')


# Handle incoming messages
@bot.message_handler(content_types=["text"])
def send_text(message):
    text = message.text.replace("\n", " ")

    if len(text) > MIN_CHAR_COUNT:
        category = get_predicted_category(text)
        bot.send_message(message.chat.id, f'Category: {category}')
    else:
        bot.send_message(
            message.chat.id, f'Headline must contain at least {MIN_CHAR_COUNT} characters in order to make a prediction.')


def get_predicted_category(headline):
    # Make API request
    response = post(url=f'https://news-category-app.azurewebsites.net/api/predict?headline={headline}')
    if response.status_code == 200:
        category = response.text
        return category
    else:
        return 'Error: Failed to call API. Please try again later.'


# Set up the webhook route
@app.route(f'/{auth_data.BOT_TOKEN}', methods=['POST'])
def handle_telegram_webhook():
    update = types.Update.de_json(request.stream.read().decode('utf-8'))
    bot.process_new_updates([update])
    return "OK"


if __name__ == '__main__':
    # Remove any existing webhook
    bot.remove_webhook()

    # Set the webhook URL
    bot.set_webhook(url=f'https://$news-category-webapp:lv7i5Cq89hrpYQyJ5d8M4eL1hNvag0cBP2yccpRrt4GTQTHcRdQsDCbmhQxg@news-category-webapp.scm.azurewebsites.net/api/registry/webhook')

    # Start the Flask app
    app.run(host='0.0.0.0', port=80)