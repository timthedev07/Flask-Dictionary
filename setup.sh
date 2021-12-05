[[ -f filename ]] || touch db.db
sqlite3 db.db ".read setup.sql"