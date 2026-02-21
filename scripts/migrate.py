#!/usr/bin/env python3
"""Apply SQL migrations to local SQLite DB (db/assessment.db)."""
import sqlite3
from pathlib import Path

def main():
    db_path = Path('db/assessment.db')
    mig_dir = Path('migrations')
    db_path.parent.mkdir(parents=True, exist_ok=True)

    con = sqlite3.connect(db_path)
    cur = con.cursor()

    for mig in sorted(mig_dir.glob('*.sql')):
        sql = mig.read_text(encoding='utf-8')
        cur.executescript(sql)
        print(f"Applied migration {mig.name}")

    con.commit()
    con.close()
    print(f"Database ready at {db_path}")

if __name__ == '__main__':
    main()
