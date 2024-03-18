import mysql.connector
import settings  # Import your settings.py file

def create_topic(title):
    try:
        connection = mysql.connector.connect(
            host=settings.DBHOST,
            user=settings.DBUSER,
            password=settings.DBPASSWD,
            database=settings.DBDATABASE
        )
        
        cursor = connection.cursor()
        cursor.callproc("CreateTopic", [title])
        connection.commit()
        
        print("Topic added successfully.")
    except mysql.connector.Error as error:
        print("Failed to add topic:", error)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    title = input("Enter the topic title: ")
    create_topic(title)
