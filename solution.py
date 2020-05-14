from pathlib import Path
from typing import List

from sqlalchemy import text
from ..utils import Services, get_summary
from ..resources import db


def resource_text(name: str):
    resource_name = "files/" + name
    return (Path(__file__).parent / Path(resource_name)).read_text()


def create_analysis_table():
    with db.engine.connect() as connection:

        # Optional: If you'd like to use user-defined functions, include them here, with
        # one function per file.
        create_udfs(connection, [
            "example_udf.sql"
        ])

        # Write some sql files, place them in the resources dir,
        # and include them in these functions to execute.

        executed_query = connection.execute(resource_text("sql_query.sql")).fetchall()

        results = [Services(record[0], record[1], record[2], record[3], record[4])
                   for record in executed_query]
        code_dict = get_summary(results)
        for code, age_bracket_dict in code_dict.items():
            for age_bracket, patient_list in age_bracket_dict.items():
                insert_statement = f"INSERT INTO SQL_SOLUTION VALUES ('{code}', '{age_bracket}', {len(set(patient_list))});"
                connection.execute(insert_statement)


def create_udfs(connection, udf_list):
    """ Create UDFs, if you'd like. One udf per file!"""
    for filename in udf_list:
        statement = resource_text(filename)
        connection.execute(text(statement))


def execute_sql_files(connection, sql_files):
    """ Execute a set of SQL files. Files may contain multiple statements."""
    for filename in sql_files:
        statement = resource_text(filename)
        for sub_statement in statement.split(";"):
            if sub_statement.strip():
                connection.execute(text(sub_statement))
