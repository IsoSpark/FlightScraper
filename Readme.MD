# Web Scraping Project with DB insert
## A Web scraping project to scrape the data from https://www.flightstats.com/v2/flight-tracker<br/>

### Do these installs before running the project,<br/>
> pip install -r requirements.txt

### Run uvicon to create local ASGI server
> uvicorn main:app --reload

### URL Directory:
> Home( http://127.0.0.1:8000/ ) - nothing here. just a 

> Get Response URL( http://127.0.0.1:8000/getflight/?airlinecode=[airline code]]&airlinenum=[airline number]&departuredate=[departure_date] )

### To test the Get Response API Endpont, use the Get Response URL and modify the following parameters:
> [airline code] = 2 char airline code
> 
> [airlinenum] = 1 - 4 char airline number
> 
> [departure_date] = Departure Date
