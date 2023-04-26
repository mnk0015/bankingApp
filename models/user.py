from .database import get_db

class User:
    def __init__(self, id=None, name=None, dob=None, pin=None, balance=None):
        self.id = id
        self.name = name
        self.dob = dob
        self.pin = pin
        self.balance = balance
        
    def save(self):
        db = get_db()
        cur = db.cursor()
        
        if not self.id:
            # Create new user
            cur.execute("INSERT INTO users (name, dob, pin, balance) VALUES (?, ?, ?, ?)",
                        (self.name, self.dob, self.pin, self.balance))
            self.id = cur.lastrowid
        else:
            # Update existing user
            cur.execute("UPDATE users SET name=?, dob=?, pin=?, balance=? WHERE id=?",
                        (self.name, self.dob, self.pin, self.balance, self.id))
        db.commit()
    
    @staticmethod
    def get_by_id(user_id):
        db = get_db()
        cur = db.cursor()
        cur.execute("SELECT id, name, dob, pin, balance FROM users WHERE id=?", (user_id,))
        user_data = cur.fetchone()
        if user_data:
            return User(*user_data)
        else:
            return None
    
    @staticmethod
    def get_by_account_number(account_number):
        db = get_db()
        cur = db.cursor()
        cur.execute("SELECT users.id, name, dob, pin, balance FROM users JOIN accounts ON users.id=accounts.user_id WHERE account_number=?", (account_number,))
        user_data = cur.fetchone()
        if user_data:
            return User(*user_data)
        else:
            return None
