from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String,ForeignKey,Numeric
from sqlalchemy.orm import Session,relationship
from sqlalchemy import create_engine

Base = declarative_base()
e = create_engine("sqlite:///some.db")
conn=e.connect()
class Network(Base):
    __tablename__ = 'network'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    def __repr__(self):
        return "Network: %r" % (self.name)

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)

    def __repr__(self):
        return "<User(%r, %r)>" % (
                self.name, self.fullname
            )

class Address(Base):
    __tablename__ = 'address'

    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))

    user = relationship("User", backref="addresses")

    def __repr__(self):
        return "<Address(%r)>" % self.email_address

class Account(Base):
    __tablename__ = 'account'
    id = Column(Integer, primary_key=True)
    owner = Column(String(50), nullable=False)
    balance = Column(Numeric, default=0)
    def __repr__(self):
        return "Account: %r, %r" % (self.owner, self.balance)

class Transaction(Base):
    __tablename__ = 'transaction'
    id = Column(Integer, primary_key=True)
    amount = Column(Numeric, nullable=False)
    account_id = Column(Integer, ForeignKey(Account.__tablename__ + '.id'), nullable=False)
    account = relationship('Account', backref="transactions")
    def __repr__(self):
        return "Transaction: %r" % (self.amount)

Base.metadata.create_all(e)

session1 = Session(bind = e)
session1.add(Network(name = 'net1'))
session1.add(Network(name = 'net2'))
session1.commit()
print(e.execute("select * from network").fetchall())

session2 = Session(bind = e)
session2.add(User(name='wendy', fullname='Wendy Weathersmith'))
session2.add(User(name='mary', fullname='Mary Contrary'))
session2.add(User(name='fred', fullname='Fred Flinstone'))
query = session2.query(User.fullname).order_by(User.fullname)
print(query)
query2 = query.filter(User.name.in_(['mary', 'ed']))
print(query2)

query3 = session2.query(User.name, Address.email_address).join(Address).filter(Address.email_address.in_(['j25@yahoo.com']))
print(query3)



session3=Session(bind = e)
account1=Account(owner = "Jack Jones", balance = 5000)
account2=Account(owner="Ed Rendell", balance=10000)
session3.add_all([Account(owner = "Jack Jones", balance = 5000),
                 Account(owner="Ed Rendell", balance=10000),
                 Transaction(amount=500, account=account1),
                 Transaction(amount=4500, account=account1),
                 Transaction(amount=6000, account=account2),
                 Transaction(amount = 4000,  account = account2)])

for account in session3.query(Account).all():
    owner = account.owner
    balance = account.balance
    spent_money = 0
    for account_transaction in account.transactions:
        spent_money += account_transaction.amount

    print("Account owner: " + str(owner) + '\t' +
          "Account balance: " + str(balance) + '\t' +
          "Spent money: " + str(spent_money))

