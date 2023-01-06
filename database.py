from path_logger import logger


@logger
def delete_db(conn):
    cur.execute("""
        DROP TABLE client, phone_number CASCADE;
        """)


@logger
def create_db(conn):
    cur.execute("""
        CREATE TABLE IF NOT EXISTS client(
            client_id SERIAL PRIMARY KEY,
            first_name VARCHAR(30) NOT NULL,
            last_name VARCHAR(40) NOT NULL,
            email TEXT UNIQUE
        );
        """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS phone_number(
            id SERIAL PRIMARY KEY,
            client_id INTEGER NOT NULL REFERENCES client(client_id),
            phone_number VARCHAR(20) UNIQUE
        );
        """)


@logger
def add_client(conn, first_name, last_name, email):
    cur.execute("""
        INSERT INTO client(first_name, last_name, email) VALUES(%s, %s, %s) RETURNING client_id;""",
                (first_name, last_name, email))
    conn.commit()
    print(f'Новый клиент добавлен c id: {cur.fetchone()[0]}')


@logger
def add_phone_number(conn, client_id, phone_number):
    cur.execute("""
        INSERT INTO phone_number(client_id, phone_number) VALUES(%s, %s);""",
                (client_id, phone_number))
    conn.commit()
    cur.execute("""
        SELECT first_name, last_name FROM client AS cl JOIN phone_number AS pn
        ON cl.client_id = pn.client_id WHERE cl.client_id=%s;""",
                (client_id,))
    print(f'Номер телефона для клиента {cur.fetchone()[1]} добавлен.')


@logger
def change_client(conn, client_id, first_name=None, last_name=None, email=None):
    cur.execute("""
        SELECT * FROM client WHERE client_id=%s;""",
                (client_id,))
    client = cur.fetchone()
    if first_name is None:
        first_name = client[1]
    if last_name is None:
        last_name = client[2]
    if email is None:
        email = client[3]
    cur.execute("""
        UPDATE client SET first_name=%s, last_name=%s, email=%s WHERE client_id=%s;""",
                (first_name, last_name, email, client_id))
    print(f'Данные клиента {last_name} изменены.')


@logger
def delete_phone(conn, client_id, phone_number):
    cur.execute("""
        SELECT EXISTS(SELECT * FROM client WHERE client_id=%s);""",
                (client_id,))
    client = cur.fetchone()[0]
    if client is False:
        print('Такого клиента в базе нет.')
    else:
        cur.execute("""
            DELETE FROM phone_number WHERE phone_number=%s;""",
                    (phone_number,))
        print(f'Телефон {phone_number} удален из базы.')


@logger
def delete_client(conn, client_id):
    cur.execute("""
        DELETE FROM phone_number WHERE client_id=%s;""",
                (client_id,))
    cur.execute("""
        DELETE FROM client WHERE client_id=%s;""",
                (client_id,))
    conn.commit()
    print('Все данные о клиенте удалены.')


@logger
def find_client(conn, first_name=None, last_name=None, email=None, phone_number=None):
    if first_name is None:
        first_name = '%'
    else:
        first_name = '%' + first_name + '%'
    if last_name is None:
        last_name = '%'
    else:
        last_name = '%' + last_name + '%'
    if email is None:
        email = '%'
    else:
        email = '%' + email + '%'
    if phone_number is None:
        cur.execute("""
            SELECT client_id, first_name, last_name, email FROM client WHERE first_name LIKE %s
            AND last_name LIKE %s AND email LIKE %s;""",
                    (first_name, last_name, email))
    else:
        cur.execute("""
            SELECT cl.client_id, cl.first_name, cl.last_name, cl.email FROM client AS cl JOIN phone_number AS pn 
            ON cl.client_id = pn.client_id
            WHERE cl.first_name LIKE %s AND cl.last_name LIKE %s AND cl.email LIKE %s AND pn.phone_number LIKE %s;""",
                    (first_name, last_name, email, phone_number))
    print(cur.fetchall())
