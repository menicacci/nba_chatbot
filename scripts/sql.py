import sqlite3
import pandas as pd
import random


def execute(data_path: str, command: str):
    connection = sqlite3.connect(data_path)
    cursor = connection.cursor()

    cursor.execute(command)

    connection.commit()
    connection.close()


def get_query_output(data_path: str, command: str):
    # Check if the command is a valid selection query
    if not sql_command.strip().lower().startswith("select"):
        return False
    
    try:
        connection = sqlite3.connect(data_path)

        df = pd.read_sql_query(command, connection)

        connection.close()

        return df
    
    except sqlite3.Error as e:
        print("SQLite error:", e)
        return False
    except Exception as e:
        print("Error:", e)
        return False


def find_min_none_instance(table_instances, num_elements):
    random.shuffle(table_instances)
    instances_sorted = sorted(table_instances, key=lambda instance: sum(1 for value in instance if value is None or value == ""))
    return instances_sorted[:num_elements]


def print_db_structure(data_path: str, num_examples: int):
    connection = sqlite3.connect(data_path)
    cursor = connection.cursor()

    cursor.execute("SELECT name, sql FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    output = []

    for table in tables:
        table_name = table[0]
        table_sql = table[1]

        cursor.execute(f"SELECT * FROM {table_name} ORDER BY RANDOM() LIMIT 1000;")
        random_instances = cursor.fetchall()

        examples = find_min_none_instance(random_instances, num_examples)

        output.append("Table:\n")
        output.append(table_sql)
        output.append("\nExamples:\n")
        for example in examples:
            output.append(str(example))
            output.append("\n")
        output.append("\n")

    connection.close()

    output_str = "".join(output)
    print(output_str)
    return output_str


def remove_tables(data_path: str, tables_to_remove: list):
    connection = sqlite3.connect(data_path)
    cursor = connection.cursor()

    remove_command = "DROP TABLE IF EXISTS {table};"

    for table in tables_to_remove:
        cursor.execute(remove_command.format(table=table))

    connection.commit()
    connection.close()


def create_db_from_csv(data_path: str, csv_paths: list):
    conn = sqlite3.connect(data_path)
    
    for csv_path, table_name in csv_paths:
        df = pd.read_csv(csv_path)
        df.to_sql(table_name, conn, index=False)

    conn.commit()
    conn.close()
