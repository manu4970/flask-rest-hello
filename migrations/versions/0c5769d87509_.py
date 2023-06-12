"""empty message

Revision ID: 0c5769d87509
Revises: 73ba4f35d884
Create Date: 2023-06-12 22:59:46.864091

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0c5769d87509'
down_revision = '73ba4f35d884'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('favoritos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('usuario_id', sa.Integer(), nullable=True),
    sa.Column('planeta_id', sa.Integer(), nullable=True),
    sa.Column('personaje_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['personaje_id'], ['people.id'], ),
    sa.ForeignKeyConstraint(['planeta_id'], ['planets.id'], ),
    sa.ForeignKeyConstraint(['usuario_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('peopleFav')
    op.drop_table('planetsFav')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('planetsFav',
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('planets_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['planets_id'], ['planets.id'], name='planetsFav_planets_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='planetsFav_user_id_fkey'),
    sa.PrimaryKeyConstraint('user_id', 'planets_id', name='planetsFav_pkey')
    )
    op.create_table('peopleFav',
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('people_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['people_id'], ['people.id'], name='peopleFav_people_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='peopleFav_user_id_fkey'),
    sa.PrimaryKeyConstraint('user_id', 'people_id', name='peopleFav_pkey')
    )
    op.drop_table('favoritos')
    # ### end Alembic commands ###
