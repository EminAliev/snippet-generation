CREATE TABLE IF NOT EXIST feeds (
    id INT PRIMARY KEY,
    title varchar(500), 
    load_date DEFAULT (datetime('now','localtime')),
);


CREATE TABLE IF NOT EXIST snippets_feeds (
   id INT PRIMARY KEY,
   title text,
   load_date DEFAULT (datetime('now','localtime')),
   snippet text,
   FOREIGN KEY (feed_id) REFERENCES feeds(id)
);
