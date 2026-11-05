from .database import (
    get_schema,
    execute_query
)

from .sql_generator import (
    generate_sql
)

from .validator import (
    validate_sql
)

from .llm import get_llm, response_to_text


CORRECTION_PROMPT = """
You are an expert SQLite SQL debugger.

DATABASE SCHEMA:
{schema}

USER QUESTION:
{question}

FAILED SQL:
{sql}

DATABASE ERROR:
{error}

Generate a corrected SQLite SQL query.

RULES:

1. Only SELECT or WITH.

2. Use only tables and columns
   present in the schema.

3. Do not invent columns.

4. Do not invent tables.

5. Do not modify the database.

6. Return ONLY SQL.

7. Do not use markdown.
"""


def correct_sql(
    question,
    sql,
    error,
    schema
):

    llm = get_llm()

    prompt = CORRECTION_PROMPT.format(
        schema=schema,
        question=question,
        sql=sql,
        error=error
    )

    response = llm.invoke(prompt)

    corrected_sql = response_to_text(response)

    corrected_sql = corrected_sql.replace(
        "```sql",
        ""
    )

    corrected_sql = corrected_sql.replace(
        "```",
        ""
    )

    return corrected_sql.strip()


def run_agent(
    question,
    max_retries=3
):

    schema = get_schema()

    # ---------------------------------
    # Generate SQL
    # ---------------------------------

    sql = generate_sql(
        question,
        schema
    )

    attempts = []

    # ---------------------------------
    # Retry Loop
    # ---------------------------------

    for attempt in range(
        max_retries + 1
    ):

        # Validate
        valid, message = validate_sql(
            sql
        )

        if not valid:

            attempts.append({
                "attempt": attempt + 1,
                "sql": sql,
                "error": message
            })

            if attempt < max_retries:

                sql = correct_sql(
                    question,
                    sql,
                    message,
                    schema
                )

                continue

            return {
                "success": False,
                "sql": sql,
                "data": None,
                "attempts": attempts,
                "error": message
            }

        # Execute
        df, error = execute_query(
            sql
        )

        # Successful
        if error is None:

            return {
                "success": True,
                "sql": sql,
                "data": df,
                "attempts": attempts,
                "error": None
            }

        # SQL execution error
        attempts.append({
            "attempt": attempt + 1,
            "sql": sql,
            "error": error
        })

        # Self correction
        if attempt < max_retries:

            sql = correct_sql(
                question,
                sql,
                error,
                schema
            )

    return {
        "success": False,
        "sql": sql,
        "data": None,
        "attempts": attempts,
        "error": "Maximum retry limit reached."
    }