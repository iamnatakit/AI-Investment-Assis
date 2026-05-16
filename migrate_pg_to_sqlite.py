import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

def migrate():
    # PostgreSQL Engine
    PG_URL = "postgresql://user:password@localhost:5433/investment_chatbot"
    pg_engine = create_engine(PG_URL)

    # SQLite Engine
    SQLITE_URL = "sqlite:///./investment_chatbot.db"
    sqlite_engine = create_engine(SQLITE_URL)

    # Reflect PG schema
    pg_meta = MetaData()
    pg_meta.reflect(bind=pg_engine)

    # Create tables in SQLite
    pg_meta.create_all(bind=sqlite_engine)
    print("✅ Tables created in SQLite.")

    # Copy data
    for table in pg_meta.sorted_tables:
        print(f"Migrating table: {table.name}...")
        with pg_engine.connect() as pg_conn:
            rows = pg_conn.execute(table.select()).fetchall()
        
        if rows:
            # Convert rows to list of dicts
            cols = table.columns.keys()
            
            # Extract values according to column names (SQLAlchemy 2.0 style)
            data = []
            for row in rows:
                row_dict = {}
                for i, col in enumerate(cols):
                    row_dict[col] = row[i]
                data.append(row_dict)
            
            with sqlite_engine.begin() as sqlite_conn:
                sqlite_conn.execute(table.insert(), data)
            print(f"  ➡️ Inserted {len(rows)} rows.")
        else:
            print(f"  ➡️ No data to copy.")

    print("🎉 Migration from PostgreSQL to SQLite complete!")

if __name__ == "__main__":
    migrate()
