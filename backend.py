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
        event_query = f"""INSERT INTO `events_submited` (`title`,`description`,`date`,`time_begin`,`time_end`,`type`,`location`) VALUES ('{title}','{description}','{date}','{time_begin}','{time_end}','{type}','{location}');"""
        cursor.execute(event_query)
        conn.commit()
        cursor.close()
    except Error as db_connection_error:
        return ("Возникла ошибка: ", db_connection_error)
    return True


def get_events(event_type, location):
    try:
        conn = create_connection_mysql_db(db_host="localhost", username="root", user_password="Portakal93",
                                          db_name="testdb")
        cursor = conn.cursor()
        get_event_query = f"""SELECT * FROM events WHERE location = "{location}" AND type = "{event_type}" """
        cursor.execute(get_event_query)
        cursor.close()
        return cursor.fetchall()
    except Error as db_connection_error:
        print("Возникла ошибка: ", db_connection_error)


def submit_event(title, description, date, time_begin, time_end, type, location):
    try:
        conn = create_connection_mysql_db(db_host="localhost", username="root", user_password="Portakal93",
                                          db_name="testdb")
        create_event(conn, title, description, date, time_begin, time_end, type, location)

    except Error as db_connection_error:
        print("Возникла ошибка: ", db_connection_error)


def regestration(first_name, last_name, email, password):
    try:
        conn = create_connection_mysql_db(db_host="localhost", username="root", user_password="Portakal93",
                                          db_name="testdb")
        cursor = conn.cursor()
        check_email_query = f"""SELECT * FROM users WHERE email = "{email}" """
        cursor.execute(check_email_query)
        if len(cursor.fetchall()) == 0:
            registration_query = f"""INSERT INTO users (first_name, last_name, email, password) VALUES ('{first_name}', '{last_name}', '{email}', '{password}')"""
            cursor.execute(registration_query)
            conn.commit()
            cursor.close()
            return 1
        else:
            return 0

    except Error as db_connection_error:
        return -1


def log_in(email, password):
    try:
        conn = create_connection_mysql_db(db_host="localhost", username="root", user_password="Portakal93",
                                          db_name="testdb")
        cursor = conn.cursor()
        check_email_query = f"""SELECT password FROM users WHERE email = "{email}" """
        cursor.execute(check_email_query)
        users = cursor.fetchall()
        if len(users) == 1:
            print(str(users[0]).split("""'""")[1])
            if str(users[0]).split("""'""")[1] == password:
                get_first_name_query = f"""SELECT first_name FROM users WHERE email = "{email}" """
                cursor.execute(get_first_name_query)
                first_name = str(cursor.fetchone()).split("""'""")[1]
                get_first_name_query = f"""SELECT last_name FROM users WHERE email = "{email}" """
                cursor.execute(get_first_name_query)
                last_name = str(cursor.fetchone()).split("""'""")[1]

                return [2, first_name, last_name]
            else:
                return [1]
        return [0]
    except Error as db_connection_error:
        return [-1]
