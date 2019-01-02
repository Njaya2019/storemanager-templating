import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import psycopg2.extras as p_extras

class DataBase():
    
    def __init__(self):
        self.con_nection=psycopg2.connect(dbname='postgres', user='postgres', host='localhost', password=' ')
        self.cursor=self.con_nection.cursor()

 
    def create_database(self):
        try:

            self.cursor.execute("SELECT COUNT(*) = 0 FROM pg_catalog.pg_database WHERE datname = 'store_db'")
            not_exists_row = self.cursor.fetchone()
            not_exists = not_exists_row[0]
            if not_exists:
                self.con_nection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
                self.cursor.execute('CREATE DATABASE store_db')
                return 'database created'
            else:
                return 'database exists'
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if self.con_nection is not None:
                self.con_nection.close()
    def connect_to_store_db(self):
        con=psycopg2.connect(dbname='store_db', user='postgres', host='localhost', password=' ')
        cur=con.cursor(cursor_factory=p_extras.DictCursor)
        return cur, con
    def create_db_tables(self):
        tables=(

            """CREATE TABLE IF NOT EXISTS products(product_id SERIAL PRIMARY KEY,product_name VARCHAR(255)
               NOT NULL,product_price INT NOT NULL,product_qty INT NOT NULL)
            """,

            """CREATE TABLE IF NOT EXISTS sales(sale_id SERIAL PRIMARY KEY,attendant_id INT NOT NULL,
               product_id INT NOT NULL,sale_quantity INT NOT NULL,tnx_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP)
            """,

            """CREATE TABLE IF NOT EXISTS users(userid SERIAL PRIMARY KEY,user_fullname VARCHAR(50) NOT NULL,
               user_email VARCHAR(50) NOT NULL,user_role VARCHAR(50) NOT NULL,user_password TEXT NOT NULL)
            """,
            """
            alter table sales add foreign key (product_id) REFERENCES products(product_id);
            """
           
        )
        try:
            con_values=self.connect_to_store_db()
            cur=con_values[0]
            con=con_values[1]
            # create table one by one
            for table in tables:
                cur.execute(table)
                print('TABLE CREATED')
            # close communication with the PostgreSQL database server
            # commit the changes
            con.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
    
    
    def drop_tables(self):
        drop_tables=""" DROP TABLE IF EXISTS products,sales,users CASCADE;"""
        try:
            self.cursor.execute(drop_tables)
            print('tables droped')
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)