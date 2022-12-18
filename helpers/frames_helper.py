from data.raw_train_frames import raw_train_frames
from data.raw_test_frames import raw_test_frames


def create_train_frame(
    text,
    intent,
    fromAirport=None,
    toAirport=None,
    departureDate=None,
    returnDate=None,
    maxBudget=None,
):
    frame = {
        "text": text,
        "intentName": intent,
    }
    if fromAirport or toAirport or departureDate or returnDate or maxBudget:
        frame["entityLabels"] = []
        if fromAirport:
            position = (
                text.find(fromAirport),
                text.find(fromAirport) + len(fromAirport) - 1,
            )
            frame["entityLabels"].append(
                {
                    "entityName": "From",
                    "startCharIndex": position[0],
                    "endCharIndex": position[1],
                    "children": [
                        {
                            "startCharIndex": position[0],
                            "endCharIndex": position[1],
                            "entityName": "Airport",
                        }
                    ],
                }
            )
        if toAirport:
            position = (text.find(toAirport), text.find(toAirport) + len(toAirport) - 1)
            frame["entityLabels"].append(
                {
                    "entityName": "To",
                    "startCharIndex": position[0],
                    "endCharIndex": position[1],
                    "children": [
                        {
                            "startCharIndex": position[0],
                            "endCharIndex": position[1],
                            "entityName": "Airport",
                        }
                    ],
                }
            )
        if departureDate:
            position = (
                text.find(departureDate),
                text.find(departureDate) + len(departureDate) - 1,
            )
            frame["entityLabels"].append(
                {
                    "entityName": "departureDate",
                    "startCharIndex": position[0],
                    "endCharIndex": position[1],
                    "children": [
                        {
                            "startCharIndex": position[0],
                            "endCharIndex": position[1],
                            "entityName": "datetimeV2",
                        }
                    ],
                }
            )
        if returnDate:
            position = (
                text.find(returnDate),
                text.find(returnDate) + len(returnDate) - 1,
            )
            frame["entityLabels"].append(
                {
                    "entityName": "returnDate",
                    "startCharIndex": position[0],
                    "endCharIndex": position[1],
                    "children": [
                        {
                            "startCharIndex": position[0],
                            "endCharIndex": position[1],
                            "entityName": "datetimeV2",
                        }
                    ],
                }
            )
        if maxBudget:
            position = (text.find(maxBudget), text.find(maxBudget) + len(maxBudget) - 1)
            frame["entityLabels"].append(
                {
                    "entityName": "maxBudget",
                    "startCharIndex": position[0],
                    "endCharIndex": position[1],
                }
            )
    return frame


def get_train_frames():
    return [
        create_train_frame(
            raw_frame["text"],
            raw_frame["intentName"],
            fromAirport=raw_frame["fromAirport"] if "fromAirport" in raw_frame.keys() else None,
            toAirport=raw_frame["toAirport"] if "toAirport" in raw_frame.keys() else None,
            departureDate=raw_frame["departureDate"]
            if "departureDate" in raw_frame.keys()
            else None,
            returnDate=raw_frame["returnDate"] if "returnDate" in raw_frame.keys() else None,
            maxBudget=raw_frame["maxBudget"] if "maxBudget" in raw_frame.keys() else None,
        )
        for raw_frame in raw_train_frames
    ]

def create_test_frame(
    text,
    intent,
    fromAirport=None,
    toAirport=None,
    departureDate=None,
    returnDate=None,
    maxBudget=None,
):
    frame = {
        "query": text,
        "text" : text,
        "intent": intent,
    }
    if fromAirport or toAirport or departureDate or returnDate or maxBudget:
        frame["entities"] = []
        if fromAirport:
            position = (
                text.find(fromAirport),
                text.find(fromAirport) + len(fromAirport) - 1,
            )
            frame["entities"].append(
                {
                    "entity": "From",
                    "startPos": position[0],
                    "endPos": position[1],
                }
            )
        if toAirport:
            position = (text.find(toAirport), text.find(toAirport) + len(toAirport) - 1)
            frame["entities"].append(
                {
                    "entity": "To",
                    "startPos": position[0],
                    "endPos": position[1],
                }
            )
        if departureDate:
            position = (
                text.find(departureDate),
                text.find(departureDate) + len(departureDate) - 1,
            )
            frame["entities"].append(
                {
                    "entity": "departureDate",
                    "startPos": position[0],
                    "endPos": position[1],
                }
            )
        if returnDate:
            position = (
                text.find(returnDate),
                text.find(returnDate) + len(returnDate) - 1,
            )
            frame["entities"].append(
                {
                    "entity": "returnDate",
                    "startPos": position[0],
                    "endPos": position[1],
                }
            )
        if maxBudget:
            position = (text.find(maxBudget), text.find(maxBudget) + len(maxBudget) - 1)
            frame["entities"].append(
                {
                    "entity": "maxBudget",
                    "startPos": position[0],
                    "endPos": position[1],
                }
            )
    else:
        frame["entities"] = []
    return frame


def get_test_frames():
    return [
        create_test_frame(
            raw_frame["text"],
            raw_frame["intent"],
            fromAirport=raw_frame["fromAirport"] if "fromAirport" in raw_frame.keys() else None,
            toAirport=raw_frame["toAirport"] if "toAirport" in raw_frame.keys() else None,
            departureDate=raw_frame["departureDate"]
            if "departureDate" in raw_frame.keys()
            else None,
            returnDate=raw_frame["returnDate"] if "returnDate" in raw_frame.keys() else None,
            maxBudget=raw_frame["maxBudget"] if "maxBudget" in raw_frame.keys() else None,
        )
        for raw_frame in raw_test_frames
    ]

def get_test_frame_for_batch_testing():
    return [
        create_train_frame(
            raw_frame["text"],
            raw_frame["intent"],
            fromAirport=raw_frame["fromAirport"] if "fromAirport" in raw_frame.keys() else None,
            toAirport=raw_frame["toAirport"] if "toAirport" in raw_frame.keys() else None,
            departureDate=raw_frame["departureDate"]
            if "departureDate" in raw_frame.keys()
            else None,
            returnDate=raw_frame["returnDate"] if "returnDate" in raw_frame.keys() else None,
            maxBudget=raw_frame["maxBudget"] if "maxBudget" in raw_frame.keys() else None,
        )
        for raw_frame in raw_test_frames
    ]
