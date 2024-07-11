import json
import schedule
import time
from sqlalchemy import create_engine, Column, Integer, String, select
from sqlalchemy.orm import declarative_base, sessionmaker

# Define the database URL
DATABASE_URL = "postgresql+psycopg2://postgres:loch@localhost:5432/postgres"

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create a base class for our class definitions
Base = declarative_base()

# Define the User class which will be mapped to the 'users' table
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String)
    password = Column(String)

# Create the table if it doesn't exist
Base.metadata.create_all(engine)

# Create a sessionmaker bound to the engine
Session = sessionmaker(bind=engine)
session = Session()

def update_database():
    # Read and parse the JSON file
    with open('C:/m3/db/db.json', 'r') as file:
        data = json.load(file)

    # Fetch existing user IDs from the database to avoid duplicates
    existing_user_ids = {user_id for user_id in session.execute(select(User.id)).scalars().all()}

    # Insert the data into the database if not already present
    for user_data in data['users']:
        if user_data['id'] not in existing_user_ids:
            user = User(id=user_data['id'], email=user_data['email'], password=user_data['password'])
            session.add(user)

    # Commit the session to save the data
    session.commit()

    print("Data updated successfully!")

# Schedule the update_database function to run every 20 seconds
schedule.every(30).seconds.do(update_database)

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(1)
