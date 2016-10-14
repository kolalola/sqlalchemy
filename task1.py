from sqlalchemy import create_engine

import os
if os.path.exists("some.db"):
    os.remove("some.db")
e = create_engine("sqlite:///some.db")
e.execute("""
    create table employee (
        emp_id integer primary key,
        emp_name varchar
    )
""")
e.execute("insert into employee (emp_name) values (:emp_name)", emp_name='dilbert')
result=e.execute("select * from employee")
print(result.fetchall())
lastnames=['ed','jack','fred','wendy','mary']
for lastname in lastnames:
    e.execute("insert into employee (emp_name) values (:emp_name)", emp_name="{}".format(lastname))
result=e.execute("select * from employee")
print (result.fetchall())

