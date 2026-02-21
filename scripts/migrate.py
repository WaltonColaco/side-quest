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
        # Run each statement individually so ALTER TABLE re-runs are skipped gracefully.
        # executescript() would abort the whole file on first error.
        statements = [s.strip() for s in sql.split(';') if s.strip() and not s.strip().startswith('--')]
        for stmt in statements:
            try:
                cur.execute(stmt)
            except sqlite3.OperationalError as e:
                if 'duplicate column' in str(e).lower():
                    pass  # column already exists — safe to ignore on re-run
                else:
                    raise
        print(f"Applied migration {mig.name}")

    con.commit()
    con.close()
    print(f"Database ready at {db_path}")

if __name__ == '__main__':
    main()
