import sqlite3

connection = sqlite3.connect('company_staff_members.db')

sql = connection.cursor()

sql.execute('''CREATE TABLE IF NOT EXISTS company_staff_members (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               user_unique_id TEXT NOT NULL,
               first_name TEXT NOT NULL,
               last_name TEXT NOT NULL,
               email_address TEXT NOT NULL,
               phone_number TEXT NOT NULL);''')

connection.commit()
connection.close()


def add_new_staff_member(user_data):
    connection = sqlite3.connect('company_staff_members.db')
    sql = connection.cursor()
    add_new_staff = sql.execute('''INSERT INTO company_staff_members (user_unique_id, first_name, last_name,
     email_address, phone_number) VALUES (?, ?, ?, ?, ?)''', (user_data['user_unique_id'],
                                                              user_data['first_name'],
                                                              user_data['last_name'],
                                                              user_data['email_address'],
                                                              user_data['phone_number']))
    connection.commit()
    connection.close()
    return add_new_staff


def check_staff_id(staff_unique_id_number):
    connection = sqlite3.connect('company_staff_members.db')
    sql = connection.cursor()
    check_id = sql.execute('''SELECT * from company_staff_members WHERE user_unique_id = ?''',
                           (staff_unique_id_number,)).fetchone()
    connection.commit()
    connection.close()
    return check_id


def delete_staff_member(staff_unique_id_number):
    connection = sqlite3.connect('company_staff_members.db')
    sql = connection.cursor()
    delete_staff = sql.execute('''DELETE FROM company_staff_members WHERE user_unique_id = ?''',
                               (staff_unique_id_number,))
    connection.commit()
    connection.close()
    return delete_staff



