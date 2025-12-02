# clacs-hilbert · README

Repositorio de trabajo para la **Teoría del Campo Lingüístico de Alta Coherencia Simbólica (T‑CLACS)** y su implementación operativa basada en un **espacio de Hilbert finito**.

Este repo está pensado para:

* Definir y guardar un **proyecto CLACS** (dimensiones, escala, artefactos).
* Calcular una métrica de **afinidad** (\Phi_{CLACS}) entre artefactos creativos y un **campo simbólico**.
* Auditar frutos textuales, escribiendo **metadatos YAML** y un **hash10** de integridad.
* "Sellar" frutos auditados en un **registro JSONL** (Listado CLACS) verificable.

Todo está construido sobre Python puro (sin dependencias externas) y organizado en capas:

* Núcleo matemático y de metadatos → `scripts/clacs_core.py`.
* Scripts de interacción por línea de comandos → `clacs_hilbert_cli.py`, `clacs_audit_artifact.py`, `clacs_seal_registry.py`.
* Carpetas para **documentos madre**, **frutos creativos**, **testigos** y **registro**.

---

## 1. Estructura del repositorio

Estructura sugerida del repo `clacs-hilbert/`:

```text
clacs-hilbert/
├─ README.md
├─ docs_madre/
│  ├─ 00_T-CLACS_v0.9.md
│  ├─ 01_Protocolo_Tejera_v0.1.md
│  ├─ 02_Capa_Jardinera_v0.1.md
│  ├─ 03_Guia_Acompanamiento_No_Clinico_v0.1.md
│  └─ 04_Manual_Metrica_Phi_CLACS_v0.1.md
├─ scripts/
│  ├─ clacs_core.py
│  ├─ clacs_hilbert_cli.py
│  ├─ clacs_audit_artifact.py
│  └─ clacs_seal_registry.py
├─ frutos/
│  ├─ textos/
│  ├─ visuales/
│  └─ otros/
├─ testigos/
│  ├─ manifiesto_testigos.md
│  ├─ W001_.../
│  └─ W002_.../
└─ registro/
   ├─ clacs_project.json
   ├─ clacs_registro.jsonl
   ├─ campos_clacs.json
   └─ sesiones_resumen.md
```

Los nombres concretos y versiones de los documentos madre pueden variar, pero la **lógica de carpetas** se mantiene.

---

## 2. Carpetas y contenido esperado

### 2.1. `docs_madre/` — Núcleo conceptual y metodológico

Aquí viven los **documentos fuente** de T‑CLACS. Se recomienda un máximo de 5 documentos madre, por ejemplo:

* `00_T-CLACS_v0.9.md`

  * Borrador de artículo académico (como el que ya tienes), con marco teórico, definiciones y metodología general.
* `01_Protocolo_Tejera_v0.1.md`

  * Descripción detallada del protocolo de auto‑entrenamiento (Capa Tejera).
* `02_Capa_Jardinera_v0.1.md`

  * Desarrollo del trabajo con mito personal, atlas simbólico, self dialógico, etc.
* `03_Guia_Acompanamiento_No_Clinico_v0.1.md`

  * Lineamientos éticos y metodológicos para acompañar a otras personas (no clínico).
* `04_Manual_Metrica_Phi_CLACS_v0.1.md`

  * Explicación formal de la métrica (\Phi_{CLACS}), ejemplos de cálculo, interpretación.

Estos documentos no son scripts ni configuraciones, sino el **cuerpo teórico** del sistema. Todo lo demás se entiende como aplicación o fruto de estos textos.

---

### 2.2. `scripts/` — Núcleo matemático y herramientas CLI

Contiene todo el código Python. Los archivos principales son:

* `clacs_core.py`  → núcleo compartido (modelo, cálculos, YAML, hash).
* `clacs_hilbert_cli.py`  → interfaz interactiva para definir el proyecto y el campo.
* `clacs_audit_artifact.py`  → auditoría de frutos textuales + front‑matter YAML + hash10.
* `clacs_seal_registry.py`  → sellado de frutos auditados en el registro JSONL.

Se describen en detalle en la sección **3. Manual de uso de scripts**.

Requisitos:

* Python 3.10+ (recomendado).
* No requiere librerías externas (solo `json`, `math`, `hashlib`, etc. del estándar).

