import sqlite3
from typing import List, Optional


class ChatChannel:
    def __init__(self, db_path: str = "memory/channels.db"):
        self.connection = sqlite3.connect(db_path)
        self.connection.execute("PRAGMA foreign_keys = ON")

        self.create_users_table()
        self.create_channels_table()

    # ---------- table creation ----------

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

    # ---------- user management ----------

    def create_user(self, user_id: str):
        """
        Creates user if not exists and ensures default channel exists.
        """

        with self.connection as conn:
            conn.execute(
                """
                INSERT OR IGNORE INTO users (user_id)
                VALUES (?)
                """,
                (user_id,),
            )

            # ensure default channel exists
            conn.execute(
                """
                INSERT OR IGNORE INTO channels (user_id, channel_name)
                VALUES (?, '')
                """,
                (user_id,),
            )

    # ---------- channel management ----------

    def create_channel(self, user_id: str, channel_name: str):
        """
        Adds new channel for user.
        """

        self.create_user(user_id)

        with self.connection as conn:
            conn.execute(
                """
                INSERT INTO channels (user_id, channel_name)
                VALUES (?, ?)
                """,
                (user_id, channel_name),
            )

    def delete_channel(self, user_id: str, channel_name: str):
        """
        Deletes channel.
        If deleted channel was default, resets default to ''.
        """

        with self.connection as conn:
            conn.execute(
                """
                DELETE FROM channels
                WHERE user_id = ?
                AND channel_name = ?
                """,
                (user_id, channel_name),
            )

            conn.execute(
                """
                UPDATE users
                SET default_channel = ''
                WHERE user_id = ?
                AND default_channel = ?
                """,
                (user_id, channel_name),
            )

    def list_channels(self, user_id: str) -> List[str]:
        """
        Returns list of channel names.
        """

        cursor = self.connection.execute(
            """
            SELECT channel_name
            FROM channels
            WHERE user_id = ?
            ORDER BY channel_name
            """,
            (user_id,),
        )

        return [row[0] for row in cursor.fetchall()]

    def channel_exists(self, user_id: str, channel_name: str) -> bool:
        cursor = self.connection.execute(
            """
            SELECT 1
            FROM channels
            WHERE user_id = ?
            AND channel_name = ?
            """,
            (user_id, channel_name),
        )

        return cursor.fetchone() is not None

    # ---------- default channel ----------

    def switch_channel(self, user_id: str, channel_name: str) -> bool:
        """
        Switch active channel.
        Returns True if successful.
        """

        if not self.channel_exists(user_id, channel_name):
            return False

        with self.connection as conn:
            conn.execute(
                """
                UPDATE users
                SET default_channel = ?
                WHERE user_id = ?
                """,
                (channel_name, user_id),
            )

        return True

    def get_default_channel(self, user_id: str) -> str:
        cursor = self.connection.execute(
            """
            SELECT default_channel
            FROM users
            WHERE user_id = ?
            """,
            (user_id,),
        )

        result = cursor.fetchone()

        if result is None:
            self.create_user(user_id)
            return ""

        return result[0]

    # ---------- thread id ----------

    def get_thread_id(self, user_id: str) -> str:
        """
        thread_id = user_id + channel_name
        """

        channel = self.get_default_channel(user_id)
        return f"{user_id}{channel}"

    # ---------- utility ----------

    def delete_user(self, user_id: str):
        """
        Removes user and all channels.
        """

        with self.connection as conn:
            conn.execute(
                """
                DELETE FROM users
                WHERE user_id = ?
                """,
                (user_id,),
            )

    def close(self):
        self.connection.close()
