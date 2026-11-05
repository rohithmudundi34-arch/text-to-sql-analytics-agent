from src.langgraph_agent import run_langgraph_agent


question = "Show the total revenue for each product category."

print("=" * 60)
print("LANGGRAPH TEXT-TO-SQL AGENT")
print("=" * 60)

print("\nQuestion:")
print(question)


result = run_langgraph_agent(question)


print("\n" + "=" * 60)
print("GENERATED SQL")
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