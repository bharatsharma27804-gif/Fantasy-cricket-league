import sqlite3

def create_database():
    conn = sqlite3.connect('cricket_game.db')
    cursor = conn.cursor()

    #Create match table

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS match(
        player TEXT PRIMARY KEY,
        scored INTEGER,
        faced INTEGER,
        fours INTEGER,
        sixes INTEGER,
        bowled INTEGER,
        maiden INTEGER,
        given INTEGER,
        wkts INTEGER,
        catches INTEGER,
        stumping INTEGER,
        ro INTEGER
        )

    ''')

    #Create stat table

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS stats(
        player TEXT PRIMARY KEY,
        matches INTEGER,
        runs INTEGER,
        hundreds INTEGER,
        fifties INTEGER,
        value INTEGER,
        ctg TEXT)
    ''')

    ##Create teams table

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS teams (
            name TEXT PRIMARY KEY,
            players TEXT,
            value INTEGER
        )
    ''')

    #SAmple match data

    match_data = [
        ("Kohli", 102, 98, 8, 2, 0, 0, 0, 0, 0, 0, 1),
        ("YUvraj", 12, 20, 1, 0, 48, 0, 36, 1, 0, 0, 0),
        ("Rahane", 49, 75, 3, 0, 0, 0, 0, 0, 1, 0, 0),
        ("Dhawan", 32, 35, 4, 0, 0, 0, 0, 0, 0, 0, 0),
        ("Dhoni", 56, 45, 3, 1, 0, 0, 0, 0, 3, 2, 0),
        ("Axar", 8, 4, 2, 0, 48, 2, 35, 1, 0, 0, 0),
        ("Pandya", 42, 36, 3, 3, 30, 0, 25, 0, 1, 0, 0),
        ("Jadeja", 18, 10, 1, 1, 60, 3, 50, 2, 1, 0, 1),
        ("Kedar", 65, 60, 7, 0, 24, 0, 24, 0, 0, 0, 0),
        ("Ashwin", 23, 42, 3, 0, 60, 2, 45, 6, 0, 0, 0),
        ("Umesh", 0, 0, 0, 0, 54, 0, 50, 4, 1, 0, 0),
        ("Bumrah", 0, 0, 0, 0, 60, 2, 49, 1, 0, 0, 0),
        ("Bhuwaneshwar", 15, 12, 2, 0, 60, 1, 46, 2, 0, 0, 0),
        ("Rohit", 46, 65, 5, 1, 0, 0, 0, 0, 1, 0, 0),
        ("Kartick", 29, 42, 3, 0, 0, 0, 0, 0, 2, 0, 1)
    ]

    #Sample stats data

    stats_data = [
        ("Kohli", 189, 8257, 28, 43, 120, "BAT"),
        ("Yuvraj", 86, 3589, 10, 21, 100, "BAT"),
        ("Rahane", 158, 5435, 11, 31, 100, "BAT"),
        ("Dhawan", 25, 565, 2, 1, 85, "AR"),
        ("Dhoni", 78, 2573, 3, 19, 75, "BAT"),
        ("Axar", 67, 208, 0, 0, 100, "BWL"),
        ("Pandya", 70, 77, 0, 0, 75, "BWL"),
        ("Jadeja", 16, 1, 0, 0, 85, "BWL"),
        ("Kedar", 111, 675, 0, 1, 90, "BWL"),
        ("Ashwin", 136, 1914, 0, 10, 100, "AR"),
        ("Umesh", 296, 9496, 10, 64, 110, "WK"),
        ("Bumrah", 73, 1365, 0, 8, 60, "WK"),
        ("Bhuwaneshwar", 17, 289, 0, 2, 75, "AR"),
        ("Rohit", 304, 8701, 14, 52, 85, "BAT"),
        ("Kartick", 11, 111, 0, 0, 75, "AR")
    ]

    cursor.executemany("INSERT OR REPLACE INTO match VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",match_data)
    cursor.executemany("INSERT OR REPLACE INTO stats VALUES (?,?,?,?,?,?,?)",stats_data)

    conn.commit()
    conn.close()
    print("Database created and seedwd successfully")

if __name__ == '__main__':
    create_database()
