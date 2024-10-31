import psycopg2
from psycopg2 import sql


class PostgreClient:
    def __init__(self):
        pass

    def insert_data_to_postgresql(self, value: dict, table_name: str="sensor_table"):
        connection = None
        cursor     = None
        try:
            connection = psycopg2.connect(
                dbname="sensors",
                user="new_user",
                password="pswd",
                host="localhost",
                port="5432"
            )
            # Create a cursor object
            cursor = connection.cursor()

            # Create a placeholder string for the values
            data = list(value.values())
            placeholders = ', '.join(['%s'] * len(data))

            # SQL query to insert data
            insert_query = sql.SQL("INSERT INTO {table} (column1, column2) VALUES ({placeholders})").format(
                table=sql.Identifier(table_name),
                placeholders=sql.SQL(placeholders)
            )


            # Execute the SQL query
            cursor.execute(insert_query, data)
            
            # Commit the transaction
            connection.commit()

            print(f"Inserted value {data} into {table_name}")

        except Exception as error:
            print(f"Error while inserting data: {error}")

        finally:
            # Close the cursor and connection
            if connection:
                connection.close()
            if cursor:
                cursor.close()
