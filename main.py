import psycopg2
from psycopg2 import sql

def commit(func):
    def wrapper(*args, **kwargs):
        connection = None
        cursor = None
        try:
            connection = psycopg2.connect(
                dbname="test",
                user="postgres",
                password="Amir1029",
                host="localhost",
                port="5432"
            )
            cursor = connection.cursor()
            result = func(cursor, *args, **kwargs)
            connection.commit()
            return result
        except Exception as e:
            if connection:
                connection.rollback()
            print(f"An error occurred: {e}")
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
    return wrapper

class UsernameField:
    def __init__(self):
        self._value = None

    def __get__(self, instance, owner):
        return self._value

    def __set__(self, instance, value):
        if not value:
            raise ValueError("Username cannot be empty.")
        if not isinstance(value, str):
            raise ValueError("Username must be a string.")
        self._value = value

class PasswordField:
    def __init__(self):
        self._value = None

    def __get__(self, instance, owner):
        return self._value

    def __set__(self, instance, value):
        if len(value) <= 8:
            raise ValueError("Password must be 8 characters long.")
        self._value = value

class PhoneField:
    def __init__(self):
        self._value = None

    def __get__(self, instance, owner):
        return self._value

    def __set__(self, instance, value):
        if not value.startswith("+998"):
            raise ValueError("Phone number must start with +998")
        self._value = value

class User:
    username = UsernameField()
    password = PasswordField()
    phone = PhoneField()

    def __init__(self, username, password, phone):
        self.username = username
        self.password = password
        self.phone = phone

    @commit
    def save_to_db(cursor, self):
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(100) NOT NULL,
                password VARCHAR(100) NOT NULL,
                phone VARCHAR(20) NOT NULL
            );
            """
        )
        cursor.execute(
            sql.SQL("""
            INSERT INTO users (username, password, phone)
            VALUES (%s, %s, %s)
            """).format(),
            (self.username, self.password, self.phone)
        )
        print("User saved successfully!")

if __name__ == "__main__":
    try:
        user = User("john_doe", "12345678", "+9981234567")
        user.save_to_db()
    except ValueError as e:
        print(e)
