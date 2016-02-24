import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Sport, Player, Base, User


engine = create_engine('sqlite:///sports.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

session.query(Player).delete()
session.commit()

session.query(Sport).delete()
session.commit()

session.query(User).delete()
session.commit()

cj = User(name="CJ", email="vssrcj@gmail.com")
session.add(cj)

rugby = Sport(name="Rugby")
session.add(rugby)

cricket = Sport(name="Cricket")
session.add(cricket)

golf = Sport(name="Golf")
session.add(golf)

tennis = Sport(name="Tennis")
session.add(tennis)

session.commit()

session.add(Player(name="Bryan Habana", dob=datetime.date(1982,1,4), sport=rugby, user=cj, photo='bryan.jpg'))
session.add(Player(name="Handre Pollard", dob=datetime.date(1982,1,4), sport=rugby, user=cj, photo='handre.jpg'))
session.add(Player(name="Duane Vermeulen", dob=datetime.date(1982,1,4), sport=rugby, user=cj, photo='duane.jpg'))

session.add(Player(name="AB de Villiers", dob=datetime.date(1982,1,4), sport=cricket, user=cj, photo='ab.jpg'))
session.add(Player(name="Hashim Amla", dob=datetime.date(1982,1,4), sport=cricket, user=cj, photo='hashim.jpg'))
session.add(Player(name="Dale Steyn", dob=datetime.date(1982,1,4), sport=cricket, user=cj, photo='dale.jpg'))
session.add(Player(name="Quinton de Kock", dob=datetime.date(1982,1,4), sport=cricket, user=cj, photo='quinton.jpg'))

session.add(Player(name="Ernie Else", dob=datetime.date(1982,1,4), sport=golf, user=cj, photo='ernie.jpg'))
session.add(Player(name="Louis Oosthuizen", dob=datetime.date(1982,1,4), sport=golf, user=cj, photo='louis.jpg'))

session.add(Player(name="Kevin Anderson", dob=datetime.date(1982,1,4), sport=tennis, user=cj, photo='kevin.jpg'))

session.commit()
