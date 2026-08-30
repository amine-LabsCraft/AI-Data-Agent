import psycopg2
from psycopg2 import sql


class DatabaseUtil:
    def __init__(self, db_config):
        self.db_config = db_config
        try:
            self.connection = psycopg2.connect(**db_config)
        except Exception as e:
            print(f"Error connecting to the database: {e}")
            self.connection = None

    def schema_details(self, schema_name):
        schema_info_context = f"Database Schema: {schema_name}\n"
 
        connection = self.connection
        cursor = None

        if connection is None:
            return "Error fetching schema details: no active database connection."

        try:
            cursor = connection.cursor()

            cursor.execute("SELECT table_name from information_schema.tables where table_schema = %s;", (schema_name,))
            tables_list = cursor.fetchall()
            for table in tables_list:
                table_name = table[0]
                schema_info_context = f"{schema_info_context}\nTable: {table_name}\n"

                # Adding Columns & Data Types
                cursor.execute("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = %s;", (table_name,))
                columns_list = cursor.fetchall()
                for column in columns_list:
                    column_name = column[0]
                    data_type = column[1]
                    schema_info_context = f"{schema_info_context}  Column: {column_name}, Data Type: {data_type}\n"

                # Adding Sample Data (identifiants paramétrés via sql.Identifier, pas de f-string SQL)
                query = sql.SQL("SELECT * FROM {}.{} LIMIT 5;").format(
                    sql.Identifier(schema_name),
                    sql.Identifier(table_name)
                )
                cursor.execute(query)
                sample_data = cursor.fetchall()
                schema_info_context = f"{schema_info_context}  Sample Data:\n"
                for row in sample_data:
                    schema_info_context = f"{schema_info_context}    {row}\n"

        except Exception as e:
            print(f"Error fetching schema details: {e}")
            schema_info_context = f"Error fetching schema details: {e}"

        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

        return schema_info_context

    def execute_sql(self, query):
        connection = self.connection
        cursor = None

        if connection is None:
            return "Error executing query: no active database connection."

        try:
            cursor = connection.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            connection.commit()
            return str(result)
        except Exception as e:
            print(f"Error executing query: {e}")
            return f"Error executing query: {e}"
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()


if __name__ == "__main__":
    obj = DatabaseUtil({
        "host": "localhost",
        "port": 5432,
        "user": "postgres",
        "password": "Amine5050&",
        "dbname": "postgres"
    })
    result = obj.schema_details("public")
    with open("test_schema_details.txt", "w") as f:
        f.write(result)