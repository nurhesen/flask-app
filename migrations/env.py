import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context


config = context.config


fileConfig(config.config_file_name)


from app.db.base import Base

import app.models.user
import app.models.post

target_metadata = Base.metadata

def get_url():
    return os.getenv("DATABASE_URL")

config.set_main_option("sqlalchemy.url", get_url())

def run_migrations_offline():
    """Run migrations offline"""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations online"""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
