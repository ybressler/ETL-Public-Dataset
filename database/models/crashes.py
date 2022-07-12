"""SQLAlchemy model for crashes"""
import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    Date,
    Time,
    Boolean,
    func
)

# app stuff
from database.models.base import Base

# ------------------------------------------------------------------------------

class CrashRecord(Base):
    """
    A table representing all edits made.

    This needs to be refactored (and replaced by somethign more meaningful)
    """

    __tablename__ = "crash_records"

    # Primary key first
    collision_id = Column(Integer, primary_key=True, autoincrement=False, nullable=False)
    is_valid = Column(Boolean, default=True)
    crash_date = Column(Date, nullable=False, comment='Occurrence date of collision')
    crash_time = Column(Time, nullable=False, comment='Occurrence time of collision')
    crash_date_time = Column(DateTime(timezone=True), nullable=False, index=True, comment='Occurrence datetime of collision - automatically calculated by combining crash_date and crash_time.')
    borough = Column(Text, nullable=True, comment='Borough where collision occurred. If not in a specific borough, value will be None')
    zip_code = Column(Text, nullable=True, comment='Postal code of incident occurrence')
    latitude = Column(Text, nullable=True,comment='Latitude coordinate for Global Coordinate System, WGS 1984, decimal degrees (EPSG 4326)')
    longitude = Column(Text, nullable=True, comment='Longitude coordinate for Global Coordinate System, WGS 1984, decimal degrees (EPSG 4326)')
    on_street_name = Column(Text, nullable=True, comment='Street on which the collision occurred')
    off_street_name = Column(Text, nullable=True, comment='Nearest cross street to the collision')
    cross_street_name = Column(Text, nullable=True, comment='Street address if known')

    # A bit tedious, would be nice to creater this in a loop
    number_of_persons_injured = Column(Integer, default=0, comment='Number of persons injured')
    number_of_persons_killed = Column(Integer, default=0, comment='Number of persons killed')
    number_of_cyclist_injured = Column(Integer, default=0, comment='Number of cyclists injured')
    number_of_cyclist_killed = Column(Integer, default=0, comment='Number of cyclists killed')
    number_of_pedestrians_injured = Column(Integer, default=0, comment='Number of pedestrians injured')
    number_of_pedestrians_killed = Column(Integer, default=0, comment='Number of pedestrians killed')
    number_of_motorist_injured = Column(Integer, default=0, comment='Number of motorists injured')
    number_of_motorist_killed = Column(Integer, default=0, comment='Number of motorists killed')

    # This too is a bit tedious
    contributing_factor_vehicle_1 = Column(Text, nullable=True, comment='Factors contributing to the collision for designated vehicle')
    contributing_factor_vehicle_2 = Column(Text, nullable=True, comment='Factors contributing to the collision for designated vehicle')
    contributing_factor_vehicle_3 = Column(Text, nullable=True, comment='Factors contributing to the collision for designated vehicle')
    contributing_factor_vehicle_4 = Column(Text, nullable=True, comment='Factors contributing to the collision for designated vehicle')
    contributing_factor_vehicle_5 = Column(Text, nullable=True, comment='Factors contributing to the collision for designated vehicle')

    vehicle_type_code1 = Column(Text, nullable=True, comment='Type of vehicle based on the selected vehicle category (ATV, bicycle, car/suv, ebike, escooter, truck/bus, motorcycle, other)')
    vehicle_type_code2 = Column(Text, nullable=True, comment='Type of vehicle based on the selected vehicle category (ATV, bicycle, car/suv, ebike, escooter, truck/bus, motorcycle, other)')
    vehicle_type_code_3 = Column(Text, nullable=True, comment='Type of vehicle based on the selected vehicle category (ATV, bicycle, car/suv, ebike, escooter, truck/bus, motorcycle, other)')
    vehicle_type_code_4 = Column(Text, nullable=True, comment='Type of vehicle based on the selected vehicle category (ATV, bicycle, car/suv, ebike, escooter, truck/bus, motorcycle, other)')
    vehicle_type_code_5 = Column(Text, nullable=True, comment='Type of vehicle based on the selected vehicle category (ATV, bicycle, car/suv, ebike, escooter, truck/bus, motorcycle, other)')

    # Metadata
    inserted_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), default=datetime.datetime.utcnow)
