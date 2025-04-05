# connection.py
import pymysql.cursors
import os
from dotenv import load_dotenv

# Load environment variables from a .env file (recommended)
load_dotenv()

class MySQLConnection:
    def __init__(self, db):
        # Load credentials securely
        connection = pymysql.connect(
            host=os.getenv('DB_HOST', 'database-1.cedo8qm2k05m.us-east-1.rds.amazonaws.com'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', 'Kabul_2525'),
            db=db,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=False
        )
        self.connection = connection

    def query_db(self, query: str, data: dict = None):
        with self.connection.cursor() as cursor:
            try:
                query = cursor.mogrify(query, data)
                print("Running Query:", query)

                cursor.execute(query)
                if query.lower().find("insert") >= 0:
                    self.connection.commit()
                    return cursor.lastrowid
                elif query.lower().find("select") >= 0:
                    result = cursor.fetchall()
                    return result
                else:
                    self.connection.commit()
            except Exception as e:
                print("Something went wrong:", e)
                return False
            finally:
                self.connection.close()

def connectToMySQL(db):
    return MySQLConnection(db)

