import sqlalchemy as db

engine = db.create_engine("sqlite:///./jimbell.db")

conn = engine.connect()

metadata = db.MetaData()
division =