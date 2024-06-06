from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import re

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def is_valid_title(title):
    # Allow only alphanumeric characters and spaces
    pattern = re.compile(r'^[a-zA-Z0-9 ]+$')
    return pattern.match(title) is not None

@app.route('/')
def index():
    conn = get_db_connection()
    movies = conn.execute('SELECT * FROM movies').fetchall()
    conn.close()
    return render_template('index.html', movies=movies)

@app.route('/search', methods=('GET', 'POST'))
def search():
    if request.method == 'POST':
        title_query = request.form.get('title')
        genre_query = request.form.get('genre')
        rating_query = request.form.get('rating')
        year_query = request.form.get('year')
        director_query = request.form.get('director')
        star_query = request.form.get('star')
        
        conn = get_db_connection()
        
        query = "SELECT * FROM movies WHERE 1=1"
        params = []
        
        if title_query:
            query += " AND title LIKE ?"
            params.append(f"%{title_query}%")
        if genre_query:
            query += " AND genre LIKE ?"
            params.append(f"%{genre_query}%")
        if rating_query:
            query += " AND rating >= ?"
            params.append(rating_query)
        if year_query:
            query += " AND year = ?"
            params.append(year_query)
        if director_query:
            query += " AND director LIKE ?"
            params.append(f"%{director_query}%")
        if star_query:
            query += " AND actors LIKE ?"
            params.append(f"%{star_query}%")
        
        movies = conn.execute(query, params).fetchall()
        conn.close()
        return render_template('index.html', movies=movies, title_query=title_query, genre_query=genre_query, rating_query=rating_query, year_query=year_query, director_query=director_query, star_query=star_query)
    
    return redirect(url_for('index'))

@app.route('/add', methods=('GET', 'POST'))
def add():
    if request.method == 'POST':
        title = request.form['title']
        genre = request.form['genre']
        director = request.form['director']
        actors = request.form['actors']
        year = request.form['year']
        runtime = request.form['runtime']
        rating = request.form['rating']
        votes = request.form['votes']
        overview = request.form['overview']
        
        if not is_valid_title(title):
            return "Invalid title. Only alphanumeric characters and spaces are allowed."
        
        conn = get_db_connection()
        conn.execute('INSERT INTO movies (title, genre, director, actors, year, runtime, rating, votes, overview) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                     (title, genre, director, actors, year, runtime, rating, votes, overview))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    
    return render_template('add.html')

@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    conn = get_db_connection()
    movie = conn.execute('SELECT * FROM movies WHERE id = ?', (id,)).fetchone()
    conn.close()
    
    if request.method == 'POST':
        title = request.form['title']
        genre = request.form['genre']
        director = request.form['director']
        actors = request.form['actors']
        year = request.form['year']
        runtime = request.form['runtime']
        rating = request.form['rating']
        votes = request.form['votes']
        overview = request.form['overview']
        
        if not is_valid_title(title):
            return "Invalid title. Only alphanumeric characters and spaces are allowed."
        
        conn = get_db_connection()
        conn.execute('UPDATE movies SET title = ?, genre = ?, director = ?, actors = ?, year = ?, runtime = ?, rating = ?, votes = ?, overview = ? WHERE id = ?',
                     (title, genre, director, actors, year, runtime, rating, votes, overview, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    
    return render_template('edit.html', movie=movie)

@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM movies WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
