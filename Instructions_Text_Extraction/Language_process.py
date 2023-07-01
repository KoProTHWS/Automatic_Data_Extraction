import spacy
from spacy.matcher import Matcher
import pandas as pd

class LanguageProcessor:

    def combine(result):

        nlp = spacy.load("de_core_news_sm")

        df = pd.DataFrame(columns=['Step', 'Action', 'Components', 'Tools Required', 'Full Instruction'])

        # Loop through the instructions and extract the information for each one
        for i, (step_number, instruction) in enumerate(zip(result['Step Number'], result['Beschreibung / text'])):
            # Parse the assembly instruction with Spacy
            doc = nlp(instruction)

            # Extract the action verbs, components and tools from the instruction
            verbs = extract_verbs(doc)
            verb_tokens = [token for token in doc if token.text in verbs]
            # components = extract_components(doc, verb_tokens)
            components = extract_components(doc)
            # tools = extract_tools(doc, verb_tokens)
            tools = extract_tools(doc, nlp)

            # Remove components which are also tools
            # components = list(set(components) - set(tools))

            df = df.append({
                'Step': step_number,
                'Action': ', '.join(verbs),
                'Components': ', '.join(components),
                'Tools Required': ', '.join(tools),
                'Full Instruction': instruction
            }, ignore_index=True)

        print('Instructions successfully split and saved as xlsx file')
        df.to_excel('Instructions_2.xlsx', index=False)



def extract_verbs(doc):
    verb_tokens = []    
    for token in doc:
        if token.dep_ == 'ROOT':
            verb_tokens.append(token)
        if token.dep_ == 'conj' and token.head.dep_ == 'ROOT':
            verb_tokens.append(token)
    verbs = [verb.text for verb in verb_tokens]
    return verbs

# def extract_components(doc, verb_tokens):
#     components = []
#     for token in verb_tokens:
#         components.extend([child.text for child in token.children if child.dep_ == 'dobj'])
#     nouns = [token.text for token in doc if token.pos_ == 'NOUN' and token.text not in components]
#     other_nouns = list(set(nouns) - set(components))
#     components = list(set(components + other_nouns))
#     return components

def extract_components(doc):
    components = []

    for token in doc:
        # Identify nouns that are not subjects, nor part of compound nouns
        if token.pos_ == 'NOUN' and token.dep_ not in ('nsubj', 'compound', 'appos'):
            components.append(token.text)
        # Identify objects of prepositions
        elif token.dep_ == 'pobj':
            components.append(token.text)

    # Remove duplicates while maintaining the order
    seen = set()
    components = [component for component in components if not (component in seen or seen.add(component))]

    return components


# Does not work 
def extract_tools(doc, nlp):
    tools = []

    matcher = Matcher(nlp.vocab)

    # Define a pattern to match a noun phrase following a preposition ('with', 'using')
    pattern = [
        {"LOWER": {"IN": ["with", "using"]}},
        {"POS": "DET", "OP": "?"},  # optional determiner (e.g. 'the', 'a')
        {"POS": "ADJ", "OP": "*"},  # optional adjectives
        {"POS": "NOUN"}
    ]

    matcher.add("TOOL_PATTERN", [pattern])

    matches = matcher(doc)
    
    for match_id, start, end in matches:
        tool_phrase = doc[start:end]
        tools.append(tool_phrase[-1].text)  

    return tools

