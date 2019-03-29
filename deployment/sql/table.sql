CREATE TABLE IF NOT EXISTS `items` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`title`	TEXT,
	`site`	TEXT,
	`price`	REAL,
	`site_id`	INTEGER,
	`url`	TEXT,
	`image`	INTEGER,
	`create_date`	TEXT,
	`update_date`	TEXT
);