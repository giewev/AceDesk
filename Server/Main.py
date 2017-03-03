from flask import Flask, request
import sqlite3
import json
app = Flask(__name__)
conn = sqlite3.connect('data.db')

c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users(
             NAME 				text (255)     	NOT NULL,
             USERNAME			text (255)		NOT NULL,
             PASSWORD			text (255)	NOT NULL,
			 CONTACT_INFO  		text (255))''')

c.execute('''CREATE TABLE IF NOT EXISTS topics(
             NAME 				text (255)     	NOT NULL)''')

c.execute('''CREATE TABLE IF NOT EXISTS topic_events(
             TOPIC_ID   		integer        	NOT NULL,
			 NAME 				text (255)		NOT NULL,
			 DESCRIPTION		text (255)		NOT NULL,
			 START_TIME			text (255)		NOT NULL)''')

c.execute('''CREATE TABLE IF NOT EXISTS user_interests(
             USER_ID   			integer        	NOT NULL,
			 TOPIC_ID 			integer     	NOT NULL)''')

c.execute('''CREATE TABLE IF NOT EXISTS friendships(
             VISIBLE_USER_ID 	integer        	NOT NULL,
			 ALLOWED_USER_ID 	integer     	NOT NULL)''')

c.execute('''CREATE TABLE IF NOT EXISTS user_events(
             EVENT_ID   		integer        	NOT NULL,
			 USER_ID 			integer    		NOT NULL)''')

@app.route("/hello")
def hello():
	return "Hello World";

def build_user_from_row(query_row, contact_visible):
	user = dict()
	user["name"] = query_row[0]
	user["username"] = query_row[1]
	if contact_visible:
		user["contact_info"] = query_row[3]

	add_metadata_to_user(user)
	return user

def add_metadata_to_user(user):
	user_interests = c.execute('''Select * from user_interests 
									left join users 
										on user_interests.USER_ID = users.ROWID
									left join topics
										on user_interests.TOPIC_ID = topics.ROWID
									where users.USERNAME = (?)''', 
									(user["username"],))
	user["interests"] = [x[6] for x in user_interests if x[6] != None]

	user_events = c.execute('''Select * from user_events 
								left join users 
									on user_events.USER_ID = users.ROWID
								left join topic_events
									on topic_events.ROWID = user_events.EVENT_ID
								where users.USERNAME = (?)''', 
								(user["username"],))
	user["events"] = [x[7] for x in user_events if x[7] != None]

	user_friendships = c.execute('''Select * from friendships 
								left join users as main_users
									on main_users.ROWID = friendships.ALLOWED_USER_ID
								left join users as visible_users
									on visible_users.ROWID = friendships.VISIBLE_USER_ID
								where visible_users.USERNAME = (?)''', 
								(user["username"],))
	user["friendships"] = [x[3] for x in user_friendships if x[3] != None]

def build_topic_from_row(query_row):
	topic = dict()
	topic["name"] = query_row[0]
	add_metadata_to_topic(topic)
	return topic

def add_metadata_to_topic(topic):
	user_interests = c.execute('''Select * from user_interests 
									left join users 
										on user_interests.USER_ID = users.ROWID
									left join topics
										on user_interests.TOPIC_ID = topics.ROWID
									where topics.NAME = (?)''', 
									(topic["name"],))
	topic["users"] = [x[3] for x in user_interests]

	topic_events = c.execute('''Select * from topic_events 
									left join topics
										on topic_events.TOPIC_ID = topics.ROWID
									where topics.NAME = (?)''', 
									(topic["name"],))
	topic["events"] = [x[1] for x in topic_events]

def build_event_from_row(query_row):
	event = dict()
	event["topic_id"] = query_row[0]
	event["name"] = query_row[1]
	event["description"] = query_row[2]
	event["start_time"] = query_row[3]
	add_metadata_to_event(event)
	return event

def add_metadata_to_event(event):
	topic_events = c.execute('''Select * from topic_events 
									left join topics
										on topic_events.TOPIC_ID = topics.ROWID
									where topic_events.NAME = (?)''', 
									(event["name"],))
	topic_events = list(topic_events)
	event["topic_name"] = topic_events[0][4]

@app.route("/users")
def get_users():
	users = [x for x in c.execute("SELECT * FROM users")]
	user_rows = [build_user_from_row(x, False) for x in users]
	return json.dumps(user_rows)

@app.route("/topics")
def get_topics():
	topics = [x for x in c.execute("SELECT * FROM topics")]
	topic_rows = [build_topic_from_row(x) for x in topics]
	return json.dumps(topic_rows)

@app.route("/events")
def get_events():
	events = [x for x in c.execute("SELECT * FROM topic_events")]
	event_rows = [build_event_from_row(x) for x in events]
	return json.dumps(event_rows)

def insert_test_data():
	test_users = [	('Ian Fade', 'giewev', "password", '444-444-4444'),
					('David Harupa', 'dave top', "abcdefg",'555-555-5555'),
					('Alex Lopez', 'alex', "admin123", '666-666-6666')]

	test_topics = [ ('Switch',),
					('Xbox',),
					('Hackathons',)]

	test_interests = [	(1,1),
						(1,2),
						(2,2)]

	test_events = [	(3, "Hofstra Hack Spring 2017", "Come hack with friends at Hofstra University", '2017-01-01 00:00:00'),
					(1, "Switch Release", "Gamestop and bestbuy will begin selling switches at midnight", '2017-03-02 23:59:59')]

	test_user_events = [	(1, 1),
							(2, 1),
							(3, 1),
							(2, 2)]

	test_friendships = [(1, 2),
						(1, 3),
						(2, 3)]

	c.executemany('INSERT INTO users VALUES (?,?,?,?)', test_users)
	c.executemany('INSERT INTO topics VALUES (?)', test_topics)
	c.executemany('INSERT INTO user_interests VALUES (?,?)', test_interests)
	c.executemany('INSERT INTO topic_events VALUES (?,?,?,?)', test_events)
	c.executemany('INSERT INTO user_events VALUES (?,?)', test_user_events)
	c.executemany('INSERT INTO friendships VALUES (?,?)', test_friendships)

if __name__ == "__main__":
	insert_test_data()
	app.run(host='0.0.0.0')
