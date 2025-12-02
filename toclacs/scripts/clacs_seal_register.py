#!/usr/bin/env python
# scripts/clacs_seal_registry.py

from __future__ import annotations
from pathlib import Path
from datetime import datetime
import json
import sys

from clacs_core import (
    load_project_config,
    compute_phi,
    parse_yaml_front_matter,
    compute_hash10_from_body,
)


REGISTRO_DIR = Path("registro")
REGISTRO_PATH = REGISTRO_DIR / "clacs_registro.jsonl"


def append_to_registro(entry: dict) -> None:
    REGISTRO_DIR.mkdir(parents=True, exist_ok=True)
    with REGISTRO_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def seal_file(path: Path) -> None:
    cfg = load_project_config()
    if not path.exists():
        raise FileNotFoundError(f"Archivo no encontrado: {path}")

    raw_text = path.read_text(encoding="utf-8")
    yaml_data, body = parse_yaml_front_matter(raw_text)
    if yaml_data is None:
        raise ValueError("El archivo no contiene YAML front-matter; primero audítalo.")

    required_fields = ["id", "sesion_id", "campo_id", "phi_clacs", "dimensiones", "hash10"]
    missing = [k for k in required_fields if k not in yaml_data]
    if missing:
        raise ValueError(f"Faltan campos obligatorios en YAML: {', '.join(missing)}")

    artefact_id = str(yaml_data["id"])
    yaml_phi = float(yaml_data["phi_clacs"])
    yaml_hash10 = str(yaml_data["hash10"])

    # Verificar hash10
    computed_hash10 = compute_hash10_from_body(body)
    if computed_hash10 != yaml_hash10:
        raise ValueError(
            f"hash10 inconsistente para {path}.\n"
            f"  YAML: {yaml_hash10}\n"
            f"  Computado: {computed_hash10}"
        )

    # Verificar Φ_CLACS (tolerancia pequeña)
    computed_phi = compute_phi(cfg, artefact_id)
    if abs(computed_phi - yaml_phi) > 1e-4:
        raise ValueError(
            f"Φ_CLACS inconsistente para artefacto {artefact_id}.\n"
            f"  YAML: {yaml_phi}\n"
            f"  Computado: {computed_phi}"
        )

    now_iso = datetime.now().isoformat(timespec="seconds")
    sesion_id = str(yaml_data["sesion_id"])
    campo_id = str(yaml_data["campo_id"])
    dimensiones = yaml_data.get("dimensiones", [])
    tipo = str(yaml_data.get("tipo", "texto"))

    nombre = path.name
    es_testigo = bool(yaml_phi > 0.95)
    testigo_id = None  # se puede actualizar después

    entry = {
        "artefact_id": artefact_id,
        "nombre": nombre,
        "tipo": tipo,
        "sesion_id": sesion_id,
        "campo_id": campo_id,
        "phi_clacs": yaml_phi,
        "dimensiones": dimensiones,
        "hash10": yaml_hash10,
        "ruta_fruto": str(path.as_posix()),
        "timestamp_registro": now_iso,
        "es_testigo": es_testigo,
        "testigo_id": testigo_id,
    }

    append_to_registro(entry)
    print(f"\nFruto sellado en {REGISTRO_PATH}:")
    print(json.dumps(entry, ensure_ascii=False, indent=2))


def main():
    if len(sys.argv) < 2:
        print("Uso: python scripts/clacs_seal_registry.py RUTA_AL_ARCHIVO.md")
        sys.exit(1)
    path = Path(sys.argv[1])
    try:
        seal_file(path)
    except Exception as e:
        print(f"Error durante el sellado: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
