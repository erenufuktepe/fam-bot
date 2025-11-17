# migrations/env.py
from __future__ import annotations

import sys
from logging.config import fileConfig
from pathlib import Path

from alembic import context
from sqlalchemy import engine_from_config, pool

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(REPO_ROOT))

from app.models import Base
from app.settings import settings

# Alembic Config
config = context.config

# Logging from alembic.ini
if config.config_file_name:
    fileConfig(config.config_file_name)

# Use your model metadata for autogenerate
target_metadata = Base.metadata


# --- Normalize SQLite URL, create parent directory, and force Alembic to use it ---
def _normalize_sqlite_url(url: str) -> tuple[str, Path | None]:
    if not url.startswith("sqlite"):
        return url, None
    # Accept sqlite:////C:/... or sqlite:///C:/... or relative forms
    if url.startswith("sqlite:////"):
        fs_path = Path(url.replace("sqlite:////", "", 1))
    elif url.startswith("sqlite:///"):
        fs_path = Path(url.replace("sqlite:///", "", 1))
    else:
        fs_path = Path(url.split("sqlite:///", 1)[-1])

    # If relative, anchor to repo root
    if not fs_path.is_absolute():
        fs_path = (REPO_ROOT / fs_path).resolve()

    fs_path.parent.mkdir(parents=True, exist_ok=True)
    clean = f"sqlite:///{fs_path.as_posix()}"
    return clean, fs_path


raw_url = getattr(settings, "DB_URL", None) or getattr(settings, "DATABASE_URL", None)
clean_url, fs_path = _normalize_sqlite_url(raw_url)

# Force Alembic to use this exact URL (ignore any alembic.ini placeholder)
config.set_main_option("sqlalchemy.url", clean_url)

print("=== Alembic DB URL ->", clean_url)
if fs_path:
    print("=== Alembic FS path ->", fs_path)


def run_migrations_offline() -> None:
    context.configure(
        url=clean_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
