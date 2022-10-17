"""Code Challenge Init

Revision ID: 3159f1d8331d
Revises: 
Create Date: 2022-10-16 21:57:15.545445

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = '3159f1d8331d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('usr_users',
    sa.Column('username', sqlmodel.sql.sqltypes.AutoString(length=55), nullable=False),
    sa.Column('hashed_password', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('biography', sqlmodel.sql.sqltypes.AutoString(length=200), nullable=True),
    sa.Column('uuid', sqlmodel.sql.sqltypes.GUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('current_timestamp(0)'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('current_timestamp(0)'), nullable=False),
    sa.PrimaryKeyConstraint('uuid', name=op.f('pk_usr_users')),
    sa.UniqueConstraint('username', name=op.f('uq_usr_users_username'))
    )
    op.create_index(op.f('ix_usr_users_uuid'), 'usr_users', ['uuid'], unique=True)
    op.create_table('pst_posts',
    sa.Column('uuid', sqlmodel.sql.sqltypes.GUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('current_timestamp(0)'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('current_timestamp(0)'), nullable=False),
    sa.Column('title', sqlmodel.sql.sqltypes.AutoString(length=100), nullable=False),
    sa.Column('text', sqlmodel.sql.sqltypes.AutoString(length=1000), nullable=False),
    sa.Column('author_user_id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.ForeignKeyConstraint(['author_user_id'], ['usr_users.uuid'], name=op.f('fk_pst_posts_author_user_id_usr_users')),
    sa.PrimaryKeyConstraint('uuid', 'author_user_id', name=op.f('pk_pst_posts'))
    )
    op.create_index(op.f('ix_pst_posts_uuid'), 'pst_posts', ['uuid'], unique=True)
    op.create_table('sbs_subscriptions',
    sa.Column('author_user_id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('subscriber_user_id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.ForeignKeyConstraint(['author_user_id'], ['usr_users.uuid'], name=op.f('fk_sbs_subscriptions_author_user_id_usr_users')),
    sa.ForeignKeyConstraint(['subscriber_user_id'], ['usr_users.uuid'], name=op.f('fk_sbs_subscriptions_subscriber_user_id_usr_users')),
    sa.PrimaryKeyConstraint('author_user_id', 'subscriber_user_id', name=op.f('pk_sbs_subscriptions'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('sbs_subscriptions')
    op.drop_index(op.f('ix_pst_posts_uuid'), table_name='pst_posts')
    op.drop_table('pst_posts')
    op.drop_index(op.f('ix_usr_users_uuid'), table_name='usr_users')
    op.drop_table('usr_users')
    # ### end Alembic commands ###
