import psycopg2


def create_db(conn):
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS clients(
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(20),
            last_name VARCHAR(20),
            email VARCHAR(40) NOT NULL)
        """)
    cur.execute("""CREATE TABLE IF NOT EXISTS phones(
            id SERIAL PRIMARY KEY,
            client_id INTEGER NOT NULL REFERENCES clients(id),
            phone VARCHAR(20) NOT NULL)
        """)
    cur.close()

def add_client(conn, first_name, last_name, email, phone=None):
    cur = conn.cursor()
    cur.execute("""INSERT INTO clients(first_name, last_name, email)
    VALUES (%s, %s, %s)
    RETURNING id;""", (first_name, last_name, email))
    client = cur.fetchone()

    if phone is not None:
        cur.execute("""INSERT INTO phones(client_id,phone)
            VALUES (%s, %s)""", (client, phone))

    cur.close()

def add_phone(client_id, phone):
    cur = conn.cursor()
    cur.execute("""UPDATE phones SET phone = %s WHERE id = %s""", (phone, client_id))
    cur.close()

def change_client(id, first_name=None, last_name=None, email=None):
    cur = conn.cursor()
    if first_name:
        cur.execute("""UPDATE clients SET first_name = %s WHERE id = %s""", (first_name, id))


    elif last_name:
        cur.execute("""UPDATE clients SET last_name = %s WHERE id = %s""", (last_name, id))

    elif email:
        cur.execute("""UPDATE clients SET email = %s WHERE id = %s""", (email, id))

    cur.close()


def del_phone (phone):
    cur = conn.cursor()
    cur.execute("""DELETE FROM phones WHERE phone = %s""", (phone,))
    cur.close()

def del_client (id):
    cur = conn.cursor()
    cur.execute("""DELETE FROM clients WHERE id = %s""", (id))
    cur.close()

def find_client(first_name=None, last_name=None, email=None, phone=None):
    cur = conn.cursor()
    if phone is not None:
        cur.execute("""SELECT first_name, last_name, email, phone FROM clients cl
     JOIN phones ph ON ph.client_id = cl.id
     WHERE ph.phone=%s
    """, (phone,))
    else:
        cur.execute("""SELECT first_name, last_name, email, phone
        FROM clients cl
        JOIN phones ph ON ph.client_id = cl.id
        WHERE first_name=%s OR last_name=%s OR email=%s;
                    """, (first_name, last_name, email))
    print(cur.fetchall())

    cur.close()




if __name__ == "__main__":
    with psycopg2.connect(database="", user="", password="") as conn:
        create_db(conn)

        # add_client(conn, 'Иван', 'Иванов', 'ianov@mail.ru', '8-900-332-33-44')
        # add_client(conn, 'Алексей', 'Петров', 'apetr@mail.ru', '8-900-400-99-21')
        # add_client(conn, 'Владимир', 'Сидоров', 'dsidr@mail.ru', '8-900-654-56-32')
        # add_client(conn, 'Светлана', 'Имамдинова', 'imma@mail.ru')

        # add_phone(18, '8-901-765-63-21')

        # change_client('18', '', 'Имамтдинова')

        # find_client('None', 'None', 'None', '8-900-654-56-32')
        # find_client('None', 'Иванов', 'None')
        # find_client('Владимир', 'None', 'None')
        # find_client('None', 'None', 'apetr@mail.ru')

        # del_phone('8-900-332-33-44')

        # del_client('2')

    conn.commit()
    conn.close()
