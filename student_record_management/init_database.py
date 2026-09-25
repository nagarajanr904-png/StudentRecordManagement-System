"""
Automated Database Initializer for Free Online MySQL.
Connects directly to your remote cloud database and provisions all tables and seed records.
No MySQL Workbench or desktop GUI required!
"""

import sys
import os
from pathlib import Path

# Add project root to path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

from app.config.settings import Settings, logger

try:
    import mysql.connector
    from mysql.connector import Error as MySQLError
except ImportError:
    print("\n❌ Error: mysql-connector-python is not installed.")
    print("Please install dependencies first: pip install -r requirements.txt\n")
    sys.exit(1)


def execute_sql_file(cursor, file_path: Path) -> int:
    """Reads a SQL file and executes each statement sequentially."""
    if not file_path.exists():
        print(f"❌ File not found: {file_path}")
        return 0

    with open(file_path, "r", encoding="utf-8") as f:
        sql_content = f.read()

    # Split statements by semicolon while ignoring comments
    statements = []
    current_stmt = []
    for line in sql_content.splitlines():
        trimmed = line.strip()
        if not trimmed or trimmed.startswith("--") or trimmed.startswith("/*"):
            continue
        current_stmt.append(line)
        if trimmed.endswith(";"):
            statement_text = "\n".join(current_stmt).strip()
            if statement_text.endswith(";"):
                statement_text = statement_text[:-1].strip()
            if statement_text:
                statements.append(statement_text)
            current_stmt = []

    executed_count = 0
    for stmt in statements:
        try:
            cursor.execute(stmt)
            executed_count += 1
        except Exception as e:
            # Skip harmless table already exists or foreign key warnings if re-running
            if "already exists" in str(e).lower() or "duplicate" in str(e).lower():
                continue
            print(f"⚠️ Statement notice: {e}")

    return executed_count


def init_database() -> None:
    print("=" * 70)
    print("  ScholarPulse - Free Online MySQL Database Initializer")
    print("=" * 70)

    Settings.reload_env()

    if not Settings.is_db_configured():
        print("\n⚠️ Database credentials not found in .env!")
        print("Please configure your .env file with your free online MySQL credentials:")
        print("  DB_HOST=your-free-mysql-host.cloud")
        print("  DB_PORT=3306")
        print("  DB_NAME=defaultdb")
        print("  DB_USER=your_username")
        print("  DB_PASSWORD=your_password\n")
        print("Tip: You can get free MySQL instances from Aiven, TiDB Cloud, Clever Cloud, etc.")
        print("No MySQL Workbench is needed!\n")
        return

    print(f"\n📡 Connecting to Cloud MySQL: {Settings.DB_HOST}:{Settings.DB_PORT}")
    print(f"📁 Target Database: {Settings.DB_NAME}")
    print(f"👤 User: {Settings.DB_USER}")

    try:
        conn = mysql.connector.connect(
            host=Settings.DB_HOST,
            port=Settings.DB_PORT,
            database=Settings.DB_NAME,
            user=Settings.DB_USER,
            password=Settings.DB_PASSWORD,
            connection_timeout=Settings.DB_CONNECT_TIMEOUT,
            autocommit=True,
        )

        cursor = conn.cursor()
        print("✅ Successfully established connection to free online MySQL server!\n")

        # 1. Execute schema.sql
        schema_path = BASE_DIR / "database" / "schema.sql"
        print(f"⚙️ Running DDL Schema ({schema_path.name})...")
        schema_count = execute_sql_file(cursor, schema_path)
        print(f"   ✓ Executed {schema_count} schema statements successfully.")

        # 2. Check if departments exist
        cursor.execute("SELECT COUNT(*) FROM departments;")
        dept_count = cursor.fetchone()[0]

        if dept_count == 0:
            seed_path = BASE_DIR / "database" / "seed.sql"
            print(f"🌱 Inserting sample seed records ({seed_path.name})...")
            seed_count = execute_sql_file(cursor, seed_path)
            print(f"   ✓ Executed {seed_count} seed statements successfully.")
        else:
            print(f"ℹ️ Database already contains {dept_count} department records (skipping duplicate seed).")

        # Verify created tables
        cursor.execute("SHOW TABLES;")
        tables = [row[0] for row in cursor.fetchall()]
        print("\n📊 Verified Tables on Remote MySQL:")
        for t in tables:
            cursor.execute(f"SELECT COUNT(*) FROM `{t}`;")
            count = cursor.fetchone()[0]
            print(f"   • {t}: {count} records")

        cursor.close()
        conn.close()

        print("\n🎉 All done! Your free online MySQL database is fully operational.")
        print("🚀 You can now launch the application:")
        print("   python main.py\n")

    except Exception as e:
        print(f"\n❌ Connection or execution failed: {e}")
        print("\nTroubleshooting tips for free online MySQL:")
        print("1. Verify host, port, database, username, and password in .env")
        print("2. Ensure the remote cloud provider allows incoming connections (firewall / IP allowlist 0.0.0.0/0)")
        print("3. Check that your internet connection is active.\n")


if __name__ == "__main__":
    init_database()
