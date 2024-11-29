# alembic/env.py

import asyncio
from logging.config import fileConfig

from decouple import config as decouple_config
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import create_async_engine

from alembic import context

# Import your SQLAlchemy models' MetaData object for 'autogenerate' support
from app.models import Base, Issue, Book, Series  # Ensure all models are imported

# this is the Alembic Config object, which provides access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
fileConfig(config.config_file_name)

# Set target metadata for 'autogenerate'
target_metadata = Base.metadata

# Retrieve the DATABASE_URL from the environment using python-decouple
DATABASE_URL = decouple_config('DATABASE_URL')

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,  # Optional: Detect column type changes
        compare_server_default=True,  # Optional: Detect default changes
    )

    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection):
    """Configure the Alembic context with the given connection."""
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,  # Optional
        compare_server_default=True,  # Optional
    )

    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online():
    """Run migrations in 'online' mode."""
    # Create an asynchronous engine
    connectable = create_async_engine(
        DATABASE_URL,
        poolclass=pool.NullPool,
        echo=False,  # Set to True to see SQL queries
    )

    # Connect to the database
    async with connectable.connect() as connection:
        # Run the synchronous migration function within the async context
        await connection.run_sync(do_run_migrations)

    # Dispose of the engine
    await connectable.dispose()

if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())