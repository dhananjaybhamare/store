"""empty message

Revision ID: 34e2a732547a
Revises: None
Create Date: 2018-09-29 11:19:25.289177

"""

# revision identifiers, used by Alembic.
revision = '34e2a732547a'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('shopping_list',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=64), nullable=True),
    sa.Column('store_name', sa.String(length=64), nullable=True),
    sa.Column('created_time', sa.DateTime(), nullable=True),
    sa.Column('updated_time', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('unit_measurement',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('item',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=64), nullable=True),
    sa.Column('price', sa.Float(), nullable=True),
    sa.Column('discount_percentage', sa.Float(), nullable=True),
    sa.Column('unit_measurement_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['unit_measurement_id'], ['unit_measurement.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('shopping_list_items',
    sa.Column('shopping_list_id', sa.Integer(), nullable=False),
    sa.Column('item_id', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.Column('actual_item_price', sa.DECIMAL(), nullable=True),
    sa.Column('discount_percentage', sa.DECIMAL(), nullable=True),
    sa.Column('discount_per_item', sa.DECIMAL(), nullable=True),
    sa.Column('discounted_item_price', sa.DECIMAL(), nullable=True),
    sa.Column('actual_total_price', sa.DECIMAL(), nullable=True),
    sa.Column('discounted_total_price', sa.DECIMAL(), nullable=True),
    sa.ForeignKeyConstraint(['item_id'], ['item.id'], ),
    sa.ForeignKeyConstraint(['shopping_list_id'], ['shopping_list.id'], ),
    sa.PrimaryKeyConstraint('shopping_list_id', 'item_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('shopping_list_items')
    op.drop_table('item')
    op.drop_table('unit_measurement')
    op.drop_table('shopping_list')
    # ### end Alembic commands ###
