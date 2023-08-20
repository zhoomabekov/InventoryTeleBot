import telebot
from telebot import types
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


# Example usage
table_data = load_data('List.csv')


@bot.message_handler(func=lambda message: True)
def handle_message_2(message):
    user_message = message.text.upper()
    if len(user_message) <= 9:
        results = lookup_values_list(table_data, user_message)
        if len(results) == 1:
            lookup_value(table_data, results[0]['Инвентарный номер'], message)
        elif len(results) > 10:
            bot.reply_to(message, 'Too many inv. numbers containing your input. Please provide more symbols...', parse_mode='Markdown')
        elif len(results) > 1:
            matching_inv_numbers = [i['Инвентарный номер'] for i in results]

            keyboard = types.InlineKeyboardMarkup(row_width=1)
            for i in matching_inv_numbers:
                button = types.InlineKeyboardButton(text=i, callback_data=i)
                keyboard.add(button)
            bot.send_message(message.chat.id, "Which one?", reply_markup=keyboard)

        else:
            bot.reply_to(message, 'Entry not found in the SEDS IT equipment list', parse_mode='Markdown')
    else:
        reply_message = "The inventory number (or its part) should not be more than 9 symbols long"
        bot.reply_to(message, reply_message, parse_mode='Markdown')


@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    lookup_value(table_data, call.data, call.message)


def lookup_value(data, key, message):
    for row in data:
        if key == row['Инвентарный номер']:
            reply_message = f'''
Дата передачи: {row['Дата передачи']}

*{row['Инвентарный номер']}*
{row['Основное средство']}
{row['Местоположение']}

{row['Пользователь']}
{row['Должность']}

{row['Первоначальная стоимость']} KZT
Дата поступления: {row['Дата поступления']}
Примечание: {row['Примечание']}

Актуальность данных: {row['АКТУАЛЬНОСТЬ']}
'''
            bot.send_message(message.chat.id, reply_message, parse_mode='Markdown')



bot.polling()
