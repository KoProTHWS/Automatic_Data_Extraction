import spacy
import re
import datetime
import os

# Load trained NER model
nlp = spacy.load("C:/Users/Varun Kaarthik/Documents/cad_data_extraction/NER_Model_Training/trained_models/de_core_news_sm_with_TOOL")


evaluation_data = [
    ("Kannst du mir bitte den Hammer geben?", [(24, 30, "TOOL")]),
    ("Wo ist der Schraubendreher? Ich muss etwas reparieren.", [(11, 27, "TOOL")]),
    ("Ich brauche einen Akkuschrauber, um das Regal zusammenzubauen.", [(18, 31, "TOOL")]),
    ("Ich habe den Bohrer verlegt. Hast du ihn gesehen?", [(13, 19, "TOOL")]),

    ("Ich brauche die Zange, um diesen Draht zu schneiden.", [(16, 21, "TOOL")]),
    ("Könntest du mir bitte den Bohrer bringen?", [(26, 32, "TOOL")]),
    ("Der Schlüssel liegt wahrscheinlich in der Garage.", [(4, 13, "TOOL")]),
    ("Ich kann das Sägeblatt nicht finden.", [(13, 22, "TOOL")]),
    ("Hast du schon den Akkuschrauber geladen?", [(18, 31, "TOOL")]),
    ("Die Wasserwaage ist in der Werkzeugkiste.", [(4, 15, "TOOL")]),
    ("Ich brauche einen neuen Meißel für diese Arbeit.", [(24, 30, "TOOL")]),
    ("Wo ist der Lötkolben? Ich brauche ihn für ein Projekt.", [(11, 20, "TOOL")]),
    ("Der Schraubenschlüssel ist auf dem Tisch.", [(4, 22, "TOOL")]),
    ("Kannst du mir die Rohrzange geben?", [(18, 27, "TOOL")]),

    ("Kannst du den Wagenheber aus dem Kofferraum holen?", [(14, 24, "TOOL")]),
    ("Ich denke, der Fuchsschwanz ist in der Werkstatt.", [(15, 27, "TOOL")]),
    ("Hast du den Schleifpapier gesehen?", [(12, 25, "TOOL")]), 
    ("Wir brauchen einen Schraubstock zum Halten des Materials.", [(19, 31, "TOOL")]),
    ("Ich muss den Bolzenschneider finden.", [(13, 28, "TOOL")]),
    ("Hast du den Gabelschlüssel verwendet?", [(12, 26, "TOOL")]),
    ("Ich kann den Nietenzange nirgends finden.", [(13, 24, "TOOL")]),
    ("Der Schneidebrenner ist zu heiß.", [(4, 19, "TOOL")]),
    ("Hast du den Nagelzieher benutzt?", [(12, 23, "TOOL")]),
    ("Ich brauche den Kombizange, um den Draht zu biegen.", [(17, 27, "TOOL")]),
    ("Der Winkelschleifer ist in der Werkstatt.", [(4, 19, "TOOL")]),
    ("Kannst du den Laserentfernungsmesser finden?", [(14, 36, "TOOL")]),
    ("Wo ist der Ringschlüssel? Ich brauche ihn.", [(11, 24, "TOOL")]),
    ("Ich habe den Steckschlüssel verlegt. Hast du ihn gesehen?", [(13, 27, "TOOL")]),
    ("Der Hobel muss geschärft werden.", [(4, 9, "TOOL")]),
    ("Ich kann den Abzieher nicht finden.", [(13, 21, "TOOL")]),
    ("Hast du schon den Drechselmeißel gesehen?", [(18, 32, "TOOL")]),
    ("Die Kettensäge ist sehr laut.", [(4, 15, "TOOL")]),
    ("Ich brauche einen neuen Schneidbrenner für diese Arbeit.", [(24, 39, "TOOL")]),
    ("Wo ist der Bohrhammer? Ich brauche ihn für ein Projekt.", [(11, 22, "TOOL")])
    
]


# Evaluation data from file provided by U&Z. Only those which mention a tool are included

# evaluation_data = [
#     ("Kupplungsadapter auf Kupplung setzen und EDH-Griff in Aufnahme der Presse platzieren.", [(67, 73, "TOOL")]),
#     ("EDH-Sicherungsring auf Adapter setzen und zum Anschlag verpressen (bei Bedarf mit einer Ausgleichsscheibe).", [(88, 105, "TOOL")]),
#     ("EDH-Griff in den Endtester - je nach Drückerrichtung links/rechts - einsetzen und festklemmen.", [(17, 27, "TOOL")]),
#     ("EDH Rückstellkraft testen, dazu Arm des Endtesters über Griffrohr schwenken, Knopf nach unten drücken.", [(40, 50, "TOOL")]),
#     ("ITV Karte vor Elektronik halten. EDH kuppelt ein, Griff nach unten drücken, dann wieder zurück.", [(4, 9, "TOOL")]),
#     ("Nochmals mit der ITV Testkarte einkuppeln lassen und Griff nach unten gedrückt halten.", [(21, 30, "TOOL")])
# ]




total_sentences = len(evaluation_data)
correct_predictions = 0
predicted_entities = 0
actual_entities = 0

# Evaluate the model on each evaluation sentence
for sentence, ground_truth_entities in evaluation_data:
    doc = nlp(sentence)
    predicted_entities += len(doc.ents)
    actual_entities += len(ground_truth_entities)

    predicted_tools = set()
    actual_tools = set()

    for ent in doc.ents:
        if ent.label_ == "TOOL":
            predicted_tool = re.sub(r"\W", "", ent.text.strip().lower())
            predicted_tools.add(predicted_tool)

    for start, end, label in ground_truth_entities:
        if label == "TOOL":
            actual_tool = re.sub(r"\W", "", sentence[start:end].strip().lower())
            actual_tools.add(actual_tool)

    if predicted_tools == actual_tools:
        print("Correct prediction!")
        correct_predictions += 1

    print("Sentence:", sentence)
    print("Predicted tools:", predicted_tools)
    print("Actual tools:", actual_tools)
    print()

#  evaluation metrics
accuracy = correct_predictions / total_sentences
precision = correct_predictions / predicted_entities if predicted_entities > 0 else 0
recall = correct_predictions / actual_entities if actual_entities > 0 else 0
f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0


current_directory = os.path.dirname(os.path.abspath(__file__))

output_folder = os.path.join(current_directory, 'evaluation_reports')

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

current_datetime = datetime.datetime.now()

timestamp = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")

# output_file = os.path.join(output_folder, f"evaluation_results_{timestamp}.txt")

# with open(output_file, "w") as file:
#     file.write("Evaluation Metrics:\n")
#     file.write(f"Date and Time: {timestamp}\n")
#     file.write(f"Accuracy: {accuracy}\n")
#     file.write(f"Precision: {precision}\n")
#     file.write(f"Recall: {recall}\n")
#     file.write(f"F1 Score: {f1_score}\n")
#     file.write("Total number of sentences: {}\n".format(total_sentences))
#     file.write("Correct_predictions: {}\n".format(correct_predictions))

# # Print a confirmation message
# print(f"Evaluation results saved to {output_file}")

# Print evaluation metrics
print("Evaluation Metrics:")
print("Accuracy:", accuracy)
print("Precision:", precision)
print("Recall:", recall)
print("F1 Score:", f1_score)
print("Total number of sentences:", total_sentences)
print("Correct_predictions:", correct_predictions)
