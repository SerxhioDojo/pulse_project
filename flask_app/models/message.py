from flask_app.config.mysqlconnection import connectToMySQL
from datetime import datetime
import math


class Message:
    db_name = 'pulse_db'

    def __init__(self, db_data):
        self.id = db_data['id']
        self.sender_id = db_data['sender_id']
        self.receiver_id = db_data['receiver_id']
        self.content = db_data['content']
        self.created_at = db_data['created_at']

    def time_span(self):
        now = datetime.now()
        delta = now - self.created_at
        print(delta.days)
        print(delta.total_seconds())
        if delta.days > 0:
            return f"{delta.days} days ago"
        elif (math.floor(delta.total_seconds() / 60)) >= 60:
            return f"{math.floor(math.floor(delta.total_seconds() / 60) / 60)} hours ago"
        elif delta.total_seconds() >= 60:
            return f"{math.floor(delta.total_seconds() / 60)} minutes ago"
        else:
            return f"{math.floor(delta.total_seconds())} seconds ago"

    @classmethod
    def get_user_messages(cls, data):
        query = "SELECT users.first_name as sender, users2.first_name as receiver, messages.* FROM users LEFT JOIN messages ON users.id = messages.sender_id LEFT JOIN users as users2 ON users2.id = messages.receiver_id WHERE users2.id =  %(id)s"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        messages = []
        for message in results:
            messages.append(cls(message))
        return messages

    @classmethod
    def save(cls, data):
        query = ("INSERT INTO messages (content,sender_id,receiver_id) VALUES (%(content)s,"
                 "%(user_id)s, %(person_id)s);")
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def destroy(cls, data):
        query = "DELETE FROM messages WHERE messages.id = %(id)"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def inboxes(cls, data):
        query = ("SELECT m.* FROM "
                    "(SELECT  u2.first_name, u2.last_name, m.receiver_id as id, m.content, m.created_at "
                    "FROM messages m "
                    "INNER JOIN users u1 on u1.id = m.sender_id "
                    "INNER JOIN users u2 on u2.id = m.receiver_id "
                    "WHERE m.sender_id = %(user_id)s "
                    "UNION "
                    "SELECT u1.first_name, u1.last_name, m.sender_id as id, m.content, m.created_at "
                    "FROM messages m "
                    "INNER JOIN users u1 on u1.id = m.sender_id "
                    "INNER JOIN users u2 on u2.id = m.receiver_id "
                    "WHERE m.receiver_id = %(user_id)s ) m "
                "INNER JOIN "
                    "(Select id, max(max_timestamp) as max_timestamp from "
                        "(select m.receiver_id as id, MAX(m.created_at) as max_timestamp "
                        "from messages m "
                        "where m.sender_id = %(user_id)s "
                        "group by m.receiver_id "
                        "UNION "
                        "select m.sender_id as id, MAX(m.created_at) as max_timestamp "
                        "from messages m "
                        "where m.receiver_id = %(user_id)s "
                        "group by m.sender_id) t "
                    "group by id) t "
                "on m.id = t.id and m.created_at = t.max_timestamp "
                "ORDER BY m.created_at DESC;")
        results = connectToMySQL(cls.db_name).query_db(query, data)
        inboxes = []
        if results:
            for inbox in results:
                inboxes.append(inbox)
            return inboxes
        return inboxes


    @classmethod
    def get_messages_by_user(cls, data):
        query = ("SELECT  u1.first_name, u1.last_name, m.sender_id, m.content, m.created_at "
                 "FROM messages m "
                 "INNER JOIN users u1 on u1.id = m.sender_id "
                 "WHERE (m.sender_id = %(user_id)s and m.receiver_id = %(person_id)s ) "
                 "or (m.sender_id = %(person_id)s  and m.receiver_id = %(user_id)s ) "
                 "order by m.created_at;")
        results = connectToMySQL(cls.db_name).query_db(query, data)
        messages = []
        if results:
            for message in results:
                messages.append(message)
            return messages
        return messages
