from database import engine
import db_models as _db_models
import os
from sqlalchemy.orm import sessionmaker

def create_db():

    db_path = "flights_db.sqlite3"
    if not os.path.exists(db_path):
        _db_models.Base.metadata.create_all(bind=engine)

def check_db( flight_id ):

    session_init_chkdb = sessionmaker(bind=engine)
    session_chkdb = session_init_chkdb()

    record_count = session_chkdb.query(_db_models.FlightDB).filter_by(db_flightid=flight_id).count()
    session_chkdb.close()

    return record_count

def insert_db( flight_id,
                airlinecode,
                airlinenum,
                carrier_name,
                flight_status,
                flight_desc,
                dep_location,
                dep_airportname,
                dep_iata,
                dep_date,
                departure_time_scheduled,
                departure_time_actual,
                dep_terminal,
                dep_gate,
                arv_location,
                arv_airportname,
                arv_iata,
                arv_date,
                arrival_time_scheduled,
                arrival_time_actual,
                arv_terminal,
                arv_gate,
                arv_baggage,
                adtnl_equip_iata,
                adtnl_equip_name,
                adtnl_tailnumber,
                adtnl_callsign,
                adtnl_bearing,
                adtnl_heading,
                adtnl_fleetaircraftid ):

    session_init_insdb = sessionmaker(bind=engine)
    session_insdb = session_init_insdb()

    stmt = _db_models.FlightDB( db_flightid         = flight_id,
                                db_airline_code     = airlinecode,
                                db_flightnumber     = airlinenum,
                                db_carriername      = carrier_name,
                                db_flightstatus     = flight_status,
                                db_flightdesc       = flight_desc,
                                db_dep_location     = dep_location,
                                db_dep_airportname  = dep_airportname,
                                db_dep_iata         = dep_iata,
                                db_dep_dt_sched     = f"{dep_date}T{departure_time_scheduled}",
                                db_dep_dt_actual    = f"{dep_date}T{departure_time_actual}",
                                db_dep_terminal     = dep_terminal,
                                db_dep_gate         = dep_gate,
                                db_arv_location     = arv_location,
                                db_arv_airportname  = arv_airportname,
                                db_arv_iata         = arv_iata,
                                db_arv_dt_sched     = f"{arv_date}T{arrival_time_scheduled}",
                                db_arv_dt_actual    = f"{arv_date}T{arrival_time_actual}",
                                db_arv_terminal     = arv_terminal,
                                db_arv_gate         = arv_gate,
                                db_arv_baggage      = arv_baggage,
                                db_adtnl_equip_iata = adtnl_equip_iata,
                                db_adtnl_equip_name = adtnl_equip_name,
                                db_adtnl_tailnumber = adtnl_tailnumber,
                                db_adtnl_callsign   = adtnl_callsign,
                                db_adtnl_bearing    = adtnl_bearing,
                                db_adtnl_heading    = adtnl_heading,
                                db_fleetAircraftId  = adtnl_fleetaircraftid
                            )
    session_insdb.add(stmt)
    session_insdb.commit()
    session_insdb.close()



