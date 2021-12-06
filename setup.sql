CREATE TABLE IF NOT EXISTS terms (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  term TEXT UNIQUE,
  def TEXT NOT NULL,
  createdAt datetime default current_timestamp,
  termType TEXT NOT NULL
);