import nbformat
import os

notebook_path = "a.ipynb"
python_script_path = "a.py"

with open(notebook_path, "r", encoding="utf-8") as f:
    nb = nbformat.read(f, as_version=4)

script_lines = []
for cell in nb.cells:
    if cell.cell_type == "code":
        script_lines.append("\n".join(cell.source.splitlines()))
        script_lines.append("\n\n")  # 셀 간의 구분을 위해 개행 추가

with open(python_script_path, "w", encoding="utf-8") as f:
    f.writelines(script_lines)
