#!/usr/bin/env python
# scripts/clacs_core.py
from __future__ import annotations
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import json
import math
import hashlib

# --------------------------------
# Rutas base
# --------------------------------

REGISTRO_DIR = Path("registro")
PROJECT_PATH = REGISTRO_DIR / "clacs_project.json"


# --------------------------------
# Modelos de datos
# --------------------------------

@dataclass
class Dimension:
    name: str           # p.ej. "L"
    label: str          # p.ej. "Límbico"
    description: str    # explicación


@dataclass
class Artefact:
    id: str
    name: str
    kind: str           # "texto", "pintura", etc.
    raw_path: str       # ruta bruta opcional
    notes: str
    scores_raw: Dict[str, int]    # por dimensión
    vector: List[float]           # vector normalizado (norma 1)


@dataclass
class Field:
    prototype_ids: List[str]
    vector: List[float]           # vector de campo (norma 1)


@dataclass
class ProjectConfig:
    project_name: str
    scale_max: int
    dimensions: List[Dimension]
    artefacts: List[Artefact]
    field: Optional[Field] = None

    def to_json(self) -> dict:
        return {
            "project_name": self.project_name,
            "scale_max": self.scale_max,
            "dimensions": [asdict(d) for d in self.dimensions],
            "artefacts": [asdict(a) for a in self.artefacts],
            "field": asdict(self.field) if self.field is not None else None,
        }

    @staticmethod
    def from_json(data: dict) -> "ProjectConfig":
        dims = [Dimension(**d) for d in data["dimensions"]]
        artefacts = [Artefact(**a) for a in data.get("artefacts", [])]
        field_data = data.get("field")
        field = Field(**field_data) if field_data else None
        return ProjectConfig(
            project_name=data["project_name"],
            scale_max=data["scale_max"],
            dimensions=dims,
            artefacts=artefacts,
            field=field,
        )


# --------------------------------
# Carga/guardado de proyecto
# --------------------------------

def load_project_config(allow_missing: bool = False) -> Optional[ProjectConfig]:
    """
    Carga registro/clacs_project.json.
    - Si allow_missing=True y no existe, devuelve None.
    - Si allow_missing=False y no existe, lanza FileNotFoundError.
    """
    if not PROJECT_PATH.exists():
        if allow_missing:
            return None
        raise FileNotFoundError(
            f"No se encontró {PROJECT_PATH}. "
            "Inicializa el proyecto con clacs_hilbert_cli.py."
        )
    with PROJECT_PATH.open("r", encoding="utf-8") as f:
        data = json.load(f)
    return ProjectConfig.from_json(data)


def save_project_config(cfg: ProjectConfig) -> None:
    REGISTRO_DIR.mkdir(parents=True, exist_ok=True)
    with PROJECT_PATH.open("w", encoding="utf-8") as f:
        json.dump(cfg.to_json(), f, ensure_ascii=False, indent=2)


# --------------------------------
# Helpers de vectores y campo
# --------------------------------

def normalize_vector(coords: List[float]) -> List[float]:
    norm_sq = sum(c * c for c in coords)
    if norm_sq == 0:
        raise ValueError("Vector de longitud cero; revisa tus puntuaciones.")
    norm = math.sqrt(norm_sq)
    return [c / norm for c in coords]


def compute_artefact_vector(
    scores_raw: Dict[str, int],
    dim_order: List[str],
    scale_max: int,
) -> List[float]:
    """
    Convierte puntuaciones enteras 0..scale_max en un vector normalizado (norma 1).
    """
    coords: List[float] = []
    for dim in dim_order:
        raw = scores_raw.get(dim, 0)
        coords.append(raw / float(scale_max))
    return normalize_vector(coords)


