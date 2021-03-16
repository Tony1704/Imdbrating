# Module Imports
import mariadb
import sys
import geheim


class DataBase:
    # Connect to MariaDB Platform
    def __init__(self):
        try:
            self.conn = mariadb.connect(
                user="root",
                password=geheim.pw,
                host="localhost",
                port=3306,
                database="imdb"

            )
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)

        # Get Cursor
        self.cur = self.conn.cursor()

    def get_person_by_id(self, id):
        cur = self.cur
        cur.execute(
            "SELECT * FROM person WHERE nconst=?",
            (id,))
        for line in cur:
            return line

    def get_all_person_id(self):
        cur = self.cur
        cur.execute(
            "SELECT distinct person.nconst FROM person inner join titleprincipals on person.nconst = "
            "titleprincipals.nconst INNER JOIN valid_movies ON valid_movies.tconst = titleprincipals.tconst "
        )
        query = []
        for line in cur:
            query.append(line[0])
        return query

    def get_person_by_name(self, name):
        cur = self.cur
        cur.execute(
            "SELECT * FROM person WHERE primaryName=?",
            (name,))
        for line in cur:
            return line

    def get_person_id_by_name(self, name):
        cur = self.cur
        cur.execute(
            "SELECT nconst FROM person WHERE primaryName=?",
            (name,))
        for line in cur:
            return line

    def get_top_rated_movies(self):
        cur = self.cur
        cur.execute(
            "SELECT * FROM imdb.top_rated_movies LIMIT 40",
            ())
        query = []
        for line in cur:
            query.append(line)
        return query

    def get_valid_movies(self):
        cur = self.cur
        cur.execute(
            "SELECT * FROM imdb.valid_movies",
            ())
        query = []
        for line in cur:
            query.append(line)
        return query

    def get_crew_of_movie(self, tconst):
        cur = self.cur
        cur.execute(
            "select titleprincipals.nconst,titleprincipals.ordering,titleprincipals.category from titleprincipals where "
            "titleprincipals.tconst=? order by titleprincipals.ordering",
            (tconst,))
        query = []
        for line in cur:
            query.append(line)
        return query

    def show_tables(self):
        """Retrieves the list of tables from the database"""

        table_list = []

        # Retrieve Contacts
        self.cur.execute("SHOW TABLES")

        for (table,) in self.cur.fetchall():
            table_list.append(table)

        return table_list

    # Get field info from cursor
    def get_field_info(self, cur):
        """Retrieves the field info associated with a cursor"""

        field_info = mariadb.fieldinfo()

        field_info_text = []

        # Retrieve Column Information
        for column in cur.description:
            column_name = column[0]
            column_type = field_info.type(column)
            column_flags = field_info.flag(column)

            field_info_text.append(f"{column_name}: {column_type} {column_flags}")

        return field_info_text

    # Get field info from cursor
    def get_table_field_info(self, table):
        """Retrieves the field info associated with a table"""

        # Fetch Table Information
        self.cur.execute(f"SELECT * FROM {table} LIMIT 1")

        field_info_text = self.get_field_info(self.cur)

        return field_info_text

    def sql(self, statement):
        self.cur.execute(statement)
        query = []
        for line in self.cur:
            query.append(line)
        return query

    # select nconst,ordering,category,t.tconst,startYear,averageRating from titlebasic inner join titleratings on titleratings.tconst = titlebasic.tconst inner join titleprincipals t on titlebasic.tconst = t.tconst where titlebasic.titleType = 'movie' and titleratings.numVotes > 50000

    def closeConnection(self):
        self.conn.close()
