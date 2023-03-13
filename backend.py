import mysql.connector
from mysql.connector import Error


def create_connection_mysql_db(db_host, username, user_password, db_name=None):
    connection_db = None
    try:
        connection_db = mysql.connector.connect(
            host=db_host,
            user=username,
            passwd=user_password,
            database=db_name
        )
    except Error as db_connection_error:
        print("Возникла ошибка: ", db_connection_error)
    return connection_db


def create_event(conn, title, description, date, time_begin, time_end, type, location):
    try:
        cursor = conn.cursor()
        event_query = f"""INSERT INTO `events` (`title`,`description`,`date`,`time_begin`,`time_end`,`type`,`location`) VALUES ('{title}','{description}','{date}','{time_begin}','{time_end}','{type}','{location}');"""
        cursor.execute(event_query)
        conn.commit()
        cursor.close()
    except Error as db_connection_error:
        return ("Возникла ошибка: ", db_connection_error)
    return True


try:
    def submit_event(title, description, date, time_begin, time_end, type, location):
        conn = create_connection_mysql_db(db_host="localhost", username="root", user_password="Portakal93",
                                          db_name="testdb")
        create_event(conn, title, description, date, time_begin, time_end, type, location)


except Error as db_connection_error:
    print("Возникла ошибка: ", db_connection_error)
