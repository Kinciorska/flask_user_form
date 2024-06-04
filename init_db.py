from settings import connection

cursor = connection.cursor()

cursor.execute('DROP TABLE IF EXISTS user_info;')
cursor.execute('CREATE TABLE user_info (id serial PRIMARY KEY,'
               'username varchar (25) NOT NULL,'
               'first_name varchar (25) NOT NULL,'
               'last_name varchar (25) NOT NULL,'
               'phone varchar (13) NOT NULL,'
               'email varchar (25) NOT NULL,'
               'password varchar (100) NOT NULL);'
               )
connection.commit()

cursor.close()
connection.close()
