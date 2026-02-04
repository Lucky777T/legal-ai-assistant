import sys
import importlib

print("="*60)
print("VERIFYING INSTALLATION")
print("="*60)

packages_to_check = [
    ("fastapi", "0.104.1"),
    ("uvicorn", "0.24.0"),
    ("pydantic", "2.5.3"),
    ("numpy", "1.26.4"),
    ("pandas", "2.1.4"),
    ("openai", "1.6.1"),
    ("torch", "2.2.2"),
    ("transformers", "4.35.2"),
    ("sentence_transformers", "2.2.2"),
    ("langchain", "0.1.0"),
]

print(f"Python version: {sys.version}\n")

for pkg, expected_version in packages_to_check:
    try:
        module = importlib.import_module(pkg.replace('-', '_'))
        version = getattr(module, '__version__', getattr(module, 'VERSION', 'N/A'))
        
        if expected_version in str(version):
            print(f"✓ {pkg}: {version}")
        else:
            print(f"⚠ {pkg}: {version} (expected {expected_version})")
    except ImportError as e:
        print(f"✗ {pkg}: NOT INSTALLED ({e})")

print("\n" + "="*60)
print("INSTALLATION STATUS")
print("="*60)