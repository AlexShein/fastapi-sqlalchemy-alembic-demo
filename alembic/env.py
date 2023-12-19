from logging.config import fileConfig
from typing import Optional

from sqlalchemy import engine_from_config, pool

from alembic import context
from database import SQLALCHEMY_DATABASE_URL
from main import Base

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

section = config.config_ini_section

config.set_section_option(section, "DB_ADDRESS", SQLALCHEMY_DATABASE_URL)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

# Following code is needed for Alembic to ignore tables which are not managed by the app:

UNMANAGED_TABLE_PREFIXES = [
    "spatial_ref_sys",
]
UNMANAGED_SCHEMAS = ["topology", "tiger"]


def include_name(name: Optional[str], type_: str, params) -> bool:
    if type_ == "table":
        if params.get("schema_name") in UNMANAGED_SCHEMAS:
            return False
        for prefix in UNMANAGED_TABLE_PREFIXES:
            if name and name.startswith(prefix):
                return False
    return True


context.configure.compare_type = True


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_schemas=True,
        include_name=include_name,
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        echo=True,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_schemas=True,
            include_name=include_name,
            compare_type=True,
        )

        with context.begin_transaction() as transaction:
            context.run_migrations()
            if "dry-run" in context.get_x_argument():
                print("Dry-run succeeded; now rolling back transaction...")
                transaction.rollback()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
