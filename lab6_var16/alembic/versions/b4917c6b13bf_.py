"""empty message

Revision ID: b4917c6b13bf
Revises: 
Create Date: 2022-11-04 12:06:34.180684

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b4917c6b13bf'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    op.drop_table('schelude_has_films')
    op.drop_table('schelude_has_users')
    op.drop_table('visiting')
    op.drop_table('sessions')
    op.drop_table('schelude')
    op.drop_table('user')
    op.drop_table('films')
    
    
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###