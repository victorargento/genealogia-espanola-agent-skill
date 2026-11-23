#!/usr/bin/env python3
"""Run an isolated installation and end-to-end fixture simulation."""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from install_skill import REPOSITORY_ROOT, SKILL_NAME, install


SIMULATION_ROOT = REPOSITORY_ROOT / "work" / "simulacion-instalacion"


def digest_tree(path: Path) -> str:
    digest = hashlib.sha256()
    for file in sorted(item for item in path.rglob("*") if item.is_file() and "__pycache__" not in item.parts and item.suffix != ".pyc"):
        digest.update(file.relative_to(path).as_posix().encode("utf-8"))
        digest.update(file.read_bytes())
    return digest.hexdigest()


def main() -> None:
    global SIMULATION_ROOT
    (REPOSITORY_ROOT / "work").mkdir(exist_ok=True)
    SIMULATION_ROOT = Path(tempfile.mkdtemp(prefix="simulacion-", dir=REPOSITORY_ROOT / "work"))
    resolved = SIMULATION_ROOT.resolve()
    expected_parent = (REPOSITORY_ROOT / "work").resolve()
    if expected_parent not in resolved.parents:
        raise RuntimeError("La simulación debe permanecer dentro de work/")

    installed = install("both", "project", SIMULATION_ROOT)
    codex_skill = SIMULATION_ROOT / ".agents" / "skills" / SKILL_NAME
    claude_skill = SIMULATION_ROOT / ".claude" / "skills" / SKILL_NAME
    canonical = REPOSITORY_ROOT / "skills" / SKILL_NAME
    hashes = {
        "canonical": digest_tree(canonical),
        "codex": digest_tree(codex_skill),
        "claude": digest_tree(claude_skill),
    }
    assert len(set(hashes.values())) == 1, "Las instalaciones no son idénticas a la skill canónica"

    fixture = REPOSITORY_ROOT / "examples" / "familia-ficticia.json"
    tool = codex_skill / "scripts" / "genealogy_tool.py"
    output = SIMULATION_ROOT / "resultado" / "familia-ficticia.ged"
    output.parent.mkdir(parents=True)
    def run_tool(*arguments: str) -> dict:
        completed = subprocess.run(
            [sys.executable, str(tool), *arguments],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        return json.loads(completed.stdout)

    tree_result = run_tool("validate", str(fixture), "--public")
    export_result = run_tool("export-public", str(fixture), str(output))
    gedcom_result = run_tool("validate-gedcom", str(output))
    original_digest = hashlib.sha256(output.read_bytes()).hexdigest()
    negative_fixture = REPOSITORY_ROOT / "examples" / "persona-estado-desconocido.json"
    rejected = subprocess.run(
        [sys.executable, str(tool), "export-public", str(negative_fixture), str(output)],
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    assert rejected.returncode != 0, "La exportación pública aceptó un estado vital desconocido"
    rejected_result = json.loads(rejected.stderr)
    assert rejected_result["status"] == "ERROR"
    assert "Estado vital no publicable" in rejected_result["error"]
    assert hashlib.sha256(output.read_bytes()).hexdigest() == original_digest, (
        "Una exportación pública rechazada modificó el GEDCOM existente"
    )

    request = SIMULATION_ROOT / "SOLICITUD-USUARIO.md"
    request.write_text(
        "# Solicitud ficticia\n\n"
        "Investiga esta familia española sin unir homónimos por el nombre. "
        "Distingue documentos de hipótesis y prepara un GEDCOM público.\n",
        encoding="utf-8",
    )
    report = {
        "status": "OK",
        "simulation_root": str(SIMULATION_ROOT),
        "installed": installed,
        "identical_skill_hash": hashes["canonical"],
        "tree_validation": tree_result,
        "export": export_result,
        "gedcom_validation": gedcom_result,
        "rejected_unknown_living_status": rejected_result,
        "atomic_output_preserved_after_rejection": True,
        "privacy_check": "OK: el fixture solo contiene personas ficticias marcadas como fallecidas",
        "limits": [
            "Comprueba instalación, archivos, validación y exportación.",
            "No ejecuta una sesión real de Codex o Claude ni prueba el disparo implícito del modelo."
        ],
    }
    report_path = SIMULATION_ROOT / "RESULTADO.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    json.dump(report, sys.stdout, ensure_ascii=False, indent=2)
    print()


if __name__ == "__main__":
    main()
