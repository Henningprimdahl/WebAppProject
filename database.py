import sqlite3
import pandas as pd

def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    
    # Create Movies table
    c.execute('''
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            genre TEXT,
            director TEXT,
            actors TEXT,
            year INTEGER,
            runtime INTEGER,
            rating REAL,
            votes INTEGER,
            overview TEXT
        )
    ''')
    
    # Read CSV file into DataFrame
    df = pd.read_csv('imdb_top_1000.csv')
    
    # Insert data into Movies table
    for _, row in df.iterrows():
        actors = f"{row['Star1']}, {row['Star2']}, {row['Star3']}, {row['Star4']}"
        c.execute('''
            INSERT INTO movies (title, genre, director, actors, year, runtime, rating, votes, overview) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (row['Series_Title'], row['Genre'], row['Director'], actors, row['Released_Year'], int(row['Runtime'].split()[0]), row['IMDB_Rating'], row['No_of_Votes'], row['Overview']))
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
