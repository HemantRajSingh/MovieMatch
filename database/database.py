import psycopg2

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

def insert_movie(title, plot, cover_image_url, year, source, trailer_link):
    connection = connect()
    if connection:
        try:
            cursor = connection.cursor()

            cursor.execute('''
                INSERT INTO Movie (title, plot, cover_image_url, year, source, trailer_link)
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', (title, plot, cover_image_url, year, source, trailer_link))

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
                INSERT INTO Movie (title, plot, cover_image_url, year, source, trailer_link)
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', movies)

            connection.commit()

            print(f"{len(movies)} movie records inserted successfully.")
        except psycopg2.Error as e:
            print("Error:", e)
        finally:
            connection.close()

