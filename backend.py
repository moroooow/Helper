import mysql.connector
from mysql.connector import Error

db_pass = "Portakal93"
db_user = "root"
db_host = "localhost"
db_name = "testdb"


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


def get_events(event_type, location):
    try:
        conn = create_connection_mysql_db(db_host=db_host, username=db_user, user_password=db_pass,
                                          db_name=db_name)
        cursor = conn.cursor()
        get_event_query = f"""SELECT * FROM events WHERE location = "{location}" AND type = "{event_type}" """
        cursor.execute(get_event_query)
        events = cursor.fetchall()
        cursor.close()
        return events
    except Error as db_connection_error:
        print("Возникла ошибка: ", db_connection_error)


def regestration(first_name, last_name, email, password, city):
    try:
        conn = create_connection_mysql_db(db_host=db_host, username=db_user, user_password=db_pass,
                                          db_name=db_name)
        cursor = conn.cursor()
        check_email_query = f"""SELECT * FROM users WHERE email = "{email}" """
        cursor.execute(check_email_query)
        if len(cursor.fetchall()) == 0:
            registration_query = f"""INSERT INTO users (first_name, last_name, email, city, is_paid, password) VALUES ('{first_name}', '{last_name}', '{email}', '{city}', 0, '{password}')"""
            cursor.execute(registration_query)
            conn.commit()
            get_id_query = f"""SELECT user_id FROM users WHERE email = "{email}" """
            cursor.execute(get_id_query)
            id = cursor.fetchone()
            cursor.close()
            return [1, id]
        else:
            return [0]

    except Error as db_connection_error:
        return [-1]


def log_in(email, password):
    try:
        conn = create_connection_mysql_db(db_host=db_host, username=db_user, user_password=db_pass,
                                          db_name=db_name)
        cursor = conn.cursor()
        check_email_query = f"""SELECT password FROM users WHERE email = "{email}" """
        cursor.execute(check_email_query)
        users = cursor.fetchall()
        if len(users) == 1:
            if str(users[0]).split("""'""")[1] == password:
                get_first_name_query = f"""SELECT first_name FROM users WHERE email = "{email}" """
                cursor.execute(get_first_name_query)
                first_name = str(cursor.fetchone()).split("""'""")[1]
                get_first_name_query = f"""SELECT last_name FROM users WHERE email = "{email}" """
                cursor.execute(get_first_name_query)
                last_name = str(cursor.fetchone()).split("""'""")[1]
                get_is_paid_query = f"""SELECT is_paid FROM users WHERE email = "{email}" """
                cursor.execute(get_is_paid_query)
                is_paid = cursor.fetchone()
                get_id_query = f"""SELECT user_id FROM users WHERE email = "{email}" """
                cursor.execute(get_id_query)
                id = cursor.fetchone()
                get_city_query = f"""SELECT city FROM users WHERE email = "{email}" """
                cursor.close()

                return [2, first_name, last_name, is_paid[0], id[0], ]
            else:
                return [1]
        return [0]
    except Error as db_connection_error:
        return [-1]


def set_interests(user_id, sports, concerts, recreation):
    try:
        conn = create_connection_mysql_db(db_host=db_host, username=db_user, user_password=db_pass,
                                          db_name=db_name)
        cursor = conn.cursor()
        set_inerests_query = f"""INSERT INTO interests (user_id, concerts, sports, recreation) VALUES ('{user_id[0]}', '{concerts}', '{sports}', '{recreation}')"""
        cursor.execute(set_inerests_query)
        conn.commit()
        cursor.close()

        return 1
    except Error as db_connection_error:
        return -1
