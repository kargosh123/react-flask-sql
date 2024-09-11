DROP TABLE IF EXISTS items;
DROP TABLE IF EXISTS values_store;

CREATE TABLE items (
  id INTEGER PRIMARY KEY AUTOINCREMENT
);

CREATE TABLE values_store (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  value FLOAT NOT NULL,
  item_id INTEGER NOT NULL,
  FOREIGN KEY (item_id) REFERENCES items (id)
);

INSERT INTO items DEFAULT VALUES;
INSERT INTO items DEFAULT VALUES;
INSERT INTO values_store (value, item_id) VALUES (0.0, 1);
INSERT INTO values_store (value, item_id) VALUES (1.0, 1);
INSERT INTO values_store (value, item_id) VALUES (2.0, 1);
INSERT INTO values_store (value, item_id) VALUES (3.0, 2);
INSERT INTO values_store (value, item_id) VALUES (4.0, 2);

