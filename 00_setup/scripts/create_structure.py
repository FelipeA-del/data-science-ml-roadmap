from pathlib import Path
STRUCTURE = {
    "00_setup": ["scripts", "notebooks"],
    "01_python_for_data": ["notebooks", "scripts", "exercises", "tests", "data"],
    "02_pandas_numpy": ["notebooks", "scripts", "exercises", "data"],
    "03_visualization": ["notebooks", "scripts", "exercises", "data"],
    "04_statistics": ["notebooks", "scripts", "exercises"],
    "05_machine_learning": ["notebooks", "scripts", "exercises", "models", "data"],
    "06_projects": ["eda_project", "ml_project"],
    "07_mlops": ["notebooks", "scripts"],
}

def create_structure(base_path: Path) -> None:
    """Crea la estructura completa de carpetas del roadmap.
    
    Args:
        base_path: Carpeta raíz donde se creará todo.
    """
    for module, subfolders in STRUCTURE.items():
        for folder in subfolders:
            path = base_path / module / folder
            path.mkdir(parents=True, exist_ok=True)
            readme = path / "README.md"
            if not readme.exists():
                readme.write_text(f"# {module} / {folder}\n")
    print("✅ Estructura creada correctamente")
if __name__ == "__main__":
    create_structure(Path("."))