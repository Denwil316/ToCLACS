#!/usr/bin/env python
# scripts/clacs_hilbert_cli.py

from __future__ import annotations
from pathlib import Path
from typing import List, Dict
import sys

from clacs_core import (
    Dimension,
    Artefact,
    Field,
    ProjectConfig,
    load_project_config,
    save_project_config,
    compute_artefact_vector,
    compute_field_vector,
    compute_phi,
)


# -----------------------------
# Helpers de CLI
# -----------------------------

def prompt_yes_no(msg: str) -> bool:
    while True:
        ans = input(msg + " [s/n]: ").strip().lower()
        if ans in ("s", "si", "sí", "y", "yes"):
            return True
        if ans in ("n", "no"):
            return False
        print("Por favor responde 's' o 'n'.")


# -----------------------------
# Inicialización de proyecto
# -----------------------------

def init_project_interactive() -> ProjectConfig:
    print("\n=== Inicialización de proyecto CLACS–Hilbert ===")
    name = input("Nombre del proyecto (p.ej. 'T-CLACS sesión 2025'): ").strip()
    while True:
        try:
            scale_max = int(input("Valor máximo de la escala por dimensión (sugerido: 4): ").strip())
            if scale_max <= 0:
                raise ValueError
            break
        except ValueError:
            print("Por favor ingresa un entero positivo (por ejemplo 4).")

    print("\nDefine las dimensiones de tu espacio (puedes empezar con 3: L, A, E).")
    dims: List[Dimension] = []
    idx = 1
    while True:
        print(f"\nDimensión #{idx}:")
        name_short = input("  Nombre corto (sin espacios, p.ej. 'L'): ").strip()
        label = input("  Etiqueta humana (p.ej. 'Límbico'): ").strip()
        desc = input("  Descripción breve de lo que mide esta dimensión: ").strip()
        if not name_short:
            print("  El nombre corto no puede estar vacío.")
            continue
        dims.append(Dimension(name=name_short, label=label or name_short, description=desc))
        idx += 1
        if not prompt_yes_no("¿Añadir otra dimensión?"):
            break

    cfg = ProjectConfig(
        project_name=name or "Proyecto CLACS",
        scale_max=scale_max,
        dimensions=dims,
        artefacts=[],
        field=None,
    )
    return cfg


# -----------------------------
# Funciones de listado/manejo
# -----------------------------

def list_dimensions(cfg: ProjectConfig) -> None:
    print("\nDimensiones definidas:")
    for d in cfg.dimensions:
        print(f"  - {d.name} ({d.label}): {d.description}")


def list_artefacts(cfg: ProjectConfig) -> None:
    if not cfg.artefacts:
        print("\nAún no hay artefactos registrados.")
        return
    print("\nArtefactos registrados:")
    for a in cfg.artefacts:
        dims_str = ", ".join(f"{k}={v}" for k, v in a.scores_raw.items())
        print(f"  - id={a.id} | {a.name} [{a.kind}] | puntajes: {dims_str}")


def add_artefact_interactive(cfg: ProjectConfig) -> None:
    print("\n=== Nuevo artefacto ===")
    art_id = input("ID corto para el artefacto (sin espacios, p.ej. 'e1'): ").strip()
    if any(a.id == art_id for a in cfg.artefacts):
        print(f"Ya existe un artefacto con id '{art_id}'.")
        return
    name = input("Nombre o título descriptivo: ").strip()
    kind = input("Tipo (p.ej. 'texto', 'pintura', 'escultura'): ").strip() or "arte"
    raw_path = input("Ruta al archivo bruto (opcional, puedes dejar vacío): ").strip()
    notes = input("Notas breves sobre este artefacto (contexto, fecha, etc.): ").strip()

    print("\nAhora asigna puntuaciones enteras para cada dimensión.")
    print(f"Escala: 0 = nada / ausente, {cfg.scale_max} = máximo en esta dimensión.")
    scores_raw: Dict[str, int] = {}
    for d in cfg.dimensions:
        while True:
            try:
                val = int(input(f"  {d.name} ({d.label}): ").strip())
                if not (0 <= val <= cfg.scale_max):
                    raise ValueError
                scores_raw[d.name] = val
                break
            except ValueError:
                print(f"    Ingresa un entero entre 0 y {cfg.scale_max}.")

    dim_order = [d.name for d in cfg.dimensions]
    vector = compute_artefact_vector(scores_raw, dim_order, cfg.scale_max)

    art = Artefact(
        id=art_id,
        name=name or art_id,
        kind=kind,
        raw_path=raw_path,
        notes=notes,
        scores_raw=scores_raw,
        vector=vector,
    )
    cfg.artefacts.append(art)

    print(f"\nArtefacto '{art.id}' registrado con vector normalizado:")
    print("  v =", " ".join(f"{x:.4f}" for x in vector))


