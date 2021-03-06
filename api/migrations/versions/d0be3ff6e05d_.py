"""empty message

Revision ID: d0be3ff6e05d
Revises: 074f27c81842
Create Date: 2022-02-28 14:34:59.986067

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'd0be3ff6e05d'
down_revision = '074f27c81842'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('reading', sa.Column('temperature', sa.Float(), nullable=False))
    op.add_column('reading', sa.Column('humidity', sa.Float(), nullable=False))
    op.add_column('reading', sa.Column('time', sa.DateTime(), nullable=True))
    op.drop_column('reading', 'time_taken')
    op.drop_column('reading', 'hum')
    op.drop_column('reading', 'temp')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('reading', sa.Column('temp', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False))
    op.add_column('reading', sa.Column('hum', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False))
    op.add_column('reading', sa.Column('time_taken', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.drop_column('reading', 'time')
    op.drop_column('reading', 'humidity')
    op.drop_column('reading', 'temperature')
    # ### end Alembic commands ###
