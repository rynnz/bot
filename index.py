import telebot
import time
from telebot import types
import sqlite3
import os
import re

#TELEGRAM API#
bot = telebot.TeleBot('1092114145:AAHRQ0p8-gcT9i8QOawYs6Uf7qK6qbdg8ug')
print("Бот успешно запущен!!")
adminuserid = 1092969024
#TELEGRAM API#

#COMMANDS#

@bot.message_handler(commands=['start'])
def start_message(message):
	if message.chat.id == message.from_user.id:
		userid = str(message.chat.id)
		username = str(message.from_user.username)
		connection = sqlite3.connect('db.sqlite')
		q = connection.cursor()
		q = q.execute('SELECT * FROM users WHERE (userid IS ? and num is ?)', (userid, 1))
		row = q.fetchone()
		if row is None:
			balance = 0
			noneusername = 'none'
			if message.from_user.username == None:
				q.execute("INSERT INTO users (userid, username, balance) VALUES ('%s', '%s', '%s')"%(userid, noneusername, balance))
				connection.commit()
			else:
				q.execute("INSERT INTO users (userid, username, balance) VALUES ('%s', '%s', '%s')"%(userid, username, balance))
				connection.commit()
			connection.close()
			bot.send_message(message.chat.id, "✌️ " + str(message.from_user.first_name) + ", благодарю за регистрацию в боте!", parse_mode='HTML')
		else:
			connection.close()
			def logincheck():
				connection = sqlite3.connect('db.sqlite')
				q = connection.cursor()
				q.execute('select username from users where (userid IS ? AND num IS ?)', (userid, 1))
				loginus = q.fetchone()[0]
				if loginus != message.from_user.username:
					if message.from_user.username == None:
						q.execute("update users set username = 'none' where (userid IS ? AND num IS ?)", (userid, 1))
						connection.commit()
						connection.close()
					else:
						q.execute("update users set username = '"+username+"' where (userid IS ? AND num IS ?)", (userid, 1))
						connection.commit()
						connection.close()
				else:
					connection.close()
			logincheck()
			bot.send_message(message.chat.id, "✌️ С возвращением, "+ str(message.from_user.first_name) +"!")

@bot.message_handler(commands=['status'])
def profile(message):
	if message.chat.id == message.from_user.id:
		userid = str(message.chat.id)
		username = str(message.from_user.username)
		connection = sqlite3.connect('db.sqlite')
		q = connection.cursor()
		q = q.execute('SELECT * FROM users WHERE (userid IS ? and num is ?)', (userid, 1))
		row = q.fetchone()
		connection.close()
		bot.send_message(message.chat.id, "💰 Balance: " + str(row[2]) + " $\n💬 ID: " +str(userid), parse_mode='HTML')

@bot.message_handler(commands=['new'])
def buy(message):
	if message.chat.id == message.from_user.id:
		userid = str(message.chat.id)
		username = str(message.from_user.username)
		connection = sqlite3.connect('db.sqlite')
		q = connection.cursor()
		q.execute('SELECT * FROM price WHERE num = 1')
		row = q.fetchone()
		q.execute('SELECT * FROM users WHERE (userid IS ? and num is ?)', (userid, 1))
		row2 = q.fetchone()
		connection.close()
		if int(row2[2]) < int(row[0]):
			bot.send_message(message.chat.id, "На вашем балансе недостаточно средств, нужно: " + str(row[0]) + " $")
		else:
			connection = sqlite3.connect('db.sqlite')
			q = connection.cursor()
			q.execute("update users set balance = balance - "+str(row[0])+" where userid =" + userid)
			connection.commit()
			connection.close()
			sentt = bot.send_message(message.chat.id, "Please wait: <b>30</b> s.", parse_mode='HTML')
			mid = sentt.message_id
			a = 30
			nn = 0
			for nn in range(30):
				a -= 1
				timerpay = str(a)
				bot.edit_message_text(chat_id=message.chat.id, message_id=mid, text="Please wait: <b>"+timerpay+"</b> s.", parse_mode='HTML')
				time.sleep(1)
			else:
				bot.delete_message(chat_id=message.chat.id, message_id=mid)
				os.system(userid) #команда cmd
				base = open(str(userid) + '.zip', 'rb')
				bot.send_document(message.chat.id, base)

@bot.message_handler(commands=['new_price'])
def pricenew(message):
	if message.chat.id == adminuserid:
		try:
			loginus = str(message.text)
			ytur = loginus
			partssr = ytur.rsplit(' ')
			paramo1 = partssr[1]
			connection = sqlite3.connect('db.sqlite')
			q = connection.cursor()
			q.execute("update price set pricee = "+str(paramo1)+" where num = 1")
			connection.commit()
			connection.close()
			bot.send_message(message.chat.id, "Цена успешно изменена!")
		except:
			bot.send_message(message.chat.id, '<b>Параметры указаны не корректно! (/new_price "сумма")</b>', parse_mode='HTML')

@bot.message_handler(commands=['add_balance'])
def upbal(message):
	if message.chat.id == adminuserid:
		try:
			loginus = str(message.text)
			ytur = loginus
			partssr = ytur.rsplit(' ')
			paramo1 = partssr[1]
			paramo2 = partssr[2]
			connection = sqlite3.connect('db.sqlite')
			q = connection.cursor()
			q.execute("update users set balance = balance + "+str(paramo2)+" where userid =" + str(paramo1))
			connection.commit()
			connection.close()
			bot.send_message(message.chat.id, "Баланс юзера успешно пополнен!")
		except:
			bot.send_message(message.chat.id, '<b>Параметры указаны не корректно! (/add_balance "ChatID" "Сумма")</b>', parse_mode='HTML')

@bot.message_handler(commands=['ban'])
def downbal(message):
	if message.chat.id == adminuserid:
		try:
			loginus = str(message.text)
			ytur = loginus
			partssr = ytur.rsplit(' ')
			paramo1 = partssr[1]
			connection = sqlite3.connect('db.sqlite')
			q = connection.cursor()
			q.execute("update users set balance = 0 where userid =" + str(paramo1))
			connection.commit()
			connection.close()
			bot.send_message(message.chat.id, "Баланс юзера успешно обнулен!")
		except:
			bot.send_message(message.chat.id, '<b>Параметры указаны не корректно! (/ban "ChatID")</b>', parse_mode='HTML')

@bot.message_handler(content_types=['text'])
def send_text(message):
	if message.chat.id == message.from_user.id:
		if int(message.chat.id) > 0:
			bot.send_message(message.chat.id, "Такой команды не существует! Воспользуйтесь списком команд")
	else:
		if message.text.lower() == 'привет':
			bot.send_message(message.chat.id, "Пока")

#COMMANDS#

bot.polling(none_stop=True, interval=0)