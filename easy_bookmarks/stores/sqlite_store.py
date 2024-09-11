import sqlite3
import polars as pl
from typing import Dict, Optional

import logging

# Configure logging
log = logging.getLogger(__name__)


class SQLiteStore:
    def __init__(self, db_path: str = 'bookmarks.db'):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.table_name = 'bookmarks'
    
    def create_table(self, columns: Dict[str, str]):
        if not "uuid" in columns:
            #columns["uuid"] = "String PRIMARY KEY AUTOINCREMENT NOT NULL"
            log.warning("It is recommended to include a uuid column. Creating a autoincremental.")
        columns_with_types = ', '.join([f"{col} {dtype}" for col, dtype in columns.items()])
        print(columns_with_types)
        self.cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                {columns_with_types}
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()

    def create_table_from_dataframe(self, df: pl.DataFrame):
        # Infer column types from DataFrame
        column_types = self._infer_column_types(df)
        
        # Create table
        columns = ', '.join([f"{col} {dtype}" for col, dtype in column_types.items()])
        self.cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                uuid INTEGER PRIMARY KEY AUTOINCREMENT,
                {columns}
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()

    def _infer_column_types(self, df: pl.DataFrame) -> Dict[str, str]:
        type_mapping = {
            pl.Utf8: 'TEXT',
            pl.Int64: 'INTEGER',
            pl.Float64: 'REAL',
            pl.Boolean: 'INTEGER',
            pl.Datetime: 'TIMESTAMP'
        }
        return {col: type_mapping.get(df[col].dtype, 'TEXT') for col in df.columns}

    def add_bookmark(self, bookmark_data: Dict):
        columns = ', '.join(bookmark_data.keys())
        placeholders = ', '.join(['?' for _ in bookmark_data])
        query = f"INSERT INTO {self.table_name} ({columns}) VALUES ({placeholders})"
        self.cursor.execute(query, list(bookmark_data.values()))
        self.conn.commit()

    def get_bookmarks(self, filters: Optional[Dict] = None) -> pl.DataFrame:
        query = f"SELECT * FROM {self.table_name}"
        params = []
        if filters:
            conditions = []
            for key, value in filters.items():
                conditions.append(f"{key} = ?")
                params.append(value)
            query += " WHERE " + " AND ".join(conditions)
        
        self.cursor.execute(query, params)
        columns = [col[0] for col in self.cursor.description]
        data = self.cursor.fetchall()
        return pl.from_records(data, orient='row', schema=columns)

    def update_bookmark(self, bookmark_id: int, update_data: Dict):
        set_clause = ', '.join([f"{key} = ?" for key in update_data.keys()])
        query = f"UPDATE {self.table_name} SET {set_clause} WHERE id = ?"
        params = list(update_data.values()) + [bookmark_id]
        self.cursor.execute(query, params)
        self.conn.commit()

    def delete_bookmark(self, bookmark_id: int):
        self.cursor.execute(f"DELETE FROM {self.table_name} WHERE id = ?", (bookmark_id,))
        self.conn.commit()

    def close(self):
        self.conn.close()

    def drop_table(self):
        query = f"DROP TABLE IF EXISTS {self.table_name}"
        self.cursor.execute(query)
        self.conn.commit()

