import sqlalchemy

# Не используется в основной программе. Только для создания БД или отчистки
class Base_maker:
    def __init__(self):
        self.db =
        self.engine = sqlalchemy.create_engine(self.db)
        self.connection = self.engine.connect()

    def table_makers(self):
        self.connection.execute("""CREATE TABLE IF NOT EXISTS clients (
		user_id INTEGER PRIMARY KEY);
        """)

        self.connection.execute("""CREATE TABLE IF NOT EXISTS search_reguest (
        Id SERIAL PRIMARY KEY,	
        user_id INTEGER NOT NULL REFERENCES clients(user_id) NOT NULL,
        time_reg VARCHAR(50) NOT NULL,
        target_person_age_from INTEGER,
        target_person_age_to INTEGER,
        target_person_sex INTEGER  NOT NULL,
        target_person_merriage INTEGER NOT NULL,
        target_person_location VARCHAR(200) NOT NULL
        );
        """)

        self.connection.execute("""CREATE TABLE IF NOT EXISTS showed_persons(
        Id SERIAL PRIMARY KEY,
        showed_person_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL REFERENCES clients(user_id) NOT NULL, 
		time_reg VARCHAR(50) NOT NULL,
        favorite_person BOOLEAN DEFAULT FALSE
        );
        """)
    # Удаление таблиц
    def tables_delete(self):
        self.connection.execute("""DROP TABLE IF EXISTS clients CASCADE;""")
        self.connection.execute("""DROP TABLE IF EXISTS showed_persons CASCADE;""")
        self.connection.execute("""DROP TABLE IF EXISTS search_reguest CASCADE;""")
    # Очистка базы
    def tables_clean(self):
        self.connection.execute("""TRUNCATE TABLE IF EXISTS clients CASCADE;""")
        self.connection.execute("""TRUNCATE TABLE IF EXISTS showed_persons CASCADE;""")
        self.connection.execute("""TRUNCATE TABLE IF EXISTS search_reguest CASCADE;""")

# Используется в основной программе
class Base_operator:
    def __init__(self):
        self.db =
        self.engine = sqlalchemy.create_engine(self.db)
        self.connection = self.engine.connect()


    def add_showed_persons(self, user_id, showed_person_id, favorite_person, time_reg):
        # showed_persons
        self.connection.execute(f"""INSERT INTO showed_persons(user_id, 
                                                               time_reg,
                                                               showed_person_id,
                                                               favorite_person) 
                                                        VALUES({user_id},
                                                               {time_reg},
                                                               {showed_person_id},
                                                               {favorite_person});""")
        pass


    def add_search_reguest(self, user_id, time_reg, age_from, age_to, sex, status, hometown):

        self.connection.execute(f"""INSERT INTO search_reguest(user_id,
                                                               time_reg,
                                                               target_person_age_from,
                                                               target_person_age_to,
                                                               target_person_sex,
                                                               target_person_merriage,
                                                               target_person_location)
                                                        VALUES({user_id},
                                                               {time_reg},
                                                               {age_from},
                                                               {age_to},
                                                               {sex},
                                                               {status},
                                                               \'{hometown}\');""") # долбанное бл.. экранирование проглоченных пйтоном кавычек

        pass


    def add_client(self, user_id):
        # clients
        self.connection.execute(f"""INSERT INTO clients(user_id) VALUES({user_id}) ON CONFLICT DO NOTHING;
        """)
        pass

    def find_showed_persons(self, user_id):
        list_id = []
        all = self.connection.execute(f"""SELECT showed_person_id FROM showed_persons 
        WHERE user_id = {user_id};
        """).fetchall()
        for every in all:
            list_id.append(every[0])
        return list_id



if __name__ == '__main__':

    # Base_maker().tables_delete()
    Base_maker().table_makers()


