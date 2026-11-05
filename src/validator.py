import re


FORBIDDEN_KEYWORDS = [
    "INSERT",
    "UPDATE",
    "DELETE",
    "DROP",
    "ALTER",
    "CREATE",
    "TRUNCATE",
    "REPLACE",
    "ATTACH",
    "DETACH"
]


def validate_sql(sql):

    sql = sql.strip()

    if not sql:
        return False, "SQL query is empty."

    upper_sql = sql.upper()

    # Only SELECT / WITH
    if not (
        upper_sql.startswith("SELECT")
        or upper_sql.startswith("WITH")
    ):
        return False, "Only SELECT queries are allowed."

    # Dangerous operations
    for keyword in FORBIDDEN_KEYWORDS:

        pattern = rf"\b{keyword}\b"

        if re.search(pattern, upper_sql):

            return (
                False,
                f"Forbidden SQL operation: {keyword}"
            )

    # Multiple statements
    if ";" in sql[:-1]:

        return (
            False,
            "Multiple SQL statements are not allowed."
        )

    return True, "SQL is valid."