def compute_field_vector(cfg: ProjectConfig, prototype_ids: List[str]) -> List[float]:
    """
    Calcula vector de campo Φ_S como suma normalizada de vectores de prototipos.
    """
    dim_order = [d.name for d in cfg.dimensions]
    vectors: List[List[float]] = []
    for pid in prototype_ids:
        art = next((a for a in cfg.artefacts if a.id == pid), None)
        if art is None:
            raise ValueError(f"Artefacto prototipo '{pid}' no encontrado.")
        if len(art.vector) != len(dim_order):
            raise ValueError(f"Dimensiones inconsistentes en artefacto '{pid}'.")
        vectors.append(art.vector)
    if not vectors:
        raise ValueError("No se proporcionaron prototipos para el campo.")
    summed = [0.0] * len(dim_order)
    for v in vectors:
        for i, c in enumerate(v):
            summed[i] += c
    return normalize_vector(summed)


def compute_phi(cfg: ProjectConfig, artefact_id: str) -> float:
    """
    Calcula Φ_CLACS(e | campo actual) = max(0, dot(v_e, Φ_S))^2, redondeado a 4 decimales.
    """
    if cfg.field is None:
        raise ValueError("El campo aún no ha sido definido en clacs_project.json.")

    art = next((a for a in cfg.artefacts if a.id == artefact_id), None)
    if art is None:
        raise ValueError(f"Artefacto '{artefact_id}' no encontrado en clacs_project.json.")

    if len(art.vector) != len(cfg.field.vector):
        raise ValueError("Dimensiones inconsistentes entre artefacto y campo.")

    amplitude = sum(a * b for a, b in zip(art.vector, cfg.field.vector))
    amplitude = max(0.0, amplitude)
    phi = amplitude * amplitude
    return round(phi, 4)


# --------------------------------
# YAML front-matter (simple)
# --------------------------------

def parse_yaml_front_matter(text: str) -> Tuple[Optional[Dict[str, object]], str]:
    """
    Si el texto comienza con un bloque YAML entre '---' y '---',
    devuelve (dict, cuerpo). Si no, devuelve (None, texto completo).

    Es un parser simple: claves, valores escalares y listas tipo:
      key:
        - item
        - item2
    """
    lines = text.splitlines(keepends=True)
    if not lines or not lines[0].strip().startswith("---"):
        return None, text

    yaml_lines: List[str] = []
    i = 1
    while i < len(lines):
        if lines[i].strip().startswith("---"):
            i += 1
            break
        yaml_lines.append(lines[i])
        i += 1

    yaml_text = "".join(yaml_lines)
    body_text = "".join(lines[i:])

    yaml_data: Dict[str, object] = {}
    # primera pasada: claves y valores escalares
    for raw_line in yaml_text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            continue
        key, val = line.split(":", 1)
        key = key.strip()
        val = val.strip()
        if val == "":
            yaml_data[key] = []
        else:
            try:
                if "." in val:
                    yaml_data[key] = float(val)
                else:
                    yaml_data[key] = int(val)
            except ValueError:
                yaml_data[key] = val
    # segunda pasada: listas
    if yaml_text:
        current_key: Optional[str] = None
        for raw_line in yaml_text.splitlines():
            stripped = raw_line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            if ":" in stripped:
                key, val = stripped.split(":", 1)
                key = key.strip()
                val = val.strip()
                if val == "" and key in yaml_data and isinstance(yaml_data[key], list):
                    current_key = key
                else:
                    current_key = None
            elif stripped.startswith("- ") and current_key is not None:
                item = stripped[2:].strip()
                yaml_data[current_key].append(item)

    return yaml_data, body_text


def dump_yaml_front_matter(data: Dict[str, object]) -> str:
    """
    Serialización minimalista de dict -> YAML front-matter.
    """
    lines: List[str] = ["---\n"]
    for key, val in data.items():
        if isinstance(val, list):
            lines.append(f"{key}:\n")
            for item in val:
                lines.append(f"  - {item}\n")
        else:
            lines.append(f"{key}: {val}\n")
    lines.append("---\n")
    return "".join(lines)


# --------------------------------
# Hash10 sobre cuerpo
# --------------------------------

def compute_hash10_from_body(body: str) -> str:
    """
    Calcula hash10 = primeros 10 caracteres de SHA256(cuerpo).
    El cuerpo es el texto después del YAML.
    """
    h = hashlib.sha256()
    h.update(body.encode("utf-8"))
    return h.hexdigest()[:10]
