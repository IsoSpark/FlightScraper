from dateutil import parser
from typing import Optional

def inputvalidateprocess( airlinecode: Optional[str] = None, airlinenum: Optional[str] = None, departuredate: Optional[str] = None ):

    error_msg = []

    if airlinecode is None or airlinecode.strip() == "":
        error_msg.append("Missing airline code")
    elif len(airlinecode) != 2:
        error_msg.append("Invalid airline code. 2-letter code only allowed")

    if airlinenum is None or airlinenum.strip() == "":
        error_msg.append("Missing flight number")
    elif len(airlinenum) > 4:
        error_msg.append("Invalid flight number. Maximum of 4 characters")

    if departuredate is None or departuredate.strip() == "":
        error_msg.append("Missing departure date")
    else:
        try:
            parser.parse( departuredate )
        except (ValueError, TypeError):
            error_msg.append("Incorrect departure date format")

    return error_msg