from helpers.luis_helper import Luis_manager
from helpers.frames_helper import get_train_frames

import csv


if __name__ == "__main__":
    luis = Luis_manager("0.1_upgraded")

    airports = []
    # from https://www.theguardian.com/news/datablog/2012/may/04/world-top-100-airports#data
    with open("./data/top100Ariports.csv", 'r') as file:
        csvreader = csv.reader(file)
        headings = next(csvreader)        
        for row in csvreader:
            code = row[2]
            name = row[3].split(',')[0]
            airports.append({"canonicalForm": name, "list": [code, name]})
    
    luis.update_closed_list("2325350f-c955-471d-ad38-012ae6c3d153", airports)

    # Create frames
    train_frames = get_train_frames()

    # Add example
    [luis.add_example(example) for example in train_frames]

    # Train
    luis.train()

    # Publish
    luis.publish()