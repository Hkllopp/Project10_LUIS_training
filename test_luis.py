from helpers.frames_helper import get_test_frames
from helpers.luis_helper import Luis_manager
import json
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import MultiLabelBinarizer
import warnings
import pytest
import sys


def test_intent():
    luis = Luis_manager(version_id="0.1_upgraded")
    for example in get_test_frames():
        query = example["query"]
        intent = example["intent"]

        prediction = luis.get_prediction({"query": query})

        if prediction.prediction.top_intent != intent:
            error_message = f'Intent "{intent}" not predicted in :"{query}".Predicted intent: {prediction.prediction.top_intent}'

            # raise error
            raise Exception(error_message)


def test_entities():
    luis = Luis_manager(version_id="0.1_upgraded")
    for example in get_test_frames():
        query = example["query"]
        entities = example["entities"]

        prediction = luis.get_prediction({"query": query})

        for expected_entity in entities:
            expected_entity = expected_entity["entity"]
            actual_entities = prediction.prediction.entities
            if expected_entity not in list(actual_entities.keys()):
                error_message = f'Entity "{expected_entity}" not found in :"{query}". Actual entities found: {list(actual_entities.keys())}'

                # raise warning
                warnings.warn(error_message)


def test_accuracy():
    luis = Luis_manager(version_id="0.1_upgraded")
    accuracy_threshold_intent = 0.7
    accuracy_threshold_entities = 0.3

    test_frames = get_test_frames()

    predictions = [
        luis.get_prediction({"query": frame["query"]}) for frame in test_frames
    ]
    predictions_intents = [
        prediction.prediction.top_intent for prediction in predictions
    ]
    predictions_entities = [
        list(prediction.prediction.entities.keys()) for prediction in predictions
    ]

    actual_intents = [frame["intent"] for frame in test_frames]
    actual_entities = [
        [entity["entity"] for entity in frame["entities"]] for frame in test_frames
    ]

    mlb = MultiLabelBinarizer()
    mlb.fit(actual_entities)
    actual_entities_binary = mlb.transform(actual_entities)
    predictions_entities_binary = mlb.transform(predictions_entities)

    intent_accuracy = accuracy_score(actual_intents, predictions_intents)
    entities_accuracy = accuracy_score(
        actual_entities_binary, predictions_entities_binary
    )

    if intent_accuracy < accuracy_threshold_intent:
        raise Exception(
            f"Intent accuracy {intent_accuracy} is below threshold {accuracy_threshold_intent}"
        )
    
    if entities_accuracy < accuracy_threshold_entities:
        raise Exception(
            f"Entities accuracy {entities_accuracy} is below threshold {accuracy_threshold_entities}"
        )
if __name__ == "__main__":
    sys.exit(pytest.main())

    # write get_test_frames() in json file
    with open("./data/test_frames.json", "w") as file:
        file.write(json.dumps(get_test_frames()))
