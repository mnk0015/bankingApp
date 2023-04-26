import mysql.connector
connection = mysql.connector.connect(host= 'localhost', username='root', password='Vanguardchamp2005$', database='example')
cursor = connection.cursor()
class Database:
    def __init__(self):
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="password",
            database="bank"
        )
        self.cursor = self.db.cursor()

    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255),
                dob DATE,
                pin INT
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS accounts (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                balance DECIMAL(10, 2),
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)

        self.db.commit()

    def insert_user(self, name, dob, pin):
        self.cursor.execute("""
            INSERT INTO users (name, dob, pin) 
            VALUES (%s, %s, %s)
        """, (name, dob, pin))
        self.db.commit()
        return self.cursor.lastrowid

    def insert_account(self, user_id, balance=0):
        self.cursor.execute("""
            INSERT INTO accounts (user_id, balance) 
            VALUES (%s, %s)
        """, (user_id, balance))
        self.db.commit()
        return self.cursor.lastrowid

    def get_user_by_id(self, id):
        self.cursor.execute("""
            SELECT * FROM users WHERE id = %s
        """, (id,))
        return self.cursor.fetchone()

    def get_user_by_pin(self, pin):
        self.cursor.execute("""
            SELECT * FROM users WHERE pin = %s
        """, (pin,))
        return self.cursor.fetchone()

    def get_account_by_user_id(self, user_id):
        self.cursor.execute("""
            SELECT * FROM accounts WHERE user_id = %s
        """, (user_id,))
        return self.cursor.fetchone()

    def update_account_balance(self, account_id, balance):
        self.cursor.execute("""
            UPDATE accounts SET balance = %s WHERE id = %s
        """, (balance, account_id))
        self.db.commit()

db = Database()
