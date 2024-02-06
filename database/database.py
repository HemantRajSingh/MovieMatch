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
