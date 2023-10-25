from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class User:
    db_name = 'pulse_db'

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.admin = data['admin']
        self.verificationCode = data['verificationCode']
        self.isVerified = data['isVerified']
        self.pic = data['pic']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    # CREATE User
    @classmethod
    def save(cls, data):
        query = ("INSERT INTO users (first_name, last_name, email, password, isVerified, "
                 "verificationCode, admin) VALUES ( %(first_name)s, %(last_name)s, %(email)s, "
                 "%(password)s, %(isVerified)s, %(verificationCode)s, 0);")
        return connectToMySQL(cls.db_name).query_db(query, data)

    # Get User By ID
    @classmethod
    def get_user_by_id(cls, data):
        query = "SELECT * FROM users WHERE users.id = %(user_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]
        return False

    @classmethod
    def get_person_by_id(cls, data):
        query = "SELECT * FROM users WHERE users.id = %(person_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]
        return False

    # Get User By ID
    @classmethod
    def get_account_by_id(cls, data):
        query = "SELECT * FROM users WHERE users.id = %(account_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]
        return False

    # Get User By Email
    @classmethod
    def get_user_by_email(cls, data):
        query = "SELECT * FROM users WHERE users.email = %(email)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]
        return False

    # Get All Users
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.db_name).query_db(query)
        users = []
        if results:
            for user in results:
                users.append(user)
            return users
        return users

    # Insert Verification Code
    @classmethod
    def updateVerificationCode(cls, data):
        query = "UPDATE users SET  verificationCode = %(verificationCode)s WHERE users.id = %(user_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    # Activate Account
    @classmethod
    def activateAccount(cls, data):
        query = "UPDATE users set isVerified = 1 WHERE users.id = %(user_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    # Update User !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    @classmethod
    def update(cls, data):
        query = ("UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s WHERE "
                 "users.id = %(user_id)s;")
        return connectToMySQL(cls.db_name).query_db(query, data)

    # DELETE User
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM users WHERE users.id = %(user_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    # Get User Liked Posts
    @classmethod
    def get_user_liked_posts(cls, data):
        query = "SELECT post_id as id from likes WHERE user_id = %(user_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        likedPosts = []
        if results:
            for row in results:
                likedPosts.append(row['id'])
            return likedPosts
        return likedPosts

    # Get User Fave Posts
    @classmethod
    def get_user_faved_posts(cls, data):
        query = "SELECT post_id as id from favorites WHERE user_id = %(user_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        favedPosts = []
        if results:
            for row in results:
                favedPosts.append(row['id'])
            return favedPosts
        return favedPosts

    # Follow
    @classmethod
    def follow(cls, data):
        query = "INSERT INTO followers (user_id, follower_id) VALUES (%(user_id)s, %(person_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    # Unfollow
    @classmethod
    def unfollow(cls, data):
        query = ("DELETE FROM followers WHERE user_id = %(user_id)s and follower_id = %("
                 "person_id)s;")
        return connectToMySQL(cls.db_name).query_db(query, data)

    # If User Liked The Post
    @classmethod
    def get_follow_by_userid(cls, data):
        query = ('SELECT * FROM followers WHERE user_id = %(user_id)s AND follower_id = %(person_id)s')
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]
        return False

    # Get Following
    @classmethod
    def get_followings(cls, data):
        query = ("SELECT f.user_id, f.follower_id, u1.first_name, u1.last_name, "
                 "u2.first_name as following_fname, u2.last_name as following_lname "
                 "FROM followers f LEFT JOIN users u1 ON f.user_id = u1.id "
                 "LEFT JOIN users u2 ON f.follower_id = u2.id "
                 "WHERE user_id = %(user_id)s")
        results = connectToMySQL(cls.db_name).query_db(query, data)
        followings = []
        if results:
            for following in results:
                followings.append(following)
            return followings
        return followings

    # Get followers
    @classmethod
    def get_followers(cls, data):
        query = ("SELECT f.user_id, f.follower_id, u1.first_name as follower_fname, u1.last_name as follower_lname,"
                 "u2.first_name, u2.last_name "
                 "FROM followers f LEFT JOIN users u1 ON f.user_id = u1.id "
                 "LEFT JOIN users u2 ON f.follower_id = u2.id "
                 "WHERE follower_id = %(user_id)s")
        results = connectToMySQL(cls.db_name).query_db(query, data)
        followers = []
        if results:
            for follower in results:
                followers.append(follower)
            return followers
        return followers
    
    @classmethod
    def get_followers_id(cls, data):
        query = ("SELECT follower_id FROM followers WHERE user_id = %(user_id)s")
        results = connectToMySQL(cls.db_name).query_db(query, data)
        followers = []
        if results:
            for follower in results:
                followers.append(follower['follower_id'])
            return followers
        return followers

    # Get user followings
    @classmethod
    def get_all_followings(cls, data):
        query = (
            "SELECT * FROM followers WHERE user_id = %(user_id)s")
        results = connectToMySQL(cls.db_name).query_db(query, data)
        followings = []
        if results:
            for following in results:
                followings.append(following)
            return followings
        return followings

    # Get Following User
    @classmethod
    def get_followings_user(cls, data):
        query = ("SELECT f.user_id, f.follower_id, u1.first_name, u1.last_name, "
                 "u2.first_name as following_fname, u2.last_name as following_lname "
                 "FROM followers f LEFT JOIN users u1 ON f.user_id = u1.id "
                 "LEFT JOIN users u2 ON f.follower_id = u2.id "
                 "WHERE user_id = %(person_id)s")
        results = connectToMySQL(cls.db_name).query_db(query, data)
        followings = []
        if results:
            for following in results:
                followings.append(following)
            return followings
        return followings

    # Get followers
    @classmethod
    def get_followers_user(cls, data):
        query = ("SELECT f.user_id, f.follower_id, u1.first_name, u1.last_name, u2.first_name, "
                 "u2.last_name FROM followers f LEFT JOIN users u1 ON f.user_id = u1.id LEFT JOIN "
                 "users "
                 "u2 ON f.follower_id = u2.id WHERE follower_id = %(person_id)s")
        results = connectToMySQL(cls.db_name).query_db(query, data)
        followers = []
        if results:
            for follower in results:
                followers.append(follower)
            return followers
        return followers

    @classmethod
    def get_notifications(cls, data):
        query = ("Select * from "
                    "(Select concat(u.first_name,' ', u.last_name, ' followed you.') as notification, "
                    "concat('/user/',u.id) as link, f.created_at "
                    "from followers f "
                    "inner join users u on f.user_id = u.id "
                    "where follower_id = %(user_id)s "
                    "UNION "
                    "Select concat(u.first_name,' ', u.last_name, ' liked your post.') as notification, "
                    "concat('/post/',p.id) as link, l.created_at "
                    "from likes l "
                    "inner join posts p on l.post_id = p.id "
                    "inner join users u on l.user_id = u.id "
                    "where p.user_id = %(user_id)s and l.user_id != %(user_id)s "
                    "UNION "
                    "Select concat(u.first_name,' ', u.last_name, ' commented on your post: ', c.comment,'.') as notification, "
                    "concat('/post/',p.id) as link, c.created_at "
                    "from comments c "
                    "inner join posts p on c.post_id = p.id "
                    "inner join users u on c.user_id = u.id "
                    "where p.user_id = %(user_id)s and c.user_id != %(user_id)s "
                    "UNION "
                    "SELECT m.* FROM "
                        "(SELECT CONCAT('You have a new message from ', u.first_name, ' ', u.last_name,'.') AS notification, "
                        "CONCAT('/messages/',m.sender_id) AS link, m.created_at "
                        "FROM messages m "
                        "INNER JOIN users u ON m.sender_id = u.id "
                        "WHERE m.receiver_id = %(user_id)s ) m "
                    "inner join "
                        "(Select CONCAT('/messages/',m.sender_id) AS link, max(m.created_at) as max_timestamp "
                        "FROM messages m "
                        "WHERE m.receiver_id = %(user_id)s  "
                        "GROUP BY CONCAT('/messages/',m.sender_id)) m1 "
                    "WHERE m.link = m1.link and m.created_at = m1.max_timestamp ) n "
                "order by n.created_at desc;")
        results = connectToMySQL(cls.db_name).query_db(query, data)
        notifications = []
        if results:
            for notification in results:
                notifications.append(notification)
            return notifications
        return notifications

    @staticmethod
    def validate_user(user):
        is_valid = True

        if len(user['first_name']) < 2:
            flash('First name should be more than 2 characters!', 'firstNameRegister')
            is_valid = False
        if len(user['last_name']) < 2:
            flash('Last name should be more than 2 characters!', 'lastNameRegister')
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address!", 'emailRegister')
            is_valid = False
        if len(user['password']) < 8:
            flash('Password should be more then 8 characters!', 'passwordRegister')
            is_valid = False
        if user['password'] != user['confirmPassword']:
            flash('Passwords do not match!', 'confirmPasswordRegister')
            is_valid = False
        return is_valid

    @staticmethod
    def validate_user_profile(user):
        valid = True

        if len(user['first_name']) < 2:
            flash('First name should be more than 2 characters!', 'firstNameRegister')
            is_valid = False
        if len(user['last_name']) < 2:
            flash('Last name should be more than 2 characters!', 'lastNameRegister')
            is_valid = False
        return valid


