import sqlite3

def create_connection():
    connection = None
    try:
        connection = sqlite3.connect('crud_example.db')
        print("Connection to SQLite DB successful")
    except sqlite3.Error as e:
        print(f"The error '{e}' occurred")
    return connection

def create_table(connection):
    create_users_table = """
    CREATE TABLE IF NOT EXISTS users (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT NOT NULL,
      age INTEGER,
      gender TEXT,
      nationality TEXT
    );
    """
    try:
        cursor = connection.cursor()
        cursor.execute(create_users_table)
        print("Table created successfully")
    except sqlite3.Error as e:
        print(f"The error '{e}' occurred")

def create_user(connection, user):
    sql = '''
    INSERT INTO users (name, age, gender, nationality)
    VALUES (?, ?, ?, ?)
    '''
    cursor = connection.cursor()
    cursor.execute(sql, user)
    connection.commit()
    return cursor.lastrowid

def read_users(connection):
    sql = "SELECT * FROM users"
    try:
        cursor = connection.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        return rows
    except sqlite3.Error as e:
        print(f"The error '{e}' occurred")
        return []

def update_user(connection, user_id, new_name, new_age):
    sql = '''
    UPDATE users
    SET name = ?, age = ? 
    WHERE id = ?
    '''
    cursor = connection.cursor()
    cursor.execute(sql, (new_name, new_age, user_id))
    connection.commit()

def delete_user(connection, user_id):
    sql = '''
    DELETE FROM users
    WHERE id = ?
    '''
    cursor = connection.cursor()
    cursor.execute(sql, (user_id,))
    connection.commit()

def menu():
    connection = create_connection()
    create_table(connection)

    while True:
        print("\nMenu:")
        print("1. Create User")
        print("2. Read Users")
        print("3. Update User")
        print("4. Delete User")
        print("5. Exit")
        
        choice = input("Enter choice: ")

        if choice == "1":
            name = input("Enter name: ")
            age = int(input("Enter age: "))
            gender = input("Enter gender (Male/Female): ")
            nationality = input("Enter nationality: ")
            new_user = (name, age, gender, nationality)
            user_id = create_user(connection, new_user)
            print(f"User created with id: {user_id}")

        elif choice == "2":
            users = read_users(connection)
            if users:
                for user in users:
                    print(user)
            else:
                print("No users found or an error occurred")

        elif choice == "3":
            user_id = int(input("Enter user id to update: "))
            new_name = str(input("Enter new name:"))
            new_age = int(input("Enter new age: "))
            update_user(connection, user_id, new_name, new_age)
            print(f"Updated user with id: {user_id}")

        elif choice == "4":
            user_id = int(input("Enter user id to delete: "))
            delete_user(connection, user_id)
            print(f"Deleted user with id: {user_id}")

        elif choice == "5":
            print("Exiting...")
            connection.close()
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    menu()
