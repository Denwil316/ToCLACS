#!/usr/bin/env python
# scripts/clacs_audit_artifact.py
from __future__ import annotations
from pathlib import Path
from datetime import datetime
import sys
from clacs_core import (
    load_project_config,
    compute_phi,
    parse_yaml_front_matter,
    dump_yaml_front_matter,
    compute_hash10_from_body,
)


def audit_file(path: Path) -> None:
    cfg = load_project_config()
    if not path.exists():
        raise FileNotFoundError(f"Archivo no encontrado: {path}")

    artefact_id = input("ID del artefacto en clacs_project.json (ej. e3): ").strip()
    if not artefact_id:
        raise ValueError("ID de artefacto no puede estar vacío.")

    phi_val = compute_phi(cfg, artefact_id)
    print(f"Φ_CLACS({artefact_id}) = {phi_val:.4f}")

    sesion_id = input("sesion_id (ej. 2025-11-26_sesion-001): ").strip()
    campo_id = input("campo_id (ej. S01): ").strip() or "S01"
    tipo = input("tipo de fruto (ej. texto, visual): ").strip() or "texto"

    now_iso = datetime.now().isoformat(timespec="seconds")

    raw_text = path.read_text(encoding="utf-8")
    yaml_data, body = parse_yaml_front_matter(raw_text)

    if yaml_data is None:
        yaml_data = {}

    dim_order = [d.name for d in cfg.dimensions]

    yaml_data.update({
        "id": artefact_id,
        "sesion_id": sesion_id,
        "campo_id": campo_id,
        "phi_clacs": phi_val,
        "dimensiones": dim_order,
        "tipo": tipo,
        "timestamp": now_iso,
    })

    hash10 = compute_hash10_from_body(body)
    yaml_data["hash10"] = hash10

    front = dump_yaml_front_matter(yaml_data)
    # Evitar perder separación si el cuerpo no empieza con salto de línea
    if body and not body.startswith("\n"):
        new_text = front + "\n" + body
    else:
        new_text = front + body

    path.write_text(new_text, encoding="utf-8")

    print(f"\nArchivo auditado y actualizado: {path}")
    print(f"hash10 (cuerpo): {hash10}")


def main():
    if len(sys.argv) < 2:
        print("Uso: python scripts/clacs_audit_artifact.py RUTA_AL_ARCHIVO.md")
        sys.exit(1)
    path = Path(sys.argv[1])
    try:
        audit_file(path)
    except Exception as e:
        print(f"Error durante la auditoría: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
