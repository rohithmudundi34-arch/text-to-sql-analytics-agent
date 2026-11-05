from src.langgraph_agent import (
    build_graph,
    get_schema
)


question = "What are the top 5 products by revenue?"

schema = get_schema()

bad_sql = """
SELECT
    p.product_name,
    SUM(p.price * s.quantity * (1 - s.discount)) AS total_revenue
FROM products p
JOIN sales s
    ON p.product_id = s.product_id
GROUP BY p.product_name
ORDER BY wrong_column DESC
LIMIT 5;
"""


initial_state = {
    "question": question,
    "schema": schema,
    "sql": bad_sql,
    "data": None,
    "error": None,
    "attempts": 0,
    "success": False
}


app = build_graph()


print("=" * 60)
print("LANGGRAPH SELF-CORRECTION TEST")
print("=" * 60)


print("\nInitial SQL:")
print(bad_sql)


result = app.invoke(initial_state)


print("\n" + "=" * 60)
print("FINAL SQL")
print("=" * 60)

print(result["sql"])


print("\n" + "=" * 60)
print("RESULT")
print("=" * 60)

if result["success"]:

    print(result["data"])

else:

    print("ERROR:")
    print(result["error"])


print("\n" + "=" * 60)
print("ATTEMPTS")
print("=" * 60)

print(result["attempts"])