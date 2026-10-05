import sqlite3


DATABASE = "database/landchain.db"


def get_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def init_database():
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS land_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            land_id TEXT UNIQUE NOT NULL,
            owner_name TEXT NOT NULL,
            guardian_name TEXT,
            survey_number TEXT NOT NULL,
            area REAL NOT NULL,
            land_type TEXT NOT NULL,
            state TEXT NOT NULL,
            district TEXT NOT NULL,
            taluk TEXT,
            village TEXT,
            address TEXT,
            registration_date TEXT NOT NULL,
            status TEXT DEFAULT 'Active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()


def add_land(
    land_id,
    owner_name,
    guardian_name,
    survey_number,
    area,
    land_type,
    state,
    district,
    taluk,
    village,
    address,
    registration_date
):
    connection = get_connection()

    connection.execute("""
        INSERT INTO land_records (
            land_id,
            owner_name,
            guardian_name,
            survey_number,
            area,
            land_type,
            state,
            district,
            taluk,
            village,
            address,
            registration_date
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        land_id,
        owner_name,
        guardian_name,
        survey_number,
        area,
        land_type,
        state,
        district,
        taluk,
        village,
        address,
        registration_date
    ))

    connection.commit()
    connection.close()


def get_all_land_records():
    connection = get_connection()

    records = connection.execute("""
        SELECT *
        FROM land_records
        ORDER BY id DESC
    """).fetchall()

    connection.close()

    return records
def delete_land(land_id):
    connection = get_connection()

    connection.execute("""
        DELETE FROM land_records
        WHERE land_id = ?
    """, (land_id,))

    connection.commit()
    connection.close()

def update_land(
    land_id,
    owner_name,
    guardian_name,
    survey_number,
    area,
    land_type,
    state,
    district,
    taluk,
    village,
    address,
    registration_date
):
    connection = get_connection()

    connection.execute("""
        UPDATE land_records
        SET owner_name = ?,
            guardian_name = ?,
            survey_number = ?,
            area = ?,
            land_type = ?,
            state = ?,
            district = ?,
            taluk = ?,
            village = ?,
            address = ?,
            registration_date = ?
        WHERE land_id = ?
    """, (
        owner_name,
        guardian_name,
        survey_number,
        area,
        land_type,
        state,
        district,
        taluk,
        village,
        address,
        registration_date,
        land_id
    ))

    connection.commit()
    connection.close()
