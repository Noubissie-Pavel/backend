import sys
from pathlib import Path

from alembic import context

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.db.session import engine

from app.models import user, company, telecom_operator, sim_cart, ussd, transaction

config = context.config

config.set_main_option('sqlalchemy.url', str(engine.url))

target_metadata = [user.Base.metadata, company.Base.metadata, telecom_operator.Base.metadata, sim_cart.Base.metadata,
                   ussd.Base.metadata, transaction.Base.metadata]


def run_migrations_online():
    connectable = engine

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    print("Offline mode not supported.")
else:
    run_migrations_online()
