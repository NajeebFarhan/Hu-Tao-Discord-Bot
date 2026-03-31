import sqlite3

class ChatChannel:
    def __init__(self):
        self.connection = self.get_connection()
        
        
    def get_connection(self):
        return sqlite3.connect("memory/channels.db")
    
    
    def create_users_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            default_channel TEXT NOT NULL DEFAULT ''
        );
        """
        
        with self.connection as conn:
            conn.execute(query)
            
    
    def create_channels_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS channels (
            user_id TEXT NOT NULL,
            channel_name TEXT NOT NULL,
            PRIMARY KEY (user_id, channel_name),
            FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
        );
        """
        
        with self.connection as conn:
            conn.execute(query)
        
        
    def create_user(self, user_id: str):
        query = """
        INSERT OR IGNORE INTO users (user_id)
        VALUES (?);
        """
        
        with self.connection as conn:
            conn.execute(query, (user_id,))