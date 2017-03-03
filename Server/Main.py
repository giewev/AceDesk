from flask import Flask, request
import sqlite3
app = Flask(__name__)
conn = sqlite3.connect('data.db')

c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users(
             NAME 				text (255)     	NOT NULL,
			 CONTACT_INFO  		text (255))''')

c.execute('''CREATE TABLE IF NOT EXISTS topics(
             NAME 				text (255)     	NOT NULL)''')

c.execute('''CREATE TABLE IF NOT EXISTS user_interests(
             USER_ID   			integer        	NOT NULL,
			 TOPIC_ID 			text (255)     	NOT NULL)''')

c.execute('''CREATE TABLE IF NOT EXISTS friendships(
             VISIBLE_USER_ID 	integer        	NOT NULL,
			 ALLOWED_USER_ID 	text (255)     	NOT NULL)''')

c.execute('''CREATE TABLE IF NOT EXISTS topic_events(
             TOPIC_ID   		integer        	NOT NULL,
			 NAME 				text (255)		NOT NULL,
			 DESCRIPTION		text (255)		NOT NULL,
			 START_TIME			text (255)		NOT NULL)''')

c.execute('''CREATE TABLE IF NOT EXISTS user_events(
             EVENT_ID   		integer        	NOT NULL,
			 USER_ID 			integer    		NOT NULL)''')

@app.route("/hello")
def hello():
	return "Hello World";

@app.route("/users")
def get_users():
	users = c.execute("SELECT * FROM users")
	user_rows = [x for x in users]
	return str(user_rows)

def insert_test_data():
	test_users = [	('Ian Fade', '444-444-4444'),
					('David Harupa', '555-555-5555'),
					('Alex Lopez', '666-666-6666')]
	c.executemany('INSERT INTO users VALUES (?,?)', test_users)

if __name__ == "__main__":
	insert_test_data()
	app.run(host='0.0.0.0')
