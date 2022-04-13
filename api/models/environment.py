from . import db

from dotenv import load_dotenv
from datetime import datetime
import os

load_dotenv()


class EnvironmentConfig(db.Model):
    __tablename__ = "environmentconfig"

    id = db.Column(db.Integer, primary_key=True)
    lights_on_time = db.Column(db.Time, nullable=False)
    lights_off_time = db.Column(db.Time, nullable=False)
    day_h_sp = db.Column(db.Float, nullable=False)
    day_l_sp = db.Column(db.Float, nullable=False)
    night_h_sp = db.Column(db.Float, nullable=False)
    night_l_sp = db.Column(db.Float, nullable=False)
    humidity_high_sp = db.Column(db.Float, nullable=False)
    humidity_low_sp = db.Column(db.Float, nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow)

    @staticmethod
    def to_dict(config, *args, **kwargs):
        if config is None:
            return {}

        return dict(
            lights_on_time=config.lights_on_time.isoformat(),
            lights_off_time=config.lights_off_time.isoformat(),
            day_h_sp=config.day_h_sp,
            day_l_sp=config.day_l_sp,
            night_h_sp=config.night_h_sp,
            night_l_sp=config.night_l_sp,
            humidity_high_sp=config.humidity_high_sp,
            humidity_low_sp=config.humidity_low_sp,
            created=config.created.isoformat(),
        ) 

    @staticmethod
    def factory(**kwargs):
        env = EnvironmentConfig()
        env.lights_on_time = kwargs.get("lights_on_time", datetime.strptime(os.environ.get("LIGHTS_ON_TIME"), "%H:%M:%S").time())
        env.lights_off_time = kwargs.get("lights_off_time", datetime.strptime(os.environ.get("LIGHTS_OFF_TIME"), "%H:%M:%S").time())
        env.day_h_sp = kwargs.get("day_h_sp", os.environ.get("DAY_H_SP"))
        env.day_l_sp = kwargs.get("day_l_sp", os.environ.get("DAY_L_SP"))
        env.night_h_sp = kwargs.get("night_h_sp", os.environ.get("NIGHT_H_SP"))
        env.night_l_sp = kwargs.get("night_l_sp", os.environ.get("NIGHT_L_SP"))
        env.humidity_high_sp = kwargs.get("humidity_high_sp", os.environ.get("HUMIDITY_HIGH_SP"))
        env.humidity_low_sp = kwargs.get("humidity_low_sp", os.environ.get("HUMIDITY_LOW_SP"))

        db.session.add(env)
        db.session.commit()
        return env
