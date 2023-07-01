import spacy
from spacy.tokens import DocBin
from spacy.training import Example
import random

from training_data.data_11_05 import TRAIN_DATA

# While training for the first time, load exisitng pretrained model like de_core_news_sm
# to train model that has already been train for some NER label with new dataset- load the same model to train
nlp = spacy.load("de_core_news_sm")

# 2. Get the NER pipeline
ner = nlp.get_pipe("ner")

# Add the new label when training for the first time (new label training)
ner.add_label("TOOL")

# 4. Disable other pipeline components
other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]

# 5. Import training data from the separate .py file

# 6. Prepare the training data for spacy 3.0
examples = []
for text, annots in TRAIN_DATA:
    doc = nlp.make_doc(text)
    example = Example.from_dict(doc, annots)
    examples.append(example)

# 7. Only train NER
with nlp.disable_pipes(*other_pipes):  # only train NER
    for i in range(20):  # Number of epochs. Change it to what suits you.
        random.shuffle(examples)
        for batch in spacy.util.minibatch(examples, size=3):  # Change the minibatch size based on your requirements
            nlp.update(batch)

# 8. Save the trained model
# nlp.to_disk("/path/to/your/model")
nlp.to_disk("C:/Users/Varun Kaarthik/Documents/cad_data_extraction/NER_Model_Training/trained_models/de_core_news_sm_with_TOOL")
