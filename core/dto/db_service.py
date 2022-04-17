import sqlite3

class DbService:
    def __init__(self):
        self.connection = sqlite3.connect(r'snippets.db')
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
                        '{snippet_text}', '{feed_id}');""".format(title_name=title, snippet_text=snippet, feed_id=feed_id)
        self.cursor.execute(sql_script)
        self.connection.commit()
        return

