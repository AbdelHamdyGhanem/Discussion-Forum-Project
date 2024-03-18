import pymysql
import settings

def create_user(username, email, password):
    try:
        db_connection = pymysql.connect(
            host=settings.DBHOST,
            user=settings.DBUSER,
            password=settings.DBPASSWD,
            database=settings.DBDATABASE,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )

        cursor = db_connection.cursor()

        cursor.callproc('CreateUser', (username, email, password))

        db_connection.commit()

        print("User created successfully.")

    except pymysql.Error as error:
        print("Error creating user:", error)

    finally:
        if 'db_connection' in locals() and db_connection.open:
            cursor.close()
            db_connection.close()

if __name__ == "__main__":
    username = input("Enter username: ")
    email = input("Enter email: ")
    password = input("Enter password: ")

    create_user(username, email, password)