def define_field_interactive(cfg: ProjectConfig) -> None:
    if not cfg.artefacts:
        print("Primero necesitas registrar al menos un artefacto.")
        return
    list_artefacts(cfg)
    print("\nDefine el campo seleccionando los IDs de artefactos prototipo.")
    print("Estos deberían ser ejemplos MUY representativos del campo CLACS que quieres medir.")
    ids_str = input("IDs de prototipos separados por coma (p.ej. 'e1,e2,e3'): ").strip()
    if not ids_str:
        print("No se proporcionaron IDs.")
        return
    prototype_ids = [s.strip() for s in ids_str.split(",") if s.strip()]
    try:
        vector = compute_field_vector(cfg, prototype_ids)
    except ValueError as e:
        print(f"Error al calcular el campo: {e}")
        return
    cfg.field = Field(prototype_ids=prototype_ids, vector=vector)
    print("\nCampo definido con éxito.")
    print("Vector de campo Φ_S (normalizado):")
    print("  Φ_S =", " ".join(f"{x:.4f}" for x in vector))
    print("Prototipos usados:", ", ".join(prototype_ids))


def compute_phi_interactive(cfg: ProjectConfig) -> None:
    if cfg.field is None:
        print("Primero debes definir el campo seleccionando prototipos.")
        return
    list_artefacts(cfg)
    art_id = input("\nID del artefacto para calcular Φ_CLACS: ").strip()
    try:
        phi_val = compute_phi(cfg, art_id)
    except ValueError as e:
        print(f"Error: {e}")
        return
    print(f"\nΦ_CLACS({art_id} | campo actual) = {phi_val:.4f}")
    # Interpretación cualitativa
    if phi_val < 0.1:
        label = "ruido / externo al campo"
    elif phi_val < 0.3:
        label = "periférico / tangencial"
    elif phi_val < 0.6:
        label = "relacionado / resonancia moderada"
    elif phi_val < 0.85:
        label = "núcleo del campo"
    else:
        label = "canónico / casi núcleo del campo"
    print(f"Interpretación cualitativa: {label}")


# -----------------------------
# Main
# -----------------------------

def main():
    cfg = load_project_config(allow_missing=True)
    if cfg is None:
        print("No se encontró configuración previa.")
        if prompt_yes_no("¿Quieres crear un nuevo proyecto CLACS ahora?"):
            cfg = init_project_interactive()
            save_project_config(cfg)
            print("\nProyecto creado y guardado en registro/clacs_project.json.")
        else:
            print("Saliendo.")
            return

    while True:
        print("\n=== Menú CLACS–Hilbert ===")
        print(f"Proyecto: {cfg.project_name}")
        print("1) Ver dimensiones")
        print("2) Añadir artefacto")
        print("3) Listar artefactos")
        print("4) Definir / redefinir campo (prototipos)")
        print("5) Calcular Φ_CLACS para un artefacto")
        print("6) Guardar y salir")
        choice = input("Elige una opción [1-6]: ").strip()
        if choice == "1":
            list_dimensions(cfg)
        elif choice == "2":
            add_artefact_interactive(cfg)
        elif choice == "3":
            list_artefacts(cfg)
        elif choice == "4":
            define_field_interactive(cfg)
        elif choice == "5":
            compute_phi_interactive(cfg)
        elif choice == "6":
            save_project_config(cfg)
            print("Configuración guardada en registro/clacs_project.json. Hasta luego.")
            break
        else:
            print("Opción no válida. Intenta de nuevo.")


if __name__ == "__main__":
    main()
