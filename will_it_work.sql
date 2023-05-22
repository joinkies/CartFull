CREATE TABLE IF NOT EXISTS users(
	uID INTEGER not null,
	shopLists BLOB,
	PRIMARY KEY (uID)
);

CREATE table if not exists newWorld (
	gID INTEGER not null,
	gPrice INTEGER,
	gPPKG INTEGER,
	gStock integer,
	PRIMARY KEY (gID)
);

CREATE table pakNSave like newWorld;
CREATE table countDown like newWorld;