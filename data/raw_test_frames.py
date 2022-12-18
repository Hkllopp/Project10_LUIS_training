raw_test_frames = [
    {
        "text": "Hi ! I'd like to make a reservation. I want to go to France, maybe Paris but from Toronto. I do not know when I'm returning but I'm planning on leaving the 02/02/2022. I have 600 dollars to spend",
        "intent": "BookFlight",
        "fromAirport": "Toronto",
        "toAirport": "Paris",
        "departureDate": "02/02/2022",
        "maxBudget": "600",
    },
    {
        "text": "I want to search a flight.",
        "intent": "BookFlight",
    },
    {
        "text": "I search a flight to go to LAX but less than 200 dollars. I will leave from CDG on 2017-12-12 and I will return on 2017-12-15.",
        "intent": "BookFlight",
        "fromAirport": "CDG",
        "toAirport": "LAX",
        "maxBudget": "200",
        "departureDate": "2017-12-12",
        "returnDate": "2017-12-15",
    },
    {"text": "STOP", "intent": "Cancel"},
]
