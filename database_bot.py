import sqlite3

database = sqlite3.connect('translate.db')
cursor = database.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS history(
        history_id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id INTEGER,
        from_lang TEXT,
        to_lang TEXT,
        original_text TEXT,
        translate_text TEXT
    )
''')

database.commit()
database.close()