import psycopg2
from db_config import load_config

database_name = 'moviematch'
def initialize_database():
    connection = None
    try:
        connection = psycopg2.connect(**load_config())
        connection.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = connection.cursor()

        # Create the Movie table if not exists
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Movie (
                id SERIAL PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                plot TEXT,
                cover_image_url VARCHAR(255),
                year INT,
                rated VARCHAR(50),
                released_date DATE,
                runtime VARCHAR(50),
                genre VARCHAR(255),
                director VARCHAR(255),
                writer VARCHAR(255),
                actors VARCHAR(255),
                language VARCHAR(100),
                country VARCHAR(100),
                awards VARCHAR(255),
                imdb_rating FLOAT,
                imdb_id VARCHAR(50),
                source_url VARCHAR(100),
                trailer_link VARCHAR(255)
            )
        ''')
        connection.commit()

        print("Table 'Movie' created successfully.")
    except psycopg2.Error as e:
        print("Error:", e)
    finally:
        if connection:
            connection.close()

def connect():
    try:
        connection = psycopg2.connect(**load_config())
        return connection
    except psycopg2.Error as e:
        print("Error:", e)

def insert_movie(movie):
    connection = connect()
    if connection:
        try:
            cursor = connection.cursor()

            cursor.execute('''
                INSERT INTO Movie (
                    title, plot, cover_image_url, year, rated, released_date, runtime, genre,
                    director, writer, actors, language, country, awards,
                    imdb_rating, imdb_id, source_url, trailer_link
                )
                VALUES (
                    %(title)s, %(plot)s, %(cover_image_url)s, %(year)s, %(rated)s, %(released_date)s,
                    %(runtime)s, %(genre)s, %(director)s, %(writer)s, %(actors)s, %(language)s,
                    %(country)s, %(awards)s, %(imdb_rating)s, %(imdb_id)s,
                    %(source_url)s, %(trailer_link)s
                )
            ''', movie)

            connection.commit()

            print("Movie record inserted successfully.")
        except psycopg2.Error as e:
            print("Error:", e)
        finally:
            connection.close()
            
def insert_movies(movies):
    connection = connect()
    if connection:
        try:
            cursor = connection.cursor()

            cursor.executemany('''
                INSERT INTO Movie (
                    title, plot, cover_image_url, year, rated, released_date, runtime, genre,
                    director, writer, actors, language, country, awards,
                    imdb_rating, imdb_id, source_url, trailer_link
                )
                VALUES (
                    %(title)s, %(plot)s, %(cover_image_url)s, %(year)s, %(rated)s, %(released_date)s, %(runtime)s, %(genre)s,
                    %(director)s, %(writer)s, %(actors)s, %(language)s, %(country)s, %(awards)s,
                    %(imdb_rating)s, %(imdb_id)s, %(source_url)s, %(trailer_link)s
                )
            ''', movies)

            connection.commit()

            print(f"{len(movies)} movie records inserted successfully.")
        except psycopg2.Error as e:
            print("Error:", e)
        finally:
            connection.close()
            
if __name__ == "__main__":
    # Initialize the database
    initialize_database()

