import random
from faker import Faker
from app.database.db import SessionLocal
from sqlalchemy import exc
from sqlalchemy.orm import Session
from app.models import User, Video, Mapping, UserDetail,VideoDetail
from app.api.endpoints.costs import calculate_cost

fake_gen = Faker()
db: Session = SessionLocal()


def get_all_users_id() -> list:
    user_id_list: list[tuple] = db.query(User.id).all()
    return [id for id_tuple in user_id_list for id in id_tuple]


def get_all_videos_id() -> list:
    vid_id_list: list[tuple] = db.query(Video.id).all()
    return [id for id_tuple in vid_id_list for id in id_tuple]


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
        for _ in range(n):
            fake_video = {
                "title": fake_gen.name(),
                "desc": fake_gen.text(),
                "URI": fake_gen.file_path(),
            }
            db.add(Video(**fake_video))
        db.commit()
    except exc.SQLAlchemyError as err:
        print(
            f"error occured. \n Type : {type(err)} \n Description: {err}")


def generate_fake_videos_detail():
    vid_ids = get_all_videos_id()
    usr_ids = get_all_users_id()
    usr_limit = abs(len(vid_ids)-len(usr_ids))
    random.shuffle(usr_ids)
    try:
        for idx, id in enumerate(vid_ids):
            vid_len = random.randint(2, 600)  # in seconds
            vid_size = random.randint(1, 1024 ** 3)  # in bytes 2**30 < 2**32
            cost = calculate_cost(vid_size=vid_size, vid_length=vid_len)
            fake_video_detail = {
                "v_id": id,
                "len": vid_len,
                "size": vid_size,
                "type": random.choice(['mkv', 'mp4']),
                "upload_cost": cost
            }

            if idx < usr_limit:
                u_id = usr_ids[idx]
                user_det: UserDetail = db.query(UserDetail).filter(
                    u_id == UserDetail.u_id).first()
                if user_det:
                    user_det.total_spent += cost
                    user_det.vid_count += 1
                else:
                    user_detail = {
                        "u_id": u_id,
                        "vid_count": 1,
                        "total_spent": cost
                    }
                db.add(UserDetail(**user_detail))
            db.add(VideoDetail(**fake_video_detail))
        db.commit()
    except exc.SQLAlchemyError as err:
        print(
            f"error occured. \n Type : {type(err)} \n Description: {err}")


def generate_fake_mapping(n: int = 1):
    try:
        all_combinations = [
            (user, video) for user in get_all_users_id() for video in get_all_videos_id()]
        random.shuffle(all_combinations)
        for _ in range(n):
            while all_combinations:
                combination = all_combinations.pop()
                u_id, v_id = combination[0], combination[1]
                if not db.query(Mapping).filter(Mapping.u_id == u_id, Mapping.v_id == v_id).first():
                    break
            else:
                u_id, v_id = None, None
            if u_id and v_id:
                fake_mapping = {
                    "u_id": u_id,
                    "v_id": v_id
                }
                user: UserDetail = db.query(UserDetail).filter(
                    UserDetail.u_id == u_id).first()
                if user:
                    user.u_id += 1
                db.add(Mapping(**fake_mapping))
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
        generate_fake_mapping(20)
        generate_fake_videos_detail()
