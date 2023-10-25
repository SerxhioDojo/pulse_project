from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash


class Post:
    db_name = 'pulse_db'

    def __init__(self, data):
        self.id = data['id']
        self.content = data['content']
        self.file = data['file']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    # Create Post
    @classmethod
    def save(cls, data):
        query = "INSERT INTO posts (content, file, user_id) VALUES (%(content)s, %(file)s, %(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    # Update Post
    @classmethod
    def update(cls, data):
        query = "UPDATE posts SET content = %(content)s WHERE posts.id = %(post_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    # Delete Post
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM posts WHERE posts.id = %(post_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    # Get All Posts
    @classmethod
    def get_all(cls, data):
        query = (
            "SELECT posts.id, posts.user_id, posts.file, posts.content, posts.created_at,"
            " u1.first_name, u1.last_name, COUNT(likes.post_id) as num_likes"
            " FROM posts"
            " LEFT JOIN users u1 ON posts.user_id = u1.id"
            " LEFT JOIN likes ON posts.id = likes.post_id"
            " INNER JOIN followers ON followers.follower_id = posts.user_id"
            " INNER JOIN users u2 ON u2.id = followers.user_id"
            " WHERE (u2.id = %(user_id)s OR u1.id = %(user_id)s)"
            " GROUP BY posts.id ORDER BY posts.created_at DESC;"
        )
        results = connectToMySQL(cls.db_name).query_db(query, data)
        posts = []
        if results:
            for post in results:
                posts.append(post)
            return posts
        return posts

    # Get Post By ID !!!!!!!!!!!!!!!!!!!!!
    @classmethod
    def get_post_by_id(cls, data):
        query = ("SELECT posts.id, posts.user_id, posts.file, posts.content, users.first_name, "
                 "users.last_name, COUNT(likes.post_id) as num_likes FROM posts  LEFT JOIN users "
                 "ON posts.user_id = users.id LEFT JOIN likes ON posts.id = likes.post_id "
                 "WHERE posts.id = %(post_id)s GROUP BY posts.id;")
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]
        return False

    # Get All User Posts !!!!!!!!!!!!!!!!!!!!!!!!1
    @ classmethod
    def get_all_user_posts(cls, data):
        query = """
       SELECT p.*, u.first_name, u.last_name
       FROM posts p
       LEFT JOIN users u ON p.user_id = u.id
       WHERE p.user_id = %(user_id)s
       GROUP BY p.id;"""
        results = connectToMySQL(cls.db_name).query_db(query, data)
        posts = []
        if results:
            for post in results:
                posts.append(post)
            return posts
        return posts

    # Get All User Posts !!!!!!!!!!!!!!!!!!!!!!!!1
    @classmethod
    def get_all_person_posts(cls, data):
        query = """
       SELECT p.*, u.first_name, u.last_name
       FROM posts p
       LEFT JOIN users u ON p.user_id = u.id
       WHERE p.user_id = %(person_id)s
       GROUP BY p.id;"""
        results = connectToMySQL(cls.db_name).query_db(query, data)
        posts = []
        if results:
            for post in results:
                posts.append(post)
            return posts
        return posts

    # Like Post
    @classmethod
    def like_post(cls, data):
        query = "INSERT INTO likes (post_id, user_id) VALUES (%(post_id)s, %(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    # Unlike Post
    @classmethod
    def unlike_post(cls, data):
        query = "DELETE FROM likes WHERE post_id = %(post_id)s and user_id = %(user_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    # Fave Post
    @classmethod
    def fave_post(cls, data):
        query = "INSERT INTO favorites (post_id, user_id) VALUES (%(post_id)s, %(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    # Unfave  Post
    @classmethod
    def unfave_post(cls, data):
        query = "DELETE FROM favorites WHERE post_id = %(post_id)s and user_id = %(user_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_post_likers(cls, data):
        query = "SELECT * from likes LEFT JOIN users on likes.user_id = users.id WHERE post_id = %(post_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        nrOfLikes = []
        if results:
            for row in results:
                nrOfLikes.append(row['email'])
            return nrOfLikes
        return nrOfLikes

    # NO of likes
    @classmethod
    def get_all_post_likes(cls, data):
        query = "SELECT COUNT(*) AS like_count FROM likes WHERE post_id = %(post_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]
        return 0

    # If User Liked The Post
    @classmethod
    def get_like_by_userid(cls, data):
        query = 'SELECT * FROM likes WHERE user_id = %(user_id)s AND tvshow_id = %(show_id)s'
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]
        return False

    # # If User Faved The Post
    @classmethod
    def get_fave_by_userid(cls, data):
        query = 'SELECT * FROM likes WHERE user_id = %(user_id)s AND tvshow_id = %(show_id)s'
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]
        return False

    @classmethod
    def user_liked_posts(cls, data):
        query = ("SELECT posts.id, posts.user_id, posts.file, posts.content, posts.created_at, "
                 "u1.first_name, u1.last_name, COUNT(likes.post_id) as num_likes "
                 "FROM posts "
                 "LEFT JOIN users u1 ON posts.user_id = u1.id "
                 "LEFT JOIN likes ON posts.id = likes.post_id "
                 "WHERE likes.user_id = %(user_id)s "
                 "GROUP BY posts.id order by posts.created_at desc")
        results = connectToMySQL(cls.db_name).query_db(query, data)
        posts = []
        if results:
            for post in results:
                posts.append(post)
            return posts
        return posts

    @classmethod
    def user_faved_posts(cls, data):
        query = ("SELECT posts.id, posts.user_id, posts.file, posts.content, posts.created_at, "
                 "u1.first_name, u1.last_name, COUNT(likes.post_id) as num_likes "
                 "FROM posts "
                 "LEFT JOIN users u1 ON posts.user_id = u1.id "
                 "LEFT JOIN likes ON posts.id = likes.post_id "
                 "Left join favorites on favorites.post_id = posts.id "
                 "WHERE favorites.user_id = %(user_id)s "
                 "GROUP BY posts.id order by posts.created_at desc")
        results = connectToMySQL(cls.db_name).query_db(query, data)
        posts = []
        if results:
            for post in results:
                posts.append(post)
            return posts
        return posts

    @staticmethod
    def validate_post(post):
        is_valid = True
        if len(post['content']) < 2:
            flash('Content should be more than 2 characters!', 'contentPost')
            is_valid = False
        return is_valid
