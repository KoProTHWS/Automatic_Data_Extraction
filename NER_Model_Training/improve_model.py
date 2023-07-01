import spacy
from spacy.tokens import DocBin
from spacy.training import Example
import random
import time
# new training data should be supplied from separate .py file
from training_data.data_12_05_4 import TRAIN_DATA

start_time = time.time()

def convert_data(data):
    converted_data = []
    for text, annotations in data:
        entities = annotations['entities']
        converted_entities = []
        for entity in entities:
            start_token, label = entity
            tokens = text.split()
            start_char = len(' '.join(tokens[:start_token])) + (1 if start_token > 0 else 0)
            end_char = start_char + len(tokens[start_token]) 
            converted_entities.append((start_char, end_char, label))
        converted_data.append((text, {"entities": converted_entities}))
    return converted_data

training_data = convert_data(TRAIN_DATA)


# While training for the first time, load exisitng pretrained model like de_core_news_sm
# to train model that has already been train for some NER label with new dataset- load the same model to train
# nlp = spacy.load("de_core_news_sm")
nlp = spacy.load("C:/Users/Varun Kaarthik/Documents/cad_data_extraction/NER_Model_Training/trained_models/de_core_news_sm_with_TOOL")

# Get the NER pipeline
ner = nlp.get_pipe("ner")


# Disable other pipeline components
other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]

# Import training data from the separate .py file

# Prepare the training data for spacy 3.0
examples = []
for text, annots in training_data:
    doc = nlp.make_doc(text)
    example = Example.from_dict(doc, annots)
    examples.append(example)

# Only train NER
with nlp.disable_pipes(*other_pipes):  # only train NER
    for i in range(30):  # Number of epochs. Change it to what suits you.
        random.shuffle(examples)
        for batch in spacy.util.minibatch(examples, size=3):  # Change the minibatch size based on your requirements
            nlp.update(batch)

# Save the trained model
# nlp.to_disk("/path/to/your/model")


nlp.to_disk("C:/Users/Varun Kaarthik/Documents/cad_data_extraction/NER_Model_Training/trained_models/de_core_news_sm_with_TOOL")

end_time = time.time()
print(f"Execution time: {end_time - start_time} seconds")
