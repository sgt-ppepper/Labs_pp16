"""alembic

Revision ID: b595f4a104da
Revises: 
Create Date: 2022-11-03 18:36:47.659743

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import DateTime
# revision identifiers, used by Alembic.
revision = 'b595f4a104da'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'user',
        Column('id', Integer, primary_key=True),
        Column('username', String(45), unique=True),
        Column('first_name', String(45)),
        Column('last_name', String(45)),
        Column('email', String(45), unique=True),
        Column('password', String(100)),
        Column('notes_count', Integer, default=0)
    )
    op.create_table(
        'notes',
        Column('id', Integer, primary_key=True),
        Column('title', String(45), nullable=False),
        Column('content', String(404)),
        Column('notescol', String(45)),
        Column('tags', String(400), nullable=False),
        Column('user_iduser', Integer, ForeignKey("user.id"), nullable=False)
    )
    op.create_table(
        'access',
        Column('id', Integer, primary_key=True, autoincrement=True),
        Column('user_id', Integer, ForeignKey("user.id"), nullable=False, primary_key=True),
        Column('note_id', Integer, ForeignKey("notes.id"), nullable=False, primary_key=True),
        Column('time', DateTime, nullable=False)
    )
    op.create_table(
        'change',
        Column('id', Integer, primary_key=True, autoincrement=True),
        Column('user_id', Integer, ForeignKey("user.id"), nullable=False, primary_key=True),
        Column('note_id', Integer, ForeignKey("notes.id"), nullable=False, primary_key=True),
        Column('time', DateTime, nullable=False)
    )
    op.create_table(
        'tag',
        Column('id', Integer, primary_key=True, autoincrement=True),
        Column('name', String(45), unique=True)
    )


def downgrade() -> None:
    pass
