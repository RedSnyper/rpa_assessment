import random
from faker import Faker
from . import SessionLocal
from sqlalchemy import exc
from sqlalchemy.orm import Session
from ..models import User, Video


fake_gen = Faker()
db: Session = SessionLocal()

def get_all_users_id() -> list:
    user_id_list: list[tuple] = db.query(User.u_id).all()
    return [id for id_tuple in user_id_list for id in id_tuple]

def generate_fake_user(n: int = 1) -> None:
        try:
            for _ in range(n):
                fake_user = {
                    "full_name": fake_gen.name(),
                    "email": fake_gen.email(),
                    "password": fake_gen.password()
                }
                db.add(User(**fake_user))
                db.commit()
        except exc.SQLAlchemyError as err:
            print(
                f"error occured. \n Type : {type(err)} \n Description: {err}")

def generate_fake_videos(n: int = 1) -> None:
        try:
            user_ids:list = get_all_users_id()
            for _ in range(n):
                u_id = random.choice(user_ids)
                user:User = db.query(User).filter(User.u_id == u_id).first()
                user.vid_count += 1
                fake_video = {
                    "vid_title": fake_gen.name(),
                    "vid_desc": fake_gen.text(),
                    "vid_URI": fake_gen.file_path(),
                    "vid_len": random.randint(1, 600),  #in seconds
                    "vid_size": random.randint(1, 1024 ** 3) ,#in bytes 2**30 < 2**32 
                    "vid_type": random.choice(['mkv','mp4']),
                    "upload_cost": round(random.uniform(17, 40),2),
                    "u_id": u_id
                }            
                db.add(Video(**fake_video))
                db.commit()
        except exc.SQLAlchemyError as err:
            print(
                f"error occured. \n Type : {type(err)} \n Description: {err}")

def generate_fake_data():
    if db.query(User).first() and db.query(Video).first():
        pass
    else:
        generate_fake_user(20)
        generate_fake_videos(30)