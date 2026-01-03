import logging
import sqlite3 as sql

#pasha
JWT_TOKEN_PASHA = ""
API_KEY_PASHA = ""

#kapital
KAPITAL_USER = ""
KAPITAL_PASS = ""

#abb
ABB_USER = ""
ABB_PASS = ""

def setup_connection_bank():
    global JWT_TOKEN_PASHA, API_KEY_PASHA, KAPITAL_USER, KAPITAL_PASS, ABB_USER, ABB_PASS

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
                     
                 CREATE TABLE IF NOT EXISTS abb_credentials
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
                logging.info("Inserted default test credentials for Pasha Bank. Please change them in db/bank.db")
                JWT_TOKEN_PASHA = "REPLACE"
                API_KEY_PASHA = "REPLACE"

                cursor.execute("INSERT INTO pasha_credentials VALUES (?, ?)", ("REPLACE", "REPLACE"))
                connection.commit()

            else:
                JWT_TOKEN_PASHA = data_pasha[0][0]
                API_KEY_PASHA = data_pasha[0][1]

            # abb
            cursor.execute("SELECT * FROM abb_credentials")
            data_abb = cursor.fetchall()

            if len(data_abb) == 0:
                logging.info("Inserted default test credentials for ABB Bank. Please change them in db/bank.db")
                ABB_USER = "REPLACE"
                ABB_PASS = "REPLACE"

                cursor.execute("INSERT INTO abb_credentials VALUES (?, ?)", ("REPLACE", "REPLACE"))
                connection.commit()

            else:
                ABB_USER = data_abb[0][0]
                ABB_PASS = data_abb[0][1]

            # kapital
            cursor.execute("SELECT * FROM kapital_credentials")
            data_abb = cursor.fetchall()

            if len(data_abb) == 0:
                logging.info("Inserted default test credentials for Kapital Bank. Please change them in db/bank.db")
                KAPITAL_USER = "REPLACE"
                KAPITAL_PASS = "REPLACE"

                cursor.execute("INSERT INTO kapital_credentials VALUES (?, ?)", ("REPLACE", "REPLACE"))
                connection.commit()

            else:
                KAPITAL_USER = data_abb[0][0]
                KAPITAL_PASS = data_abb[0][1]


    except sql.ProgrammingError as e:
        print("Error:", str(e))


def save_data(bank:str, jwt: str, api_key: str):
    try:
        with sql.connect("db/bank.db") as connection:
            cursor = connection.cursor()

            match bank:
                case "Pasha_Bank":
                    cursor.execute("UPDATE pasha_credentials SET jwt=?, api_key=?", (jwt, api_key))
                    connection.commit()
                    return
                case "Kapital_Bank":
                    cursor.execute("UPDATE kapital_credentials SET username=?, password=?", (jwt, api_key))
                    connection.commit()
                    return
                case "ABB_Bank":
                    cursor.execute("UPDATE abb_credentials SET username=?, password=?", (jwt, api_key))
                    connection.commit()
                    return
                case _:
                    print("Invalid bank name")
    except sql.ProgrammingError as e:
        print("Error:", str(e))