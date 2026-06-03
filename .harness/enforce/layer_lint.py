import ast, sys
from pathlib import Path

LAYER_DEPS = {
    "types": [], "config": ["types"], "repo": ["types", "config"],
    "service": ["types", "config", "repo"], "runtime": ["types", "config", "service"]
}

def check():
    errors = []
    for f in Path("src").rglob("*.py"):
        if f.name == "__init__.py": continue
        try:
            tree = ast.parse(f.read_text())
            layer = f.parts[f.parts.index("src")+1]
            allowed = LAYER_DEPS.get(layer, [])
            for node in ast.walk(tree):
                if isinstance(node, ast.ImportFrom) and node.module:
                    imported = node.module.split(".")[0]
                    if imported in LAYER_DEPS and imported not in allowed:
                        errors.append(f"❌ {layer} → {imported} (not allowed)")
        except: pass
    if errors:
        print("\n".join(errors)); sys.exit(1)
    print("✅ Architecture clean")

if __name__ == "__main__":
    check()
