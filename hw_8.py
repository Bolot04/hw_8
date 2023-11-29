import sqlite3


def create_countries_table(conn):
    conn.execute('''
        CREATE TABLE IF NOT EXISTS countries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL
        )
    ''')

    countries_data = [('Киргизия',), ('Германия',), ('Китай',)]
    conn.executemany('INSERT INTO countries (title) VALUES (?)', countries_data)


def create_cities_table(conn):
    conn.execute('''
        CREATE TABLE IF NOT EXISTS cities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            area REAL DEFAULT 0,
            country_id INTEGER,
            FOREIGN KEY (country_id) REFERENCES countries (id)
        )
    ''')

    cities_data = [
        ('Бишкек', 128.4, 1),
        ('Ош', 87.3, 1),
        ('Берлин', 891.8, 2),
        ('Пекин', 16410.5, 3),
        ('Москва', 2561.5, 0),
        ('Нью-Йорк', 468.9, 0),
    ]
    conn.executemany('INSERT INTO cities (title, area, country_id) VALUES (?, ?, ?)', cities_data)


def create_students_table(conn):
    conn.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            city_id INTEGER,
            FOREIGN KEY (city_id) REFERENCES cities (id)
        )
    ''')

    students_data = [
        ('Иван', 'Иванов', 1),            # 1
        ('Петр', 'Петров', 2),            # 2
        ('Алия', 'Смагулова', 1),         # 3
        ('Екатерина', 'Мюллер', 3),       # 4
        ('John', 'Doe', 4),               # 5
        ('Alice', 'Johnson', 5),          # 6
        ('Bekbolot', 'Bakirov', 1),       # 7
        ('Erbolot', 'Ercinbekov', 2),     # 8
        ('Pasha', 'Omorov', 5),           # 9
        ('Sultan', 'Saburov', 6),         # 10
        ('Nursultan', 'Rakhatov', 3),     # 11
        ('Kairat', 'Tagaybekov', 4),      # 12
        ('Adyl', 'Nikitin', 6),           # 13
        ('Tsoy', 'Pavlov', 5),            # 14
        ('Uuluk', 'Polotov', 2)           # 15
    ]
    conn.executemany('INSERT INTO students (first_name, last_name, city_id) VALUES (?, ?, ?)', students_data)


def display_students_by_city(conn):
    cities = conn.execute('SELECT id, title FROM cities').fetchall()

    while True:
        print(
            "\nВы можете отобразить список учеников по выбранному id города из перечня городов ниже, \nдля выхода из программы введите 0:")
        for city in cities:
            print(f"{city[0]}. {city[1]}")

        city_id = int(input())
        if city_id == 0:
            break


        students_info = conn.execute('''
            SELECT
                students.first_name,
                students.last_name,
                countryes.title AS country,
                cities.title AS city,
                cities.area
            FROM students
            JOIN cities ON students.city_id = cities.id
            LEFT JOIN countries ON cities.country_id = countries.id
            WHERE cities.id = ?
        ''', (city_id,)).fetchall()

        print("\nИнформация о студентах в выбранном городе:")
        for student in students_info:
            country = student[2] if student[2] else 'Не указан!'
            print(f'Имя: {student[0]}, Фамилия: {student[1]}, Страна: {country}, Город: {student[3]}, Площадь города: {student[4]}')

def main():
    connection = sqlite3.connect(':memory:')
    create_countries_table(connection)
    create_cities_table(connection)
    create_students_table(connection)
    display_students_by_city(connection)
    connection.close()

if __name__ == "__main__":
    main()
