import mysql.connector
from mysql.connector import Error


def create_connection_mysql_db(db_host,username,user_password, db_name=None):
    connection_db=None
    try:
        connection_db=mysql.connector.connect(
            host=db_host,
            user=username,
            passwd=user_password,
            database=db_name
        )
    except Error as db_connection_error:
        print("Возникла ошибка: ", db_connection_error)
    return connection_db


def create_event(conn,title,description,useful_links,city):
    try:
        cursor=conn.cursor()
        event_query = f"""INSERT INTO `events` (`title`,`description`,`useful_links`,`city`) VALUES ('{title}','{description}','{useful_links}','{city}');"""
        cursor.execute(event_query)
        conn.commit()
        cursor.close()
    except Error as db_connection_error:
        return ("Возникла ошибка: ", db_connection_error)
    return True


try:
    conn = create_connection_mysql_db(db_host=config.host, username=config.user, user_password=config.password,
                                      db_name=config.db_name)
    cursor=conn.cursor()
    showColumns_query="""SHOW columns from events;"""
    cursor.execute(showColumns_query)
    print(cursor.fetchall())
    create_event(conn,"Сатана","Шабашим","choZaXyinya.com","Murmansk")

    show_query = """SELECT * from events;"""
    conn.commit()
    cursor.execute(show_query)
    print(cursor.fetchall())

except Error as db_connection_error:
    print("Возникла ошибка: ", db_connection_error)