import scraper as _scraper
import inputvalidate as _inputvalidate
from fastapi import FastAPI, HTTPException
from typing import Optional

app = FastAPI()

@app.get("/")
async def root():
    return {"message": f"Hello, this is a web scraper for flightstats flight tracker (https://www.flightstats.com/v2/flight-tracker) webpage"}

# this pulls the airline code, airline number and departure date in the get request url
@app.get("/getflight/")
async def getflight( airlinecode: Optional[str] = None, airlinenum: Optional[str] = None, departuredate: Optional[str] = None ):

    error_msg_main = _inputvalidate.inputvalidateprocess(airlinecode, airlinenum, departuredate)

    if error_msg_main and len(error_msg_main) > 0:

        raise HTTPException(status_code=404, detail=error_msg_main)

    else:
        return _scraper.flightscrape(airlinecode, airlinenum, departuredate)
