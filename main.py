from recom_anime import data_prep, recomendation
import telebot

print("Bot starting....")

with open('key', 'r') as f:
    key = f.readline()
prep = data_prep.Preprocessing()
rec = recomendation.Recommend()
prep.load_csv('D:\\Begginer_projects\\Anime_bot\\Data\\anime.csv', "D:\\Begginer_projects\\Anime_bot\\Data\\anime_with_synopsis.csv")
prep.preprocess()
X = prep.get_X()
res = X['Clear name'][(X['Clear name'].str.find("tokyoghoul") != -1)]


bot = telebot.TeleBot(key)
print("Bot started")
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(commands=['help'])
def send_help(message):
    repl = """To get recommendations for your anime enter /recomm
    *Please*, enter your anime name only in english.
    *Example*: Death Note"""
    bot.reply_to(message, repl, parse_mode='Markdown')
@bot.message_handler(commands=['recomm'])
def get_recommendations(message):
    sent_msg = bot.send_message(message.chat.id, "Enter name of anime (only english anime names allowed):")

    bot.register_next_step_handler(sent_msg, print_recommendations)


def checkValidName(text):
    text = text.lower().replace(" ", "")
    res = X['Clear name'][(X['Clear name'].str.find(text) != -1)]
    if len(res[res.str.len() == len(text)].index) == 1:
        return True
    return False

def print_recommendations(message):
    if 'tokyo ghoul'  in message.text.lower():
        bot.reply_to(message, "This anime is not allowed here")
        bot.send_message(message.chat.id, '1000-7?')
        return
    bot.send_message(message.chat.id, "Picking best recommendations for you.....")
    mes = ""
    if not checkValidName(message.text):
        bot.reply_to(message, "Can't find exactly that anime.")
        check = X[(X['Clear name'].str.find(message.text.lower().replace(" ", "")) != -1)].sort_values(by='Score')["English name"]
        if len(check) != 0 :
            bot.send_message(message.chat.id, "Maybe you mean:")
            counter = 0
            out = ""
            for i in range(len(check)):
                if counter == 10:
                    break
                out += check[check.index[i]] + "\n"
                counter +=1
            bot.send_message(message.chat.id, out)
            bot.send_message(message.chat.id, "Try again please 🥺")
            return
        bot.send_message(message.chat.id, "Try again please 🥺")
        return
    res = rec.get_predictions(X, message.text)
    for i in range(1, len(res)):
        mes += f"{i } - {res[res.index[i]]}\n"
    bot.send_message(message.chat.id, f"Result for *{res[res.index[0]]}* :\n", parse_mode='Markdown')
    bot.send_message(message.chat.id, mes)

@bot.message_handler(content_types=['text'])
def send_warning(message):
    bot.reply_to(message, "Enter /recomm to search for new anime")

bot.polling()