"""SQLAlchemy Core Table models live here as per-feature files.

`metadata` is the single MetaData shared by every table so Alembic
autogenerate and migrations can target them all. There are no tables yet.
"""

from sqlalchemy import MetaData

metadata = MetaData()
