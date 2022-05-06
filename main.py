import sqlite3
from configure import path
from flask import Flask, jsonify, render_template

app = Flask(__name__)


def db_connection(qwery, params=""):
    """Соединение с базой данных"""
    try:
        with sqlite3.connect(path) as connection:
            cursor = connection.cursor()
            cursor.execute(qwery, params)
            result = cursor.fetchall()
            return result
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite:", error)


def create_breeds_table():
    """Создание таблицы пород животного"""
    qwery = """
    CREATE TABLE IF NOT EXISTS breeds
    (
    id integer primary key AUTOINCREMENT,
    breed varchar(40)
    )
    """
    print(db_connection(qwery))


def fulfill_breeds_table():
    """Заполнение таблицы пород животного"""
    qwery = """
    INSERT INTO breeds (breed)
    SELECT DISTINCT breed FROM animals
    WHERE breed IS NOT NULL
    ORDER BY breed ASC 
    """
    print(db_connection(qwery))


def create_colors_table():
    """Создание таблицы расцветок животного"""
    qwery = """
    CREATE TABLE IF NOT EXISTS all_colors
    (
    id integer primary key AUTOINCREMENT,
    color1 varchar(30),
    color2 varchar(30) CONSTRAINT non_color DEFAULT "no color"
    )
    """
    print(db_connection(qwery))


def fulfill_colors_table():
    """Заполнение таблицы расцветок животного"""
    qwery = """
    INSERT INTO all_colors (color1, color2)
    SELECT DISTINCT animals.color1, animals.color2
    FROM animals 
    """
    print(db_connection(qwery))


def create_outcome_table():
    """Создание таблицы outcome"""
    qwery = """
    CREATE TABLE IF NOT EXISTS outcome
    (
    id integer primary key AUTOINCREMENT,
    subtype varchar(20),
    "type" varchar(20),
    "month" INTEGER NOT NULL CONSTRAINT ck_month CHECK("month" between 1 and 12),
    "year" INTEGER NOT NULL CONSTRAINT ck_year CHECK("year" between 2000 and 2100)
    )
    """
    print(db_connection(qwery))


def fulfill_outcome_table():
    """Заполнение таблицы outcome"""
    qwery = """
    INSERT INTO outcome (subtype, "type", "month", "year")
    SELECT DISTINCT animals.outcome_subtype,
    animals.outcome_type,
    animals.outcome_month,
    animals.outcome_year
    FROM animals
    """
    print(db_connection(qwery))


def create_main_table():
    """Создание основной таблицы"""
    qwery = """
    CREATE TABLE IF NOT EXISTS animals_new
    (
    "index" INTEGER primary key AUTOINCREMENT,
    age_upon_outcome varchar(10),
    animal_id varchar(10),
    name varchar(40) CONSTRAINT no_name DEFAULT "no name",
    date_of_birth date,
    animal_type varchar(20),
    breed_id integer,
    outcome_id integer,
    colors_id integer,
    FOREIGN KEY (outcome_id) REFERENCES outcome(id),
    FOREIGN KEY (colors_id) REFERENCES all_colors(id),
    FOREIGN KEY (breed_id) REFERENCES breeds(id)
    )
    """
    print(db_connection(qwery))


def fulfill_main_table():
    """Заполнение основной таблицы"""
    qwery = """
    INSERT INTO animals_new (age_upon_outcome, animal_id, name, date_of_birth,
    animal_type, breed_id, outcome_id, colors_id)
    SELECT animals.age_upon_outcome, animals.animal_id, animals.name, animals.date_of_birth,
    animals.animal_type, breeds.id, outcome.id, all_colors.id
    FROM animals
    LEFT JOIN all_colors ON all_colors.color1 = animals.color1
    AND all_colors.color2 = animals.color2
    LEFT JOIN outcome ON outcome.subtype = animals.outcome_subtype
    AND outcome."type" = animals.outcome_type
    AND outcome."month" = animals.outcome_month
    AND outcome."year" = animals.outcome_year
    LEFT JOIN breeds ON breeds.breed = animals.breed
    """
    print(db_connection(qwery))


def choose_by_animal_id(itemid):
    """Выбор животного по его ID"""
    qwery = """
    SELECT age_upon_outcome, animal_id, name, date_of_birth, animal_type, breed, color1, color2, subtype,
    "type", "month", "year"
    FROM animals_new
    LEFT JOIN all_colors ON all_colors.id = animals_new.colors_id
    LEFT JOIN breeds ON breeds.id = animals_new.breed_id
    LEFT JOIN outcome ON outcome.id = animals_new.outcome_id
    WHERE animals_new.animal_id = :itemid    
    """

    print(db_connection(qwery, {'itemid': itemid}))

    response = db_connection(qwery, {'itemid': itemid})[0]
    response_json = {
        "age_upon_outcome": response[0],
        "animal_id": response[1],
        "name": response[2],
        "date_of_birth": response[3],
        "animal_type": response[4],
        "breed": response[5],
        "color1": response[6],
        "color2": response[7],
        "outcome_subtype": response[8],
        "outcome_type": response[9],
        "outcome_month": response[10],
        "outcome_year": response[11],
    }
    return response_json


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['DEBUG'] = True


@app.route("/<itemid>")
def search_by_animal_item(itemid):
    """Вьюшка страницы поиска по id"""
    try:
        response_json = choose_by_animal_id(itemid)
        return jsonify(response_json)
    except IndexError:
        return "Ошибка IndexError"


if __name__ == '__main__':
    app.run(debug=True)

# Проверки
# create_breeds_table()
# create_colors_table()
# create_outcome_table()
# create_main_table()
# choose_by_animal_id('A678581')