Ejemplos de ejecución (desde la raíz del repo):

```bash
python scripts/clacs_hilbert_cli.py
python scripts/clacs_audit_artifact.py frutos/textos/2025-11-26_sesion-001_e3.md
python scripts/clacs_seal_registry.py frutos/textos/2025-11-26_sesion-001_e3.md
```

---

### 2.3. `frutos/` — Artefactos creativos

Aquí se guardan los **frutos** producidos bajo un campo CLACS:

* `frutos/textos/` → textos en Markdown (`.md`) u otro formato de texto con YAML front‑matter.
* `frutos/visuales/` → imágenes, bocetos, ilustraciones.
* `frutos/otros/` → audio, video, u otros tipos de artefactos.

Convención de nombres sugerida para textos:

```text
frutos/textos/AAAA-MM-DD_sesion-XXX_eN.md
```

Ejemplos:

* `frutos/textos/2025-11-26_sesion-001_e3.md`
* `frutos/textos/2025-11-26_sesion-002_e7.md`

Donde:

* `sesion-001` es un identificador humano de la sesión.
* `e3`, `e7` son IDs de artefacto que **deben existir** en `clacs_project.json`.

Los textos auditados llevarán un bloque **YAML front‑matter** al inicio, por ejemplo:

```markdown
---
id: e3
sesion_id: 2025-11-26_sesion-001
campo_id: S01
phi_clacs: 0.8647
dimensiones:
  - L
  - A
  - E
tipo: texto
timestamp: 2025-11-26T23:15:00
hash10: a1b2c3d4e5
---
Aquí comienza el cuerpo del texto…
```

Este front‑matter lo genera y actualiza **automáticamente** `clacs_audit_artifact.py`.

---

### 2.4. `testigos/` — Validaciones humanas y manifiestos

Carpeta dedicada a la parte **humana–ritual** del sistema: los **Testigos** y los **Escritos Testigo** (frutos con afinidad muy alta, p.ej. (\Phi_{CLACS} > 0.9500), validados por una persona concreta).

Estructura sugerida:

```text
testigos/
  ├─ manifiesto_testigos.md
  ├─ W001_Nombre-Simbolico/
  │  ├─ W001_manifiesto_individual.md
  │  └─ W001_evidencias.md
  └─ W002_.../
```

* `manifiesto_testigos.md`

  * Documento madre de la carpeta.
  * Define qué es un Testigo, criterios, responsabilidades, protocolo para declarar un Escrito Testigo.
* `W001_Nombre-Simbolico/`

  * Carpeta para cada Testigo.
  * `W001_manifiesto_individual.md` → breve historia, relación con CLACS, alcance de su rol.
  * `W001_evidencias.md` → lista de frutos que esa persona ha validado, con referencia a `frutos/` y `registro/clacs_registro.jsonl`.

Ejemplo de entrada en `W001_evidencias.md`:

```markdown
- Artefacto: e17
  - Fruto: frutos/textos/2025-12-01_sesion-010_e17.md
  - Campo: S03 (Mito Agua–Obsidiana)
  - Φ_CLACS: 0.9725
  - Fecha de validación: 2025-12-02
  - Comentario: "…"
```

En esta iteración, la integración con scripts es mínima: los Testigos se manejan principalmente de forma manual, usando los datos del registro.

---

### 2.5. `registro/` — Listado CLACS y configuración de proyecto

Esta carpeta concentra el **estado estructural** del sistema CLACS:

* `clacs_project.json`

  * Archivo central de configuración.
  * Lo crea y actualiza `clacs_hilbert_cli.py`.
  * Contiene:

    * `project_name` → nombre del proyecto.
    * `scale_max` → escala máxima por dimensión (p. ej. 4).
    * `dimensions` → lista de dimensiones (nombre, etiqueta, descripción).
    * `artefacts` → lista de artefactos con sus puntuaciones y vectores normalizados.
    * `field` → campo actual (prototipos y vector de campo) si está definido.

* `clacs_registro.jsonl`

  * Archivo JSONL (una línea = un objeto JSON) que actúa como **Listado CLACS**.
  * Lo escribe `clacs_seal_registry.py` al sellar frutos auditados.
  * Cada línea incluye:

    * `artefact_id`, `nombre`, `tipo`, `sesion_id`, `campo_id`, `phi_clacs`, `dimensiones`, `hash10`, `ruta_fruto`, `timestamp_registro`, `es_testigo`, `testigo_id`.

* `campos_clacs.json`

  * (Opcional en esta iteración) Catálogo de campos CLACS definidos: IDs, nombres, descripciones, vectores.
  * Puede llenarse manualmente o por scripts futuros.

* `sesiones_resumen.md`

  * Bitácora humana, en lenguaje natural.
  * Se puede actualizar a mano después de cada sesión: qué campo se usó, qué artefactos se generaron, notas cualitativas.

---

## 3. Manual de uso de scripts

En esta sección se explica **qué hace cada script**, **qué lee/escribe** y **cómo usarlo** paso a paso.

> Todos los comandos se asumen ejecutados desde la raíz del repo (`clacs-hilbert/`).

### 3.1. `clacs_core.py` — Núcleo compartido

Aunque no se ejecuta directamente, `clacs_core.py` es el corazón del sistema. Proporciona:

* **Modelos de datos:**

  * `Dimension`, `Artefact`, `Field`, `ProjectConfig`.
* **Gestión de proyecto:**

  * `load_project_config(allow_missing=False)` → lee `registro/clacs_project.json`.
  * `save_project_config(cfg)` → escribe `registro/clacs_project.json`.
* **Matemática de vectores y campo:**

  * `compute_artefact_vector(scores_raw, dim_order, scale_max)` → de puntuaciones crudas a vector normalizado.
  * `compute_field_vector(cfg, prototype_ids)` → vector de campo (\hat{\Phi}_S) a partir de prototipos.
  * `compute_phi(cfg, artefact_id)` → (\Phi_{CLACS}(e \mid S)) = `max(0, dot(v_e, Φ_S))**2`, redondeado a 4 decimales.
* **YAML y hash:**

  * `parse_yaml_front_matter(text)` → separa YAML inicial y cuerpo.
  * `dump_yaml_front_matter(data)` → serializa dict → YAML front‑matter.
  * `compute_hash10_from_body(body)` → `hash10` = 10 primeros caracteres de SHA256(cuerpo).

Los otros scripts lo importan y NUNCA replican esta lógica, lo que garantiza coherencia.

---

### 3.2. `clacs_hilbert_cli.py` — Definir proyecto, artefactos y campo

**Rol:**

* Crear e inicializar un **proyecto CLACS**.
* Definir **dimensiones** (L, A, E u otras), escala y nombre de proyecto.
* Registrar **artefactos** con puntuaciones por dimensión y obtener sus vectores normalizados.
* Definir el **campo** (vector (\hat{\Phi}_S)) a partir de artefactos prototipo.
* Calcular (\Phi_{CLACS}) para artefactos registrados.

**Archivos que lee/escribe:**

* Lee: `registro/clacs_project.json` (si existe).
* Escribe: `registro/clacs_project.json` (crea/actualiza).
* No toca `frutos/` ni `clacs_registro.jsonl`.

**Salida en consola:**

* Menú interactivo con opciones numeradas.
* Listado de dimensiones y artefactos.
* Vectores normalizados.
* Valores de (\Phi_{CLACS}) e interpretaciones cualitativas.

**Uso básico:**

```bash
python scripts/clacs_hilbert_cli.py
```

Si no existe `clacs_project.json`, el script preguntará si quieres crear un nuevo proyecto y te guiará por estos pasos:

1. **Nombre del proyecto** (cadena libre).
2. **Escala máxima** (entero positivo, p. ej. 4).
3. **Dimensiones**:

   * Para cada dimensión: nombre corto (`L`, `A`, `E`), etiqueta humana, descripción.
   * Puedes añadir tantas como quieras (3 es un buen inicio).

Luego verás un menú como:

```text
=== Menú CLACS–Hilbert ===
Proyecto: Mi Proyecto CLACS
1) Ver dimensiones
2) Añadir artefacto
3) Listar artefactos
4) Definir / redefinir campo (prototipos)
5) Calcular Φ_CLACS para un artefacto
6) Guardar y salir
```

Flujo recomendado:

1. **Añadir artefactos** (opción 2):

   * ID (`e1`, `e2`, …), nombre, tipo, ruta opcional, notas.
   * Puntuaciones 0..scale_max para cada dimensión.
   * El script calcula el vector normalizado y lo muestra.

