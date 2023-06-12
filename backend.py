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


def create_event(conn, title, description, date, time_begin, time_end, type, location):
    try:
        cursor = conn.cursor()
        event_query = f"""INSERT INTO `events_submited` (`title`,`description`,`date`,`time_begin`,`time_end`,`type`,`location`) VALUES ('{title}','{description}','{date}','{time_begin}','{time_end}','{type}','{location}');"""
        cursor.execute(event_query)
        conn.commit()
        cursor.close()
    except Error as db_connection_error:
        return "Возникла ошибка: ", db_connection_error
    return True


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


def submit_event(title, description, date, time_begin, time_end, type, location):
    try:
        conn = create_connection_mysql_db(db_host=db_host, username=db_user, user_password=db_pass,
                                          db_name=db_name)
        create_event(conn, title, description, date, time_begin, time_end, type, location)

    except Error as db_connection_error:
        print("Возникла ошибка: ", db_connection_error)


def regestration(first_name, last_name, email, password):
    try:
        conn = create_connection_mysql_db(db_host=db_host, username=db_user, user_password=db_pass,
                                          db_name=db_name)
        cursor = conn.cursor()
        check_email_query = f"""SELECT * FROM users WHERE email = "{email}" """
        cursor.execute(check_email_query)
        if len(cursor.fetchall()) == 0:
            registration_query = f"""INSERT INTO users (first_name, last_name, email, is_paid, password) VALUES ('{first_name}', '{last_name}', '{email}', 0, '{password}')"""
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
                cursor.close()

                return [2, first_name, last_name, is_paid[0], id[0]]
            else:
                return [1]
        return [0]
    except Error as db_connection_error:
        return [-1]


def set_paid(email):
    try:
        conn = create_connection_mysql_db(db_host=db_host, username=db_user, user_password=db_pass,
                                          db_name=db_name)
        cursor = conn.cursor()
        pay_query = f"""UPDATE users SET is_paid =1 WHERE email = "{email}" """
        cursor.execute(pay_query)
        conn.commit()
        cursor.close()

        return 1
    except Error as db_connection_error:
        return -1


def upload_tasks(title, type, time_begin, time_end, date, user_id):
    try:
        conn = create_connection_mysql_db(db_host=db_host, username=db_user, user_password=db_pass,
                                          db_name=db_name)
        cursor = conn.cursor()
        tasks_query = f"""INSERT INTO tasks (title, type, time_begin, time_end, date, user_id) VALUES ('{title}', '{type}', '{time_begin}', '{time_end}', '{date}', '{user_id}')"""
        cursor.execute(tasks_query)
        conn.commit()
        get_id_query = f"""SELECT task_id FROM tasks WHERE user_id = {user_id}"""
        cursor.execute(get_id_query)
        id = cursor.fetchone()
        cursor.close()

        return [1, id[0]]
    except Error as db_connection_error:
        return [-1]


def change_task_date(id, date):
    try:
        conn = create_connection_mysql_db(db_host=db_host, username=db_user, user_password=db_pass,
                                          db_name=db_name)
        cursor = conn.cursor()
        change_query = f"""UPDATE tasks SET date = "{date}" WHERE task_id = {id} """
        cursor.execute(change_query)
        conn.commit()
        cursor.close()

        return 1
    except Error as db_connection_error:
        return -1


def delete_task(task_id):
    try:

        conn = create_connection_mysql_db(db_host=db_host, username=db_user, user_password=db_pass,
                                          db_name=db_name)
        cursor = conn.cursor()
        delete_query = f"""DELETE FROM tasks WHERE task_id = {task_id}"""
        cursor.execute(delete_query)
        conn.commit()
        cursor.close()

        return 1
    except Error as db_connection_error:
        print("Возникла ошибка: ", db_connection_error)


def get_tasks(user_id):
    try:
        conn = create_connection_mysql_db(db_host=db_host, username=db_user, user_password=db_pass,
                                          db_name=db_name)
        cursor = conn.cursor()
        delete_query = f"""SELECT * FROM tasks WHERE user_id = {user_id}"""
        cursor.execute(delete_query)
        tasks = cursor.fetchall()
        cursor.close()

        return tasks
    except Error as db_connection_error:
        return -1

def clear_tasks(user_id):
    try:

        conn = create_connection_mysql_db(db_host=db_host, username=db_user, user_password=db_pass,
                                          db_name=db_name)
        cursor = conn.cursor()
        delete_query = f"""DELETE FROM tasks WHERE user_id = {user_id}"""
        cursor.execute(delete_query)
        conn.commit()
        cursor.close()

        return 1
    except Error as db_connection_error:
        print("Возникла ошибка: ", db_connection_error)