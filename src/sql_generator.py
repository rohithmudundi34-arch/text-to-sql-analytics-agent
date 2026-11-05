from .llm import get_llm


SQL_PROMPT = """
You are an expert SQLite data analyst.

Convert the user's business question into
a valid SQLite SQL query.

DATABASE SCHEMA:
{schema}

USER QUESTION:
{question}

RULES:

1. Generate ONLY SQLite-compatible SQL.

2. Only use tables and columns from the schema.

3. Never invent tables.

4. Never invent columns.

5. Only generate SELECT or WITH queries.

6. Never generate:
   INSERT
   UPDATE
   DELETE
   DROP
   ALTER
   CREATE
   TRUNCATE

7. Use JOIN when required.

8. Revenue means:

   products.price
   * sales.quantity
   * (1 - sales.discount)

9. Use meaningful column aliases.

10. Return ONLY SQL.

11. Do not use markdown.

12. Do not explain the query.
"""


def generate_sql(question, schema):

    llm = get_llm()

    prompt = SQL_PROMPT.format(
        schema=schema,
        question=question
    )

    response = llm.invoke(prompt)

    sql = response.content.strip()

    # Remove markdown if model adds it
    sql = sql.replace("```sql", "")
    sql = sql.replace("```", "")

    return sql.strip()