2. **Listar artefactos** (opción 3) para revisar.

3. **Definir campo** (opción 4):

   * Introducir IDs de prototipos separados por comas (`e1,e2,e3`).
   * El script calcula (\hat{\Phi}_S) y lo guarda en `clacs_project.json`.

4. **Calcular Φ_CLACS** (opción 5):

   * Dar un ID de artefacto.
   * Recibir (\Phi_{CLACS}) y una etiqueta cualitativa (ruido, periférico, núcleo, canónico).

5. **Guardar y salir** (opción 6).

---

### 3.3. `clacs_audit_artifact.py` — Auditoría, YAML y hash10

**Rol:**

* Tomar un fruto textual en `frutos/textos/`.
* Verificar que su `id` exista en `clacs_project.json` (por medio de tu input).
* Calcular (\Phi_{CLACS}) con el campo actual.
* Escribir/actualizar un **YAML front‑matter** con metadatos CLACS.
* Calcular `hash10` sobre el cuerpo del texto y guardarlo en YAML.

**Archivos que lee:**

* `registro/clacs_project.json` → para cargar dimensiones, artefactos y campo.
* El archivo de texto indicado (p. ej. `frutos/textos/2025-11-26_sesion-001_e3.md`).

**Archivos que escribe:**

* Sobrescribe el archivo de texto indicado, añadiendo o actualizando su front‑matter YAML.
* No toca `clacs_registro.jsonl` ni otros.

**Salida en consola:**

* Muestra el valor calculado de (\Phi_{CLACS}).
* Muestra el `hash10` generado.
* Confirma que el archivo fue auditado y actualizado.

**Uso básico:**

```bash
python scripts/clacs_audit_artifact.py frutos/textos/2025-11-26_sesion-001_e3.md
```

El script te pedirá:

1. `ID del artefacto` (ej. `e3`)

   * Debe existir ya en `clacs_project.json`.
   * Se usa para obtener el vector del artefacto.
2. `sesion_id` (ej. `2025-11-26_sesion-001`)
3. `campo_id` (ej. `S01` · por defecto usa `S01` si lo dejas vacío).
4. `tipo` (`texto`, `visual`, etc.; por defecto `texto`).

El script entonces:

* Carga el contenido del archivo.
* Si el archivo ya tenía YAML al inicio, lo lee, lo actualiza y lo reescribe.
* Si no tenía YAML, crea uno nuevo al inicio.
* Calcula:

  * `phi_clacs` = (\Phi_{CLACS}) para ese artefacto.
  * `hash10` = SHA256(cuerpo)[:10].
* Inserta o actualiza campos en el YAML:

  * `id`, `sesion_id`, `campo_id`, `phi_clacs`, `dimensiones`, `tipo`, `timestamp`, `hash10`.

Al finalizar verás algo como:

```text
Φ_CLACS(e3) = 0.8647

Archivo auditado y actualizado: frutos/textos/2025-11-26_sesion-001_e3.md
hash10 (cuerpo): a1b2c3d4e5
```

---

### 3.4. `clacs_seal_registry.py` — Sellar frutos en el registro CLACS

**Rol:**

* Tomar un fruto textual **ya auditado** (con YAML y `hash10`).
* Verificar integridad:

  * recalcula `hash10` y lo compara con YAML;
  * recalcula (\Phi_{CLACS}) y lo compara con `phi_clacs` en YAML.
* Si todo es consistente, escribe una entrada en `registro/clacs_registro.jsonl`.

**Archivos que lee:**

* `registro/clacs_project.json` → para recomputar (\Phi_{CLACS}).
* El archivo de texto indicado (contenido + YAML).

**Archivos que escribe:**

* `registro/clacs_registro.jsonl` → añade una línea JSON con metadatos del fruto sellado.

**Salida en consola:**

* Mensajes de error si algo no cuadra (hash, Φ, campos faltantes).
* En caso de éxito, imprime la entrada JSON añadida.

**Uso básico:**

```bash
python scripts/clacs_seal_registry.py frutos/textos/2025-11-26_sesion-001_e3.md
```

Requisitos previos:

* El archivo debe tener YAML válído con los campos:

  * `id`, `sesion_id`, `campo_id`, `phi_clacs`, `dimensiones`, `hash10`.
