from src.agent import run_agent


question = "Show monthly sales revenue."
print("\n")
print("=" * 60)
print("QUESTION")
print("=" * 60)

print(question)


print("\n")
print("=" * 60)
print("RUNNING AGENT")
print("=" * 60)


result = run_agent(question)


print("\n")
print("=" * 60)
print("GENERATED SQL")
print("=" * 60)

print(result["sql"])


if result["success"]:

    print("\n")
    print("=" * 60)
    print("RESULT")
    print("=" * 60)

    print(result["data"])

else:

    print("\n")
    print("=" * 60)
    print("ERROR")
    print("=" * 60)

    print(result["error"])


print("\n")
print("=" * 60)
print("ATTEMPTS")
print("=" * 60)

print(len(result["attempts"]) + 1)