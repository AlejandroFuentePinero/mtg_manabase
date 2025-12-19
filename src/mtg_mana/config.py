from __future__ import annotations

from pathlib import Path

# src/mtg_mana/config.py -> repo root is two levels up from src/
PROJECT_ROOT: Path = Path(__file__).resolve().parents[2]

# Data
DATA_DIR: Path = PROJECT_ROOT / "data"
RAW_DATA_DIR: Path = DATA_DIR / "raw"
INTERIM_DATA_DIR: Path = DATA_DIR / "interim"
PROCESSED_DATA_DIR: Path = DATA_DIR / "processed"
EXTERNAL_DATA_DIR: Path = DATA_DIR / "external"

# Reports
REPORTS_DIR: Path = PROJECT_ROOT / "reports"
FIGURES_DIR: Path = REPORTS_DIR / "figures"
TABLES_DIR: Path = REPORTS_DIR / "tables"

# Models (saved artefacts)
MODELS_DIR: Path = PROJECT_ROOT / "models"

# Notebooks / docs (optional, but handy)
NOTEBOOKS_DIR: Path = PROJECT_ROOT / "notebooks"
DOCS_DIR: Path = PROJECT_ROOT / "docs"


def ensure_dirs() -> None:
    """Create expected project directories if they do not exist."""
    for p in (
        RAW_DATA_DIR,
        INTERIM_DATA_DIR,
        PROCESSED_DATA_DIR,
        EXTERNAL_DATA_DIR,
        FIGURES_DIR,
        TABLES_DIR,
        MODELS_DIR,
    ):
        p.mkdir(parents=True, exist_ok=True)
