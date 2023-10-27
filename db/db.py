import psycopg2
from db.config import HOST, USER, PASSWORD, DATABASE
        
class DB:
    def __init__(self):
        try:
            
            self.con = psycopg2.connect(
                host=HOST,
                user=USER,
                password=PASSWORD,
                database=DATABASE,
            )
            self.cur = self.con.cursor()
            
            self.cur.execute("""CREATE TABLE IF NOT EXISTS users(user_id INTEGER PRIMARY KEY, lon FLOAT, lat FLOAT, hour INTEGER, minute INTEGER)""")
            self.con.commit()
            print('Connect successfully')
        except Exception as _ex:
            print(f"[Info] Error While Working with Postgre {_ex}")
            
    
    def user_add(self, date):
        
        self.cur.execute(f"""INSERT INTO users(user_id, lon, lat, hour, minute) VALUES({date['user_id']},{date['lat']},{date['lon']},{date['hour']},{date['minute']})""")
        self.con.commit()
        
    def select_all(self):
        
        self.cur.execute("SELECT * FROM users")
        
        try:
            return self.cur.fetchall()
        except Exception as _ex:
            print(f'[INFO] {_ex}')
        
    
    def user_check(self, user_id):
    
        self.cur.execute(f"SELECT * FROM users WHERE user_id = {user_id}")
        try:
            return self.cur.fetchone()
        except Exception:
            pass
    
    def delete_user(self, user_id):
        
        self.cur.execute(f"DELETE FROM users WHERE user_id = {user_id}")
        self.con.commit()