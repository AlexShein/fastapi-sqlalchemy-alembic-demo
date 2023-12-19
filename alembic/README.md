Alembic is a tool to control DB changes, written by author of SQL Alchemy.
It allows you to automatically generate, apply and roll back DB migrations.

Before running the commands ensure that you have your python env activated.
To generate new migration automatically based on model classes changes run

```
alembic revision --autogenerate -m "<migration_name>"
```

To migrate to certain migration, copy it's hash and run

```
alembic upgrade <migration_hash>
```

To revert last migration copy hash of the previous migration and run

```
alembic downgrade <down_migration_hash>
```

To unapply ALL migrations use

```
alembic downgrade base
```

Also it's possible to "apply" migration virtually without changes in the
underlying DB. It may be useful if tables are already created. To do this run

```
alembic stamp <migration_hash>
```

Also it's possible to "apply" migration virtually without changes in the
underlying DB. It may be useful if tables are already created. To do this
run

```
alembic stamp <migration_hash>
```

_DO NOT USE_ commands like

```
alembic upgrade +1

alembic downgrade -1
```

because it possible to run them multiple times hence rolling back/applying more
than 1 migration in a time an doing potentially dangerous changes to the DB.

[Documentation is available here](https://alembic.sqlalchemy.org/en/latest/tutorial.html)
