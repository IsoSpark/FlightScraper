import requests
import random
import json
import db_function as _db_function
from dateutil import parser
from bs4 import BeautifulSoup
from jsonpath_ng import parse
from fastapi import HTTPException
from typing import Optional

def flightscrape( airlinecode: Optional[str] = None, airlinenum: Optional[str] = None, departuredate: Optional[str] = None ):

    #parses the date to detect the month, day and year
    departuredate_parsed = parser.parse( departuredate )
    departuredate_year = departuredate_parsed.year
    departuredate_month = departuredate_parsed.month
    departuredate_day = departuredate_parsed.day

    url = f"https://www.flightstats.com/v2/flight-tracker/{airlinecode}/{airlinenum}?year={departuredate_year}&month={departuredate_month}&date={departuredate_day}"

    #list user agents
    web_user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0"
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/127.0.6533.107 Mobile/15E148 Safari/604.1"
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 14.6; rv:129.0) Gecko/20100101 Firefox/129.0"
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_6_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15"
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_6_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 OPR/112.0.0.0"
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_6_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1"
        "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.103 Mobile Safari/537.36"
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.2651.98"
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 OPR/112.0.0.0"
    ]

    headers = {
        "User-Agent": random.choice(web_user_agents) #randomizes the user agents to not be detected as a bot
    }

    # Set get request to flightstats website
    response = requests.get(url, headers=headers)

    # Parse HTML
    soup = BeautifulSoup(response.text, "html.parser")

    # Find the <script> tag containing "__NEXT_DATA__"
    script_tag = soup.find("script", text=lambda text: text and "__NEXT_DATA__" in text)

    # If script with __NEXT_DATA__ is found
    if script_tag:
        # Extract JSON-like data inside the script tag
        json_text = script_tag.string.strip()

        # Remove the unnecessary JS variable assignment part
        json_text = json_text.replace("__NEXT_DATA__ = ", "").split(";__NEXT_LOADED_PAGES__")[0]

        json_data = json.loads(json_text)

        flight_id = next((match.value for match in parse("$.props.initialState.flightTracker.flight.flightId").find(json_data)) , None)

        if flight_id is None:

            raise HTTPException(status_code=404, detail=f"Record for {airlinecode}{airlinenum} on date {departuredate} not found")

        else:

            #variable assignment for return response

            flight_status = next((match.value for match in parse("$.props.initialState.flightTracker.flight.status.status").find(json_data)) , None)
            flight_desc = next((match.value for match in parse("$.props.initialState.flightTracker.flight.status.statusDescription").find(json_data)) , None)
            carrier_name = next((match.value for match in parse("$.props.initialState.flightTracker.flight.resultHeader.carrier.name").find(json_data)) , None)

            dep_airportname = next((match.value for match in parse("$.props.initialState.flightTracker.flight.departureAirport.name").find(json_data)), None)
            dep_city = next((match.value for match in parse("$.props.initialState.flightTracker.flight.departureAirport.city").find(json_data)), None)
            dep_state = next((match.value for match in parse("$.props.initialState.flightTracker.flight.departureAirport.state").find(json_data)), None)
            dep_country = next((match.value for match in parse("$.props.initialState.flightTracker.flight.departureAirport.country").find(json_data)), None)
            dep_iata = next((match.value for match in parse("$.props.initialState.flightTracker.flight.departureAirport.iata").find(json_data)), None)
            dep_date = next((match.value for match in parse("$.props.initialState.flightTracker.flight.departureAirport.date").find(json_data)), None)
            dep_time_sched = next((match.value for match in parse("$.props.initialState.flightTracker.flight.departureAirport.times.scheduled.time24").find(json_data)), None)
            dep_time_sched_timezone = next((match.value for match in parse("$.props.initialState.flightTracker.flight.departureAirport.times.scheduled.timezone").find(json_data)), None)
            dep_time_actual = next((match.value for match in parse("$.props.initialState.flightTracker.flight.departureAirport.times.estimatedActual.time24").find(json_data)), None)
            dep_time_actual_timezone = next((match.value for match in parse("$.props.initialState.flightTracker.flight.departureAirport.times.estimatedActual.timezone").find(json_data)), None)
            dep_terminal = next((match.value for match in parse("$.props.initialState.flightTracker.flight.departureAirport.terminal").find(json_data)), None)
            dep_gate = next((match.value for match in parse("$.props.initialState.flightTracker.flight.departureAirport.gate").find(json_data)), None)

            arv_city = next((match.value for match in parse("$.props.initialState.flightTracker.flight.arrivalAirport.city").find(json_data)), None)
            arv_state = next((match.value for match in parse("$.props.initialState.flightTracker.flight.arrivalAirport.state").find(json_data)), None)
            arv_country = next((match.value for match in parse("$.props.initialState.flightTracker.flight.arrivalAirport.country").find(json_data)), None)
            arv_airportname = next((match.value for match in parse("$.props.initialState.flightTracker.flight.arrivalAirport.name").find(json_data)), None)
            arv_iata = next((match.value for match in parse("$.props.initialState.flightTracker.flight.arrivalAirport.iata").find(json_data)), None)
            arv_date = next((match.value for match in parse("$.props.initialState.flightTracker.flight.arrivalAirport.date").find(json_data)), None)
            arv_time_sched = next((match.value for match in parse("$.props.initialState.flightTracker.flight.arrivalAirport.times.scheduled.time24").find(json_data)), None)
            arv_time_sched_timezone = next((match.value for match in parse("$.props.initialState.flightTracker.flight.arrivalAirport.times.scheduled.timezone").find(json_data)), None)
            arv_time_actual = next((match.value for match in parse("$.props.initialState.flightTracker.flight.arrivalAirport.times.estimatedActual.time24").find(json_data)), None)
            arv_time_actual_timezone = next((match.value for match in parse("$.props.initialState.flightTracker.flight.arrivalAirport.times.estimatedActual.timezone").find(json_data)), None)
            arv_terminal = next((match.value for match in parse("$.props.initialState.flightTracker.flight.arrivalAirport.terminal").find(json_data)), None)
            arv_gate = next((match.value for match in parse("$.props.initialState.flightTracker.flight.arrivalAirport.gate").find(json_data)), None)
            arv_baggage = next((match.value for match in parse("$.props.initialState.flightTracker.flight.arrivalAirport.baggage").find(json_data)), None)
            adtnl_equip_iata = next((match.value for match in parse("$.props.initialState.flightTracker.flight.additionalFlightInfo.equipment.iata").find(json_data)), None)
            adtnl_tailnumber = next((match.value for match in parse("$.props.initialState.flightTracker.flight.positional.flexTrack.tailNumber").find(json_data)), None)
            adtnl_equip_name = next((match.value for match in parse("$.props.initialState.flightTracker.flight.additionalFlightInfo.equipment.name").find(json_data)), None)
            adtnl_callsign = next((match.value for match in parse("$.props.initialState.flightTracker.flight.positional.flexTrack.callsign").find(json_data)), None)
            adtnl_bearing = next((match.value for match in parse("$.props.initialState.flightTracker.flight.positional.flexTrack.bearing").find(json_data)), None)
            adtnl_heading = next((match.value for match in parse("$.props.initialState.flightTracker.flight.positional.flexTrack.heading").find(json_data)), None)
            adtnl_fleetaircraftid = next((match.value for match in parse("$.props.initialState.flightTracker.flight.positional.flexTrack.fleetAircraftId").find(json_data)), None)

            if dep_date is not None:
                dep_date = parser.parse(dep_date).strftime("%Y-%m-%d")

            if arv_date is not None:
                arv_date = parser.parse(arv_date).strftime("%Y-%m-%d")

            if dep_state is None:
                dep_location = f"{dep_city}, {dep_country}"
            else:
                dep_location = f"{dep_city}, {dep_state}, {dep_country}"

            if arv_state is None:
                arv_location = f"{arv_city}, {arv_country}"
            else:
                arv_location = f"{arv_city}, {arv_state}, {arv_country}"

            if dep_time_sched is None and dep_time_sched_timezone is None:
                departure_time_scheduled = None
            else:
                departure_time_scheduled =  f"{dep_time_sched} {dep_time_sched_timezone}"

            if dep_time_actual is None and dep_time_actual_timezone is None:
                departure_time_actual = None
            else:
                departure_time_actual =  f"{dep_time_actual} {dep_time_actual_timezone}"

            if arv_time_sched is None and arv_time_sched_timezone is None:
                arrival_time_scheduled = None
            else:
                arrival_time_scheduled =  f"{arv_time_sched} {arv_time_sched_timezone}"

            if arv_time_actual is None and arv_time_actual_timezone is None:
                arrival_time_actual = None
            else:
                arrival_time_actual =  f"{arv_time_actual} {arv_time_actual_timezone}"

            # db logic

            # call logic for DB creation
            _db_function.create_db()

            # check db if record already exist
            record_exists_count = _db_function.check_db(flight_id)

            if record_exists_count == 0:
            # call logic for DB insert
                _db_function.insert_db( flight_id,
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
                                        adtnl_fleetaircraftid
                                      )

            # return response mapping

            return{

                "mainflightdetails": {

                    "flightId": flight_id,
                    "airlineCode": airlinecode,
                    "flightNumber": airlinenum,
                    "carrierName": carrier_name,
                    "flightStatus": flight_status,
                    "flightDesc": flight_desc,

                    "departureInfo": {
                        "departureLocation": dep_location,
                        "departureAirporName": dep_airportname,
                        "departureAirportIATACode": dep_iata,
                        "depatureDate": dep_date,
                        "departureTimeScheduled": departure_time_scheduled,
                        "departureTimeActual": departure_time_actual,
                        "departureTerminal": dep_terminal,
                        "departureGate": dep_gate
                    },

                    "arrivalInfo": {
                        "arrivalLocation": arv_location,
                        "arrivalAirporName": arv_airportname,
                        "arrivalAirportIATACode": arv_iata,
                        "arrivalate": arv_date,
                        "arrivalTimeScheduled": arrival_time_scheduled,
                        "arrivalTimeActual": arrival_time_actual,
                        "arrivalTerminal": arv_terminal,
                        "arrivalGate": arv_gate,
                        "arrivalBaggage": arv_baggage,
                    },

                    "additionalInformation": {
                        "equipmentIATACode": adtnl_equip_iata,
                        "equipmentName": adtnl_equip_name,
                        "tailNumber": adtnl_tailnumber,
                        "callsign": adtnl_callsign,
                        "bearing": adtnl_bearing,
                        "heading": adtnl_heading,
                        "fleetAircraftId": adtnl_fleetaircraftid,
                    },
                },
            }