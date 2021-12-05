CREATE TABLE IF NOT EXISTS words (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  word TEXT UNIQUE,
  def TEXT NOT NULL,
  createdAt datetime default current_timestamp,
  wordType TEXT NOT NULL
);