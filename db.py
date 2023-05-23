import sqlite3

conn = sqlite3.connect('cartfull.sqlite')
cursor = conn.cursor()

conn.execute("""CREATE TABLE IF NOT EXISTS users(
uID INTEGER not null,
accID TEXT not null,
shopLists BLOB,
PRIMARY KEY (uID));""")


def supermarket_params(supermarket_name):
    return f"""CREATE table if not exists {supermarket_name} (
        gID INTEGER not null,
        gProductName TEXT not null,
        gPrice INTEGER,
        gPPKG INTEGER,
        gStock integer not null,
        PRIMARY KEY (gID)
        );"""


conn.execute(supermarket_params('newWorld'))
conn.execute(supermarket_params('pakNSave'))
conn.commit()
