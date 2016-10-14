from sqlalchemy import MetaData
from sqlalchemy import Table, Column
from sqlalchemy import Integer, String
from sqlalchemy import String, Numeric, DateTime, Enum,Unicode,UnicodeText
from sqlalchemy import ForeignKey,ForeignKeyConstraint,create_engine
import os
from sqlalchemy import inspect
if os.path.exists("some2.db"):
    os.remove("some2.db")
e = create_engine("sqlite:///some2.db")


metaData=MetaData()
user_table = Table('user', metaData,
                   Column('id', Integer, primary_key=True),
                   Column('name', String),
                   Column('fullname', String)
                   )
addresses_table = Table('address', metaData,
                        Column('id', Integer, primary_key=True),
                        Column('email_address', String(100), nullable=False),
                        Column('user_id', Integer, ForeignKey('user.id'))
                        )
story_table = Table('story', metaData,
                    Column('story_id', Integer, primary_key=True),
                    Column('version_id', Integer, primary_key=True),
                    Column('headline', Unicode(100), nullable=False),
                    Column('body', UnicodeText)
                    )
published_table = Table('published', metaData,
                        Column('pub_id', Integer, primary_key=True),
                        Column('pub_timestamp', DateTime, nullable=False),
                        Column('story_id', Integer),
                        Column('version_id', Integer),
                        ForeignKeyConstraint(
                            ['story_id', 'version_id'],
                            ['story.story_id', 'story.version_id'])
                        )

network_table= Table('network',metaData,
             Column('network_id', Integer, primary_key=True),
             Column('name', String(100), nullable=False),
             Column('created_at', DateTime, nullable=False),
             Column('owner_id', Integer,ForeignKey('user.id'))
             )
metaData.create_all(e)
metadata2=MetaData()
reflect = Table('user', metadata2, autoload=True, autoload_with=e)
inspector = inspect(e)
columns=inspector.get_columns('network')

results = []
table_names=inspector.get_table_names()
for table_name in table_names:
   for column in inspector.get_columns(table_name):
       if column['name'] == 'story_id':
           results+=table_name
print(results)




