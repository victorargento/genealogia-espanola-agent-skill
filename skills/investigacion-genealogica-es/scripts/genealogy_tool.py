#!/usr/bin/env python3
"""Validate genealogy JSON and export/validate GEDCOM 5.5.1."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path


STATUSES = {"documented", "testimony", "inferred", "hypothesis", "rejected"}
MONTHS = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
LINE = re.compile(r"(\d+) (?:@([^@]+)@ )?([A-Z0-9_]+)(?: (.*))?")
POINTER_TYPES = {"FAMC": "FAM", "FAMS": "FAM", "HUSB": "INDI", "WIFE": "INDI", "CHIL": "INDI", "SOUR": "SOUR"}


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def exact_date(event: dict) -> date | None:
    if not event.get("date"):
        return None
    precision = event.get("precision", "exact")
    value = event["date"]
    if precision in {"year", "about"}:
        if not re.fullmatch(r"[0-9]{4}", str(value)) or not 1 <= int(value) <= 9999:
            raise ValueError(f"Año inválido: {value}")
        return None
    if precision == "month":
        date.fromisoformat(value + "-01")
        return None
    if precision != "exact":
        raise ValueError(f"Precisión no admitida: {precision}")
    try:
        return date.fromisoformat(event["date"])
    except ValueError as exc:
        raise AssertionError(f"Fecha exacta inválida: {event['date']}") from exc


def validate_model(data: dict, public: bool = False) -> dict:
    assert data.get("version") == 1, "La versión debe ser 1"
    people_list = data.get("people", [])
    family_list = data.get("families", [])
    source_list = data.get("sources", [])
    people = {item["id"]: item for item in people_list}
    families = {item["id"]: item for item in family_list}
    sources = {item["id"]: item for item in source_list}
    assert len(people) == len(people_list), "ID de persona duplicado"
    assert len(families) == len(family_list), "ID de familia duplicado"
    assert len(sources) == len(source_list), "ID de fuente duplicado"

    source_refs: set[str] = set()
    births: dict[str, date] = {}
    for person_id, person in people.items():
        assert person.get("given_names") or person.get("surnames"), f"Nombre vacío: {person_id}"
        if public:
            assert person.get("living") is False, f"Estado vital no publicable: {person_id}"
        for event in person.get("events", []):
            assert event.get("status", "documented") in STATUSES, f"Estado inválido en {person_id}"
            source_refs.update(event.get("source_ids", []))
            parsed = exact_date(event)
            if event.get("type") == "birth" and parsed:
                births[person_id] = parsed

    parent_family: dict[str, str] = {}
    edges = {person_id: [] for person_id in people}
    for family_id, family in families.items():
        assert family.get("status", "documented") in STATUSES, f"Estado inválido en {family_id}"
        partners = family.get("partners", [])
        assert 1 <= len(partners) <= 2, f"Parejas inválidas: {family_id}"
        assert len(set(partners)) == len(partners), f"Pareja repetida: {family_id}"
        for partner_id in partners:
            assert partner_id in people, f"Pareja inexistente: {partner_id}"
        for child_id in family.get("children", []):
            assert child_id in people, f"Hijo inexistente: {child_id}"
            assert child_id not in partners, f"Autoparentesco: {family_id}"
            assert child_id not in parent_family, f"Dos familias parentales: {child_id}"
            parent_family[child_id] = family_id
            for partner_id in partners:
                edges[partner_id].append(child_id)
                if partner_id in births and child_id in births:
                    age = (births[child_id] - births[partner_id]).days / 365.2425
                    assert 12 <= age <= 80, f"Cronología parental improbable: {partner_id} -> {child_id}"
        source_refs.update(family.get("source_ids", []))
        for event in family.get("events", []):
            assert event.get("status", "documented") in STATUSES, f"Estado inválido en {family_id}"
            source_refs.update(event.get("source_ids", []))
            exact_date(event)

    def visit(person_id: str, stack: set[str]) -> None:
        assert person_id not in stack, f"Ciclo de ascendencia: {person_id}"
        for child_id in edges[person_id]:
            visit(child_id, stack | {person_id})

    for person_id in people:
        visit(person_id, set())
    missing = sorted(source_refs - sources.keys())
    assert not missing, "Fuentes inexistentes: " + ", ".join(missing)
    return {"status": "OK", "people": len(people), "families": len(families), "sources": len(sources), "public_mode": public}


def clean(value: object) -> str:
    return " ".join(str(value).replace("\r", " ").replace("\n", " ").split())


def ged_date(event: dict) -> str:
    value = event["date"]
    precision = event.get("precision", "exact")
    if precision == "exact":
        year, month, day = value.split("-")
        return f"{int(day)} {MONTHS[int(month) - 1]} {year}"
    if precision == "month":
        year, month = value.split("-")
        return f"{MONTHS[int(month) - 1]} {year}"
    if precision == "year":
        return value
    if precision == "about":
        return "ABT " + value
    raise AssertionError(f"Precisión no admitida: {precision}")


def append_event(lines: list[str], event: dict, source_map: dict[str, str]) -> None:
    tag = {"birth": "BIRT", "death": "DEAT", "marriage": "MARR"}.get(event.get("type"))
    if not tag:
        raise ValueError(f"Evento no soportado por esta versión: {event.get('type')}. No se exporta para evitar pérdida silenciosa.")
    lines.append(f"1 {tag}")
    if event.get("date"):
        lines.append(f"2 DATE {ged_date(event)}")
    if event.get("place"):
        lines.append(f"2 PLAC {clean(event['place'])}")
    status = event.get("status", "documented")
    if status != "documented":
        lines.append(f"2 NOTE Estado de evidencia: {status}")
    for source_id in event.get("source_ids", []):
        lines.append(f"2 SOUR @{source_map[source_id]}@")


def export_gedcom(data: dict) -> str:
    validate_model(data)
    if data.get("hypotheses"):
        raise ValueError("Esta versión no exporta hypotheses: conserva el modelo y prepara una vista revisada explícita.")
    people, families, sources = data["people"], data["families"], data["sources"]
    person_map = {item["id"]: f"I{index}" for index, item in enumerate(people, 1)}
    family_map = {item["id"]: f"F{index}" for index, item in enumerate(families, 1)}
    source_map = {item["id"]: f"S{index}" for index, item in enumerate(sources, 1)}
    child_of: dict[str, str] = {}
    partner_of = {item["id"]: [] for item in people}
    person_lookup = {item["id"]: item for item in people}
    for family in families:
        for child_id in family.get("children", []):
            child_of[child_id] = family["id"]
        for partner_id in family.get("partners", []):
            partner_of[partner_id].append(family["id"])

    lines = ["0 HEAD", "1 SOUR GENEALOGIA-ES-AGENT", "1 GEDC", "2 VERS 5.5.1", "2 FORM LINEAGE-LINKED", "1 CHAR UTF-8"]
    for person in people:
        lines.extend([f"0 @{person_map[person['id']]}@ INDI", f"1 NAME {clean(person.get('given_names', ''))} /{clean(person.get('surnames', ''))}/"])
        if person.get("sex") in {"M", "F", "X", "U"}:
            lines.append(f"1 SEX {'U' if person['sex'] == 'X' else person['sex']}")
            if person['sex'] == 'X':
                lines.append("1 NOTE Valor de sexo en el modelo original: X")
        for event in person.get("events", []):
            append_event(lines, event, source_map)
        if person["id"] in child_of:
            lines.append(f"1 FAMC @{family_map[child_of[person['id']]]}@")
        for family_id in partner_of[person["id"]]:
            lines.append(f"1 FAMS @{family_map[family_id]}@")

    for family in families:
        lines.append(f"0 @{family_map[family['id']]}@ FAM")
        partners = family.get("partners", [])
        used: set[str] = set()
        for partner_id in partners:
            sex = person_lookup[partner_id].get("sex")
            tag = "WIFE" if sex == "F" and "WIFE" not in used else "HUSB" if "HUSB" not in used else "WIFE"
            used.add(tag)
            lines.append(f"1 {tag} @{person_map[partner_id]}@")
        for child_id in family.get("children", []):
            lines.append(f"1 CHIL @{person_map[child_id]}@")
        for event in family.get("events", []):
            append_event(lines, event, source_map)
        for source_id in family.get("source_ids", []):
            lines.append(f"1 SOUR @{source_map[source_id]}@")
        status = family.get("status", "documented")
        if status != "documented":
            lines.append(f"1 NOTE Estado de evidencia: {status}")

    for source in sources:
        lines.extend([f"0 @{source_map[source['id']]}@ SOUR", f"1 TITL {clean(source['title'])}"])
        if source.get("repository"):
            lines.append(f"1 NOTE Repositorio: {clean(source['repository'])}")
        if source.get("citation"):
            lines.append(f"1 NOTE Cita: {clean(source['citation'])}")
        if source.get("url"):
            lines.append(f"1 NOTE URL: {clean(source['url'])}")
    lines.append("0 TRLR")
    return "\n".join(lines) + "\n"


def validate_gedcom(path: Path) -> dict:
    raw = path.read_bytes()
    lines = raw.decode("utf-8").splitlines()
    assert lines and lines[0] == "0 HEAD" and lines[-1] == "0 TRLR", "Cabecera o cierre GEDCOM inválido"
    records: dict[str, str] = {}
    pointers: list[tuple[str, str, int]] = []
    individual_links: set[tuple[str, str, str]] = set()
    family_links: set[tuple[str, str, str]] = set()
    current_id: str | None = None
    current_type: str | None = None
    previous = 0
    for number, line in enumerate(lines, 1):
        assert len(line.encode("utf-8")) <= 255, f"Línea demasiado larga: {number}"
        match = LINE.fullmatch(line)
        assert match, f"Sintaxis GEDCOM inválida: línea {number}"
        level, xref, tag, value = int(match.group(1)), match.group(2), match.group(3), match.group(4) or ""
        assert level <= previous + 1, f"Salto de nivel: línea {number}"
        previous = level
        if level == 0 and xref:
            assert xref not in records, f"ID GEDCOM repetido: {xref}"
            records[xref] = tag
            current_id, current_type = xref, tag
        if tag in POINTER_TYPES and value.startswith("@") and value.endswith("@"):
            target = value.strip("@")
            pointers.append((tag, target, number))
            if current_type == "INDI" and current_id and level == 1 and tag in {"FAMS", "FAMC"}:
                individual_links.add((current_id, tag, target))
            if current_type == "FAM" and current_id and level == 1 and tag in {"HUSB", "WIFE", "CHIL"}:
                role = "FAMC" if tag == "CHIL" else "FAMS"
                family_links.add((target, role, current_id))
    for tag, target, number in pointers:
        assert target in records, f"Referencia inexistente: línea {number}"
        assert records[target] == POINTER_TYPES[tag], f"Tipo de referencia incorrecto: línea {number}"
    assert individual_links == family_links, "Los enlaces INDI/FAM no son recíprocos"
    return {"status": "OK", "format": "GEDCOM 5.5.1 UTF-8", "records": len(records), "references": len(pointers), "reciprocal_family_links": True, "lines": len(lines), "bytes": len(raw)}


def write_atomic(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(content, encoding="utf-8", newline="\n")
    try:
        validate_gedcom(temporary)
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)


def main() -> None:
    if not __debug__:
        raise SystemExit("Ejecuta sin -O: esta versión necesita las comprobaciones de validación activas.")
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    validate_parser = sub.add_parser("validate")
    validate_parser.add_argument("input", type=Path)
    validate_parser.add_argument("--public", action="store_true")
    export_parser = sub.add_parser("export")
    export_parser.add_argument("input", type=Path)
    export_parser.add_argument("output", type=Path)
    public_export_parser = sub.add_parser("export-public")
    public_export_parser.add_argument("input", type=Path)
    public_export_parser.add_argument("output", type=Path)
    gedcom_parser = sub.add_parser("validate-gedcom")
    gedcom_parser.add_argument("input", type=Path)
    args = parser.parse_args()
    try:
        if args.command == "validate":
            result = validate_model(read_json(args.input), args.public)
        elif args.command in {"export", "export-public"}:
            data = read_json(args.input)
            if args.command == "export-public":
                validate_model(data, public=True)
            output = export_gedcom(data)
            write_atomic(args.output, output)
            result = {"status": "OK", "mode": "public" if args.command == "export-public" else "private", "output": str(args.output), "bytes": len(output.encode("utf-8"))}
        else:
            result = validate_gedcom(args.input)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except (AssertionError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "ERROR", "error": str(exc)}, ensure_ascii=False, indent=2), file=sys.stderr)
        raise SystemExit(1) from None


if __name__ == "__main__":
    main()
