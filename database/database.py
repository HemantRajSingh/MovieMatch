import psycopg2
from db_config import load_config

database_name = 'moviematch'
def initialize_database():
    try:
        connection = psycopg2.connect(**load_config())
        connection.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = connection.cursor()

        # Check if the database exists
        cursor.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{database_name}'")
        exists = cursor.fetchone()

        # If the database doesn't exist, create it
        if not exists:
            cursor.execute(f"CREATE DATABASE {database_name}")
            connection.commit()
            print("Database 'moviematch' created successfully.")

        # Switch to moviematch database
        cursor.execute(f"set search_path='{database_name}'")
        connection.commit()

        # Create the Movie table if not exists
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Movie (
                id SERIAL PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                plot TEXT,
                cover_image_url VARCHAR(255),
                year INT,
                source_url VARCHAR(100),
                trailer_link VARCHAR(255)
            )
        ''')
        connection.commit()

        print("Table 'Movie' created successfully.")
    except psycopg2.Error as e:
        print("Error:", e)
    finally:
        # Close the database connection
        if connection:
            connection.close()


# Call the function to initialize the database and table
initialize_database()

def connect():
    try:
        connection = psycopg2.connect(
            user='postgres',
            password='procit',
            host='localhost',
            database='moviematch'
        )
        return connection
    except psycopg2.Error as e:
        print("Error:", e)

def insert_movie(title, plot, cover_image_url, year, source_url, trailer_link):
    connection = connect()
    if connection:
        try:
            cursor = connection.cursor()

            cursor.execute('''
                INSERT INTO Movie (title, plot, cover_image_url, year, source_url, trailer_link)
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', (title, plot, cover_image_url, year, source_url, trailer_link))

            connection.commit()

            print("Movie record inserted successfully.")
        except psycopg2.Error as e:
            print("Error:", e)
        finally:
            connection.close()
            
# Example usage:
# movies_to_insert = [
#     ('Title1', 'Plot1', 'Image1.jpg', 2022, 'Source1', 'Trailer1'),
#     ('Title2', 'Plot2', 'Image2.jpg', 2023, 'Source2', 'Trailer2'),
#     # Add more entries as needed
# ]
# insert_movies(movies_to_insert)
def insert_movies(movies):
    connection = connect()
    if connection:
        try:
            cursor = connection.cursor()

            cursor.executemany('''
                INSERT INTO Movie (title, plot, cover_image_url, year, source_url, trailer_link)
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', movies)

            connection.commit()

            print(f"{len(movies)} movie records inserted successfully.")
        except psycopg2.Error as e:
            print("Error:", e)
        finally:
            connection.close()

