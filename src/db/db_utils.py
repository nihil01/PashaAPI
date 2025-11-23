import sqlite3 as sql

#pasha
JWT_TOKEN_PASHA = ""
API_KEY_PASHA = ""

#kapital
KAPITAL_USER = ""
KAPITAL_PASS = ""

def setup_connection_bank():
    global JWT_TOKEN_PASHA, API_KEY_PASHA, KAPITAL_USER, KAPITAL_PASS

    try:
        with sql.connect("db/bank.db") as connection:
            cursor = connection.cursor()

            cursor.executescript("""
                 CREATE TABLE IF NOT EXISTS pasha_credentials
                 (
                     jwt
                         TEXT,
    
                     api_key
                         TEXT
                 );
    
                 CREATE TABLE IF NOT EXISTS kapital_credentials
                 (
                     username
                         TEXT,
    
                     password
                         TEXT
                 );
             """)

            # pasha
            cursor.execute("SELECT * FROM pasha_credentials")
            data_pasha = cursor.fetchall()

            if len(data_pasha) == 0:
                print("Inserted default test credentials for Pasha Bank. Please change them in db/bank.db")
                JWT_TOKEN_PASHA = "REPLACE"
                API_KEY_PASHA = "REPLACE"

                cursor.execute("INSERT INTO pasha_credentials VALUES (?, ?)", ("REPLACE", "REPLACE"))
                connection.commit()

            else:
                JWT_TOKEN_PASHA = data_pasha[0][0]
                API_KEY_PASHA = data_pasha[0][1]

            # kapital
            cursor.execute("SELECT * FROM kapital_credentials")
            data_kapital = cursor.fetchall()

            if len(data_kapital) == 0:
                print("Inserted default test credentials for Kapital Bank. Please change them in db/bank.db")
                KAPITAL_USER = "REPLACE"
                KAPITAL_PASS = "REPLACE"

                cursor.execute("INSERT INTO kapital_credentials VALUES (?, ?)", ("REPLACE", "REPLACE"))
                connection.commit()

            else:
                KAPITAL_USER = data_kapital[0][0]
                KAPITAL_PASS = data_kapital[0][1]

    except sql.ProgrammingError as e:
        print("Error:", str(e))