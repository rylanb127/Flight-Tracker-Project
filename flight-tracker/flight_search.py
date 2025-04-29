import pandas as pd
import random
from datetime import datetime

def generate_mock_flights():
    airports_us = ["JFK", "LAX", "ORD", "ATL", "DFW", "DEN", "SFO", "MIA", "SEA", "NWA"]
    airports_eu = ["LHR", "CDG", "FRA", "AMS", "MAD", "ZRH", "BRU", "FCO", "DUB", "BCN"]
    airlines = ["Delta", "United", "American", "Lufthansa", "Air France", "British Airways", "KLM", "Swiss"]
    classes = ["Economy", "Business", "First Class"]
    flights = []

    today = datetime.today()
    for _ in range(1000):
        dep = random.choice(airports_us)
        dest = random.choice(airports_eu)
        airline = random.choice(airlines)
        flight_class = random.choice(classes)
        stops = random.choice([0, 1])
        baggage_fee = random.choice([0, 25, 50])
        price = random.randint(800, 2500) if flight_class == "First Class" else random.randint(400, 1200)

        departure_date = today + pd.to_timedelta(random.randint(1, 730), unit="d")
        return_date = departure_date + pd.to_timedelta(random.randint(3, 14), unit="d")

        flights.append({
            "airline": airline,
            "price": price,
            "departure_date": departure_date.strftime('%Y-%m-%d'),
            "return_date": return_date.strftime('%Y-%m-%d'),
            "class": flight_class,
            "stops": stops,
            "baggage_fee": baggage_fee,
            "departure": dep,
            "destination": dest
        })

    # Special guaranteed flight for testing
    flights.append({
        "airline": "TestAir",
        "price": 999,
        "departure_date": "2025-06-10",
        "return_date": "2025-06-20",
        "class": "Business",
        "stops": 1,
        "baggage_fee": 30,
        "departure": "DFW",
        "destination": "BRU"
    })
    return flights

def fetch_flight_prices(origin, destination, depart_date, return_date, preferred_class="Economy", flight_type="Direct"):
    flights = generate_mock_flights()
    df = pd.DataFrame(flights)

    df["departure_date"] = pd.to_datetime(df["departure_date"])
    df["return_date"] = pd.to_datetime(df["return_date"])
    depart_date = pd.to_datetime(depart_date)
    return_date = pd.to_datetime(return_date)

    df = df[(df["departure"] == origin) & (df["destination"] == destination)]
    df = df[(df["departure_date"] >= depart_date) & (df["return_date"] <= return_date)]
    df = df[df["class"] == preferred_class]

    if flight_type == "Direct":
        df = df[df["stops"] == 0]
    elif flight_type == "Layover":
        df = df[df["stops"] > 0]

    if df.empty:
        return {"error": "No flights found that match your search criteria."}
    else:
        df = df.sort_values(by="price").head(3)  # ✅ Top 3 cheapest flights

        flights_list = []
        for _, row in df.iterrows():
            flights_list.append({
                "airline": row["airline"],
                "price": f"${row['price']}",
                "departure_date": str(row["departure_date"].date()),
                "return_date": str(row["return_date"].date()),
                "flight_class": row["class"],
                "stops": int(row["stops"]),  # ✅ Force to Python int
                "baggage_fee": f"${row['baggage_fee']}",
                "origin": row["departure"],
                "destination": row["destination"]
            })

        return {"flights": flights_list}
