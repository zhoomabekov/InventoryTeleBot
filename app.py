import telebot
from config import TOKEN
from extensions import APIException
import csv
import os

bot = telebot.TeleBot(TOKEN)


# Load the CSV file
def load_data(file_path):
    data = []
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    print('Data read!')
    return data


# Lookup function
def lookup_values_list(data, key):
    matches = [row for row in data if key in row['Инвентарный номер']]
    return matches


def lookup_value(data, key):
    for row in data:
        if key in row['Инвентарный номер']:
            print(row['Инвентарный номер'], row['Основное средство'])
            return row


# Example usage
table_data = load_data('List.csv')


@bot.message_handler(func=lambda message: True)
def handle_message_2(message):
    user_message = message.text.upper()
    if len(user_message) <= 9:
        results = lookup_values_list(table_data, user_message)
        if results:
            reply_message = "\n".join([i['Инвентарный номер'] for i in results])
            print(reply_message)
        else:
            reply_message = 'Entry not found in the SEDS IT equipment list'
    else:
        reply_message = "The inventory number (or its part) should not be more than 9 symbols long"

    bot.reply_to(message, reply_message, parse_mode='Markdown')


# @bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_message = message.text.upper()
    if len(user_message) <= 9:
        result = lookup_value(table_data, user_message)
        if result:
            reply_message = f'''
Дата передачи: {result['Дата передачи']}

*{result['Инвентарный номер']}*
{result['Основное средство']}

{result['Местоположение']}

{result['Пользователь']}
{result['Должность']}

{result['Первоначальная стоимость']} KZT
Дата поступления: {result['Дата поступления']}

Примечание: {result['Примечание']}
'''
        else:
            reply_message = 'Entry not found in the SEDS IT equipment list'
    else:
        reply_message = "The inventory number (or its part) should not be more than 9 symbols long"

    bot.reply_to(message, reply_message, parse_mode='Markdown')


# Start the bot
bot.polling()