* El archivo debe haber sido auditado con `clacs_audit_artifact.py`.

El script:

1. Lee YAML y cuerpo del texto.
2. Verifica **hash10**:

   * Recalcula `hash10` del cuerpo.
   * Si difiere del YAML, se detiene con error.
3. Verifica **Φ_CLACS**:

   * Recalcula (\Phi_{CLACS}) con `clacs_project.json`.
   * Si difiere de `phi_clacs` (más allá de una tolerancia pequeña), se detiene.
4. Construye una entrada JSON:

```json
{
  "artefact_id": "e3",
  "nombre": "2025-11-26_sesion-001_e3.md",
  "tipo": "texto",
  "sesion_id": "2025-11-26_sesion-001",
  "campo_id": "S01",
  "phi_clacs": 0.8647,
  "dimensiones": ["L", "A", "E"],
  "hash10": "a1b2c3d4e5",
  "ruta_fruto": "frutos/textos/2025-11-26_sesion-001_e3.md",
  "timestamp_registro": "2025-11-26T23:20:00",
  "es_testigo": false,
  "testigo_id": null
}
```

5. Añade esta línea a `registro/clacs_registro.jsonl`.

Si `phi_clacs > 0.95`, `es_testigo` se marca automáticamente como `true` (aunque la validación humana y `testigo_id` se manejan aparte).

---

## 4. Flujo de trabajo completo (resumen)

1. **Definir proyecto y campo**

   * Ejecutar `clacs_hilbert_cli.py`.
   * Crear proyecto, definir escala y dimensiones.
   * Registrar varios artefactos (e1, e2, e3…).
   * Elegir prototipos y definir el campo (Φ_S).

2. **Producir un fruto textual**

   * Escribir un texto siguiendo el protocolo T‑CLACS (Tejera, Jardinera, etc.).
   * Guardarlo en `frutos/textos/` con un nombre que incluya fecha, sesión e ID (`e3`).

3. **Auditar el fruto**

   * Ejecutar:

     ```bash
     python scripts/clacs_audit_artifact.py frutos/textos/..._e3.md
     ```

   * Indicar `id` (`e3`), `sesion_id`, `campo_id`, `tipo`.

   * El script crea/actualiza YAML con `phi_clacs`, `dimensiones`, `timestamp`, `hash10`.

4. **Sellar el fruto**

   * Ejecutar:

     ```bash
     python scripts/clacs_seal_registry.py frutos/textos/..._e3.md
     ```

   * Si hash y Φ son coherentes, el fruto queda registrado en `clacs_registro.jsonl`.

5. **(Opcional) Validación por Testigo**

   * Revisar `clacs_registro.jsonl` en busca de frutos con `phi_clacs > 0.95`.
   * Leerlos con calma; si un Testigo los valida como Escrito Testigo:

     * actualizar manualmente la entrada correspondiente (`es_testigo: true`, `testigo_id: "W001"`),
     * registrar el caso en `testigos/W001_evidencias.md`.

6. **Actualizar la bitácora humana**

   * Anotar en `registro/sesiones_resumen.md` un resumen de la sesión: símbolos, insights, cambios en el mito personal.

---

## 5. Extensiones posibles

Este README describe la **iteración actual** del sistema clacs‑hilbert. Algunas extensiones naturales son:

* Añadir un módulo de utilidades (`clacs_tools.py`) para:

  * listar artefactos por rango de Φ,
  * exportar `clacs_registro.jsonl` a CSV,
  * generar gráficos de distribución de Φ por sesión o por campo.

* Estructurar `campos_clacs.json` como catálogo formal de campos:

  * `campo_id`, `nombre`, `descripcion`, `prototipos`, `vector`.

* Añadir scripts para trabajar con `testigos/`:

  * sugerir candidatos a Escrito Testigo,
  * generar plantillas para `W001_evidencias.md`.

* Integrar este núcleo con otros sistemas (por ejemplo, frontends tipo QEL o dashboards web) consumiendo `clacs_project.json` y `clacs_registro.jsonl`.

Mientras tanto, este README sirve como **guía completa** para:

* entender qué va en cada carpeta,
* saber qué hace cada script,
* y seguir un flujo de trabajo reproducible desde la definición del campo hasta el sellado de frutos.
