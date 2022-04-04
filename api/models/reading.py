from sqlalchemy import func

from datetime import datetime, timedelta, timezone

from . import db


class Reading(db.Model):  
    __tablename__ = "reading"

    id = db.Column(db.Integer, primary_key=True)
    temperature = db.Column(db.Float, nullable=False)
    humidity = db.Column(db.Float, nullable=False)
    time = db.Column(db.DateTime, default=datetime.utcnow)

    @staticmethod
    def find(*args, **kwargs):
        query = Reading.query
        
        if kwargs.get("period"):
            days = 0
            hours = 0
            minutes = 0

            if "days" in kwargs["period"]:
                days = int(kwargs["period"].split("days=")[1])
            elif "hours" in kwargs["period"]:
                hours = int(kwargs["period"].split("hours=")[1])
            elif "minutes" in kwargs["period"]:
                minutes = int(kwargs["period"].split("minutes=")[1])

            now = datetime.now(timezone.utc)
            delta = timedelta(days=days, hours=hours, minutes=minutes)
            query = query.filter(Reading.time <= now, Reading.time >= (now - delta))
        
        if kwargs.get("dateFrom"):
            _from = datetime.strptime(kwargs.get("dateFrom"), "%Y-%m-%d").date()
            query = query.filter(Reading.time >= _from)
        
        if kwargs.get("dateTo"):
            """ For unknown reasons the lte operator is having a hissy fit so instead we take the date
            chosen and add a day then use the lt operator to get the correct query range """

            _to = datetime.strptime(kwargs.get("dateTo"), "%Y-%m-%d").date() + timedelta(days=1)
            query = query.filter(Reading.time < _to)
        
        query = query.order_by(Reading.time)
        return query
    
    @staticmethod
    def to_dict(queryset, *args, **kwargs):
        readings = [
            dict(temp=r.temperature, hum=r.humidity, time=r.time.isoformat()) 
            for r in queryset.all()
        ]
        return readings
