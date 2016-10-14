from sqlalchemy import MetaData, Table, Column, String, Integer
from sqlalchemy import create_engine
from sqlalchemy import and_, or_
from sqlalchemy import select
from sqlalchemy import ForeignKey
import os

metadata = MetaData()
e = create_engine("sqlite:///some.db")

conn = e.connect()
user_table = Table('user', metadata,
                    Column('id', Integer, primary_key=True),
                    Column('username', String(50)),
                    Column('fullname', String(50))
                   )
address_table = Table("address", metadata,
                      Column('id', Integer, primary_key=True),
                      Column('user_id', Integer, ForeignKey('user.id'),
                             nullable=False),
                      Column('email_address', String(100), nullable=False)
                      )
metadata.create_all(e)
conn.execute(address_table.insert(), [
    {"user_id": 1, "email_address": "ed@ed.com"},
    {"user_id": 1, "email_address": "ed@gmail.com"},
    {"user_id": 2, "email_address": "jack@yahoo.com"},
    {"user_id": 3, "email_address": "wendy@gmail.com"},
])

print(user_table.c.fullname == 'ed')
print(and_(user_table.c.fullname == 'ed',user_table.c.id > 5))
print(or_(user_table.c.username == 'ed'))

#03_sql_expression
insert_stmt = user_table.insert().values(username='ed', fullname='Ed Jones')
result = conn.execute(insert_stmt)
result.inserted_primary_key
conn.execute(user_table.insert(), [
    {'username': 'jack', 'fullname': 'Jack Burger'},
    {'username': 'wendy', 'fullname': 'Wendy Weathersmith'}
])
#03_sql_expression

result = conn.execute(user_table.insert(), [
    {'username': 'dilbert',
     'fullname': 'Dilbert Jones'}
])
print(result.inserted_primary_key)


select = select([user_table]). \
    where(or_(user_table.c.username == 'wendy',user_table.c.username == 'dilbert')). \
          order_by(user_table.c.fullname)

print(conn.execute(select).fetchall())

query = select([user_table.c.fullname, address_table.c.email_address]).\
    select_from(user_table.join(address_table)).\
    where(user_table.c.username == 'ed').\
    order_by(address_table.c.email_addres)
print(conn.execute(query).fetchall())

result = user_table.update().values(fullname="Ed Jones").where(user_table.c.username == 'ed')
print(conn.execute(result).fetchall())


delete_stmt = user_table.delete()
conn.execute(delete_stmt)
delete_stmt=address_table.delete()
conn.execute(delete_stmt)