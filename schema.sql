DROP TABLE IF EXISTS property;

CREATE TABLE property (
    id INTEGER PRIMARY KEY,
    price INTEGER NOT NULL,
    otherinfo TEXT NOT NULL
);