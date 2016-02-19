import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Sport, Player, Base


engine = create_engine('sqlite:///sports.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

session.query(Player).delete()
session.commit()

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

session.add(Player(name="Bryan Habana", dob=datetime.date(1982,1,4), sport=rugby, photo='bryan.jpg'))
session.add(Player(name="Handre Pollard", dob=datetime.date(1982,1,4), sport=rugby, photo='handre.jpg'))
session.add(Player(name="Duane Vermeulen", dob=datetime.date(1982,1,4), sport=rugby, photo='duane.jpg'))

session.add(Player(name="AB de Villiers", dob=datetime.date(1982,1,4), sport=cricket, photo='ab.jpg'))
session.add(Player(name="Hashim Amla", dob=datetime.date(1982,1,4), sport=cricket, photo='hashim.jpg'))
session.add(Player(name="Dale Steyn", dob=datetime.date(1982,1,4), sport=cricket, photo='dale.jpg'))
session.add(Player(name="Quinton de Kock", dob=datetime.date(1982,1,4), sport=cricket, photo='quinton.jpg'))

session.add(Player(name="Ernie Else", dob=datetime.date(1982,1,4), sport=golf, photo='ernie.jpg'))
session.add(Player(name="Louis Oosthuizen", dob=datetime.date(1982,1,4), sport=golf, photo='louis.jpg'))

session.add(Player(name="Kevin Anderson", dob=datetime.date(1982,1,4), sport=tennis, photo='kevin.jpg'))

session.commit()
