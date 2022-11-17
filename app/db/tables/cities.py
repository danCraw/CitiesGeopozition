from sqlalchemy import Column, String, Table
from sqlalchemy.dialects.postgresql import UUID

from app.db.base import metadata

City = Table(
                'cities',
                metadata,
                Column("id", UUID(), primary_key=True),
                Column("name", String(65), nullable=False),
                Column("latitude", String(65), nullable=False),
                Column("longitude", String(65), nullable=False)
)
