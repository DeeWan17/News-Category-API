from flask import Flask, request
from telebot import TeleBot, types
from requests import post
from config import BOT_TOKEN, WEBHOOK_URL

MIN_CHAR_COUNT = 20

bot = TeleBot(token=BOT_TOKEN)
app = Flask(__name__)

# Handle the /start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, '''Hi! I'm the News Categorizer Bot.\n\nSend me a news headline and I will tell you what category such a news belongs to.
                     
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


@app.route(f'/bot/{BOT_TOKEN}', methods=['POST'])
def webhook():
    update = types.Update.de_json(request.stream.read().decode('utf-8'))
    bot.process_new_updates([update])
    return ''

if __name__ == '__main__':
    bot.remove_webhook()
    bot.set_webhook(url=f'{WEBHOOK_URL}/bot/{BOT_TOKEN}')
    app.run(host='0.0.0.0', port=80)
