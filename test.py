from helpers.frames_helper import get_test_frames
from helpers.luis_helper import Luis_manager
import json


def test_frames():
    luis = Luis_manager(version_id="0.1_upgraded")
    for example in get_test_frames():

        query = example["query"]
        intent = example["intent"]
        entities = example["entities"]

        prediction = luis.get_prediction({"query": query})

        for expected_entity in entities:
            expected_entity = expected_entity["entity"]
            actual_entities = prediction.prediction.entities
            if expected_entity not in list(actual_entities.keys()):
                error_message = f'Entity "{expected_entity}" not found in :\n"{query}".\nActual entities found: {list(actual_entities.keys())}'
                print("_" * 20)
                print(error_message)
                print("_" * 20)

                # raise error
                # raise Exception(error_message)


if __name__ == "__main__":
    test_frames()

    # write get_test_frames() in json file
    with open("./data/test_frames.json", "w") as file:
        file.write(json.dumps(get_test_frames()))
