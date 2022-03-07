from pathlib import Path

print(Path(__file__).parent.parent)
print(Path(__file__).resolve())
# print(Path(__file__) == Path(__file__).resolve())