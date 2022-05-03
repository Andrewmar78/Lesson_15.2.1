CREATE TABLE IF NOT EXISTS breeds
--Создание таблицы пород животных
(
id integer primary key AUTOINCREMENT,
breed varchar(40)
);

INSERT INTO breeds (breed)
--Заполнение таблицы пород животных
SELECT DISTINCT breed FROM animals
WHERE breed IS NOT NULL
ORDER BY breed ASC

--CREATE TABLE IF NOT EXISTS colors
--"""Создание таблицы окраски животного"""
--(
--id integer primary key AUTOINCREMENT,
--color varchar(20) CONSTRAINT non_color DEFAULT "no color"
--);
--
--INSERT INTO colors (color)
--"""Заполнение таблицы окраски животного"""
--SELECT DISTINCT * FROM
--(
--SELECT DISTINCT color1 as color FROM animals
--UNION ALL
--SELECT DISTINCT color2 as color FROM animals
--)
--WHERE color IS NOT NULL
--ORDER BY color ASC


CREATE TABLE IF NOT EXISTS all_colors
--Создание таблицы расцветок животного
(
id integer primary key AUTOINCREMENT,
color1 varchar(30),
color2 varchar(30) CONSTRAINT non_color DEFAULT "no color"
)

INSERT INTO all_colors (color1, color2)
SELECT DISTINCT animals.color1, animals.color2
FROM animals


CREATE TABLE IF NOT EXISTS outcome
--Создание таблицы outcome
(
id integer primary key AUTOINCREMENT,
subtype varchar(20),
"type" varchar(20),
"month" INTEGER NOT NULL CONSTRAINT ck_month CHECK("month" between 1 and 12),
"year" INTEGER NOT NULL CONSTRAINT ck_year CHECK("year" between 2000 and 2100)
)

INSERT INTO outcome (subtype, "type", "month", "year")
--Заполнение таблицы outcome
SELECT DISTINCT animals.outcome_subtype,
animals.outcome_type,
animals.outcome_month,
animals.outcome_year
FROM animals


CREATE TABLE IF NOT EXISTS animals_new
--Создание нормализованной основной таблицы
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

INSERT INTO animals_new (age_upon_outcome, animal_id, name, date_of_birth,
--Заполнение нормализованной основной таблицы
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