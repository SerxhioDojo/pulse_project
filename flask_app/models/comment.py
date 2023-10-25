from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash


class Comment:
    db_name = 'pulse_db'

    def __init__(self, db_data):
        self.id = db_data['id']
        self.comment = db_data['comment']
        self.user_id = db_data['user_id']
        self.post_id = db_data['post_id']
        self.created_at = db_data['created_at']

    # Create Comment
    @classmethod
    def create(cls, data):
        query = ("INSERT INTO comments (comment, user_id, post_id) VALUES (%(comment)s, "
                 "%(user_id)s, %(post_id)s);")
        return connectToMySQL(cls.db_name).query_db(query, data)

    # Get Comments In Post
    @classmethod
    def get_comments_by_post_id(cls, data):
        query = ("SELECT c.*, u.first_name, u.last_name FROM comments c INNER JOIN users u ON "
                 "c.user_id = u.id WHERE c.post_id = %(post_id)s")
        results = connectToMySQL(cls.db_name).query_db(query, data)
        comments = []
        if results:
            for comment in results:
                comments.append(comment)
            return comments
        return comments

    # Delete Comment
    @classmethod
    def delete_comment(cls, data):
        query = "DELETE FROM comments WHERE id = %(comment_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @staticmethod
    def validate_comment(comment):
        is_valid = True
        if len(comment['comment']) <= 0:
            flash('Comment should not be empty!', 'comment')
            is_valid = False
        return is_valid
