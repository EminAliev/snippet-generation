import psycopg2
import os


class DbService:
    def __init__(self):
        self.connection = psycopg2.connect(dbname=os.environ.get('DATABASE_NAME'), 
                                           user=os.environ.get('DATABASE_USERNAME'), 
                                           password=os.environ.get('DATABASE_PASSWORD'), 
                                           host=os.environ.get('DATABASE_HOST'))
        self.cursor = self.connection.cursor()

    def insert_to_feeds(self, file_name=None, url=None):
        if file_name:
            title_name = file_name
        else:
            title_name = url
        sql_script = """INSERT INTO feeds (title) VALUES ('{title_name}');""".format(title_name=title_name)
        self.cursor.execute(sql_script)
        self.connection.commit()
        return

    def get_id_feed(self):
        sql_script = """select last_insert_rowid() from feeds"""
        self.cursor.execute(sql_script)
        return self.cursor.fetchone()

    def insert_snippets(self, title, snippet, feed_id):
        sql_script = """INSERT INTO snippets_feeds (title,snippet,feed_id) 
                        VALUES ('{title_name}',
                        '{snippet_text}', '{feed_id}');""".format(title_name=title, snippet_text=snippet,
                                                                  feed_id=feed_id)
        self.cursor.execute(sql_script)
        self.connection.commit()
        return

    def select_feed(self, feed_id):
        sql_script = """SELECT TOP 1 * FROM feeds where id='{feed_id}'""".format(feed_id=feed_id)
        self.cursor.execute(sql_script)
        return self.cursor.fetchone()

    def get_all_feeds(self):
        sql_script = """select * from feeds"""
        self.cursor.execute(sql_script)
        return self.cursor.fetchall()

    def get_snippets_from_feed(self, feed_id):
        sql_script = """SELECT s.title, s.snippet FROM snippets_feeds as s join feeds as f on f.id=s.feed_id"""
        self.cursor.execute(sql_script)
        return self.cursor.fetchall()
