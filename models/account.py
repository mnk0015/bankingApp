from utils.database import get_db

class Account:
    def __init__(self, id=None, user_id=None, account_number=None):
        self.id = id
        self.user_id = user_id
        self.account_number = account_number
        
    def save(self):
        db = get_db()
        cur = db.cursor()
        
        if not self.id:
            # Create new account
            cur.execute("INSERT INTO accounts (user_id, account_number) VALUES (?, ?)",
                        (self.user_id, self.account_number))
            self.id = cur.lastrowid
        else:
            # Update existing account
            cur.execute("UPDATE accounts SET user_id=?, account_number=? WHERE id=?",
                        (self.user_id, self.account_number, self.id))
        db.commit()
    
    @staticmethod
    def get_by_account_number(account_number):
        db = get_db()
        cur = db.cursor()
        cur.execute("SELECT id, user_id, account_number FROM accounts WHERE account_number=?", (account_number,))
        account_data = cur.fetchone()
        if account_data:
            return Account(*account_data)
        else:
            return None
