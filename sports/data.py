import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Sport, Player, Base


engine = create_engine('sqlite:///sports.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

session.query(Sport).delete()
session.commit()

rugby = Sport(name="Rugby")
session.add(rugby)

cricket = Sport(name="Cricket")
session.add(cricket)

golf = Sport(name="Golf")
session.add(golf)

tennis = Sport(name="Tennis")
session.add(tennis)

session.commit()

session.add(Player(name="Bryan Habana", dob=datetime.date(1982,1,4), sport=rugby))
session.add(Player(name="Fourie du Preez", dob=datetime.date(1982,1,4), sport=rugby))
session.add(Player(name="Dwyane Vermeulen", dob=datetime.date(1982,1,4), sport=rugby))

session.add(Player(name="AB de Villiers", dob=datetime.date(1982,1,4), sport=cricket))
session.add(Player(name="Hashim Amla", dob=datetime.date(1982,1,4), sport=cricket))
session.add(Player(name="Dale Steyn", dob=datetime.date(1982,1,4), sport=cricket))
session.add(Player(name="Kagiso Rabada", dob=datetime.date(1982,1,4), sport=cricket))

session.add(Player(name="Ernie Else", dob=datetime.date(1982,1,4), sport=golf))
session.add(Player(name="Trevor Immelman", dob=datetime.date(1982,1,4), sport=golf))

session.add(Player(name="Wesley Moodey", dob=datetime.date(1982,1,4), sport=tennis))

session.commit()
