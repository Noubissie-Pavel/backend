Here is the full `README.md` file that combines everything into a single file for your project:

### `README.md`

```markdown
# Alembic Migrations Guide

This guide explains the process for running Alembic migrations in the project, both for the first-time setup and for updating the database schema after code changes.

## First-Time Setup

If you're setting up the database and migrations for the first time, follow these steps:

1. **Install Dependencies**  
   Ensure all required dependencies are installed. You can do this by running:
   
   ```bash
   pip install -r requirements.txt
   ```

2. **Initialize Alembic**  
   This step creates the Alembic configuration and migration environment files:

   ```bash
   alembic init alembic
   ```

3. **Create the Initial Migration**  
   The following command will auto-generate the first migration. It compares your current database models (defined in SQLAlchemy) with the existing database schema (if any) and generates the necessary migration files.

   ```bash
   alembic revision --autogenerate -m "Initial migration"
   ```

4. **Apply the Migration**  
   To apply the migration and create the tables in the database, run the following command:

   ```bash
   alembic upgrade head
   ```

   This will apply all migrations up to the most recent revision (`head`), creating your database schema.

---

## Updating the Database Schema

After modifying your SQLAlchemy models (e.g., adding new columns, modifying data types), you'll need to update your database schema. Follow these steps:

1. **Generate a New Migration**  
   After making changes to the models, generate a new migration script by running the following:

   ```bash
   alembic revision --autogenerate -m "Describe changes made"
   ```

   This will create a new migration file under the `alembic/versions` directory. Review this file to ensure it correctly represents the changes you made to the models.

2. **Apply the Migration**  
   Apply the new migration by running the following command:

   ```bash
   alembic upgrade head
   ```

   This will apply the new migration and update the database schema.

---

## Rolling Back Migrations

If you need to rollback the most recent migration, you can do so by running:

```bash
alembic downgrade -1
```

To rollback to a specific migration, use its revision identifier (found in the filename under `alembic/versions`):

```bash
alembic downgrade <revision-id>
```

---

## Troubleshooting

- **`ImportError` related to models**: Ensure that your SQLAlchemy models are imported into the Alembic environment file (`env.py`). Typically, you can add them like this:

  ```python
  from app.models import User  # Import your models here
  ```

- **`No changes detected` error**: This usually happens if there are no model changes that require a migration. Ensure you've actually modified your models before running `alembic revision --autogenerate`.

---

## Example `alembic.ini` Configuration

Make sure to check your `alembic.ini` file for the correct database URL. It should look something like this:

```ini
[alembic]
script_location = alembic
sqlalchemy.url = postgresql://username:password@localhost:5432/database_name
```

Replace `username`, `password`, `localhost`, and `database_name` with your actual PostgreSQL credentials.

---

## Summary of Common Commands

- **Initialize Alembic**: `alembic init alembic`
- **Generate Initial Migration**: `alembic revision --autogenerate -m "Initial migration"`
- **Apply Migrations**: `alembic upgrade head`
- **Generate Migration after Schema Changes**: `alembic revision --autogenerate -m "Describe changes made"`
- **Rollback Migration**: `alembic downgrade -1`
- **Rollback to Specific Revision**: `alembic downgrade <revision-id>`
```

---

This single `README.md` file will guide you through the setup, usage, and troubleshooting of Alembic migrations for your project.