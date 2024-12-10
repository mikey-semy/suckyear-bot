import sys
print("Python path:")
print("\n".join(sys.path))

print("\nTrying import:")
from backend.shared.models.base import SQLModel
print("Import successful!")