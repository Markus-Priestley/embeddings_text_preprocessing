# json files are in a key value format like dictionaries
import json
import re
from nltk.stem import WordNetLemmatizer
import string
import sys

# Prompt user to input json file name and opens file
jsonFileName = input("Enter json File: ")
try:
    # With makes sure opened files are automatically closed
    with open(jsonFileName) as openedJson:
        # Load takes and opened json file and converts it into a dictionary object.
        jsonObject = json.load(openedJson) 
except:
    print("Must input an existing json file")
    sys.exit()

# Converts json dict into a string which will be parsed
jsonString = json.dumps(jsonObject)
# Uses regex in order to find all tags
intentTagsList = re.findall('{"tag": "([0-9a-zA-Z ]+)"', jsonString)
# Edits tags until sufficient
# Lowercase
intentTagsList = [tag.lower() for tag in intentTagsList]
lemmatizer = WordNetLemmatizer()
# Lematizes
intentTagsList = [lemmatizer.lemmatize(tag) for tag in intentTagsList]
# Removes punctuation
intentTagsList = [tag.translate(str.maketrans('', '', string.punctuation)) for tag in intentTagsList] 

# Now steps will be taken in order to seperate each tags questions/requests into their own lists

# Parses all questions/requests into tagSentences list where each idex contains all the
#     questions/requests for the tag at the same index on the intentTagsList
tagSentences = re.findall('"patterns": \[([A-Za-z0-9?.,)\-( "\'+]+)\]', jsonString)
# Creates a list with each individual questions/request for the first tag in the intentTagsList
index0TagSentences = re.findall('"([A-Za-z0-9?., ]+)"', tagSentences[0])
print("cheese")
print(index0TagSentences)
# This function does the same thing as line 27 (creates a list of sentences/requests for a single
#     tag from a list of all sentences/requests) but can be used for any tag
def seperateTagSentences(tagIndex):
    return re.findall('"([A-Za-z0-9?+., )\-(\']+)"', tagSentences[tagIndex])

# Creates a list similar to tagSentences, but each index is a list with questions/requests as
#     entries
seperatedTagSentences = []
for index in range(len(tagSentences)):
     seperatedTagSentences.append(seperateTagSentences(index))

# Creates a list with every sentence/request seperated individually as the indexes of the list
allSentencesSeperated = []
for tagIndex in range(len(tagSentences)):
    for sentenceIndex in range(len(seperateTagSentences(tagIndex))):
        allSentencesSeperated.append(seperateTagSentences(tagIndex)[sentenceIndex])
# Edits sentences until sufficient
# Lowercase
allSentencesSeperated = [sentence.lower() for sentence in allSentencesSeperated]
lemmatizer = WordNetLemmatizer()
# Lematizes
allSentencesSeperated = [lemmatizer.lemmatize(sentence) for sentence in allSentencesSeperated]
# Removes punctuation
allSentencesSeperated = [sentence.translate(str.maketrans('', '', string.punctuation)) for sentence in allSentencesSeperated]
# Creates matching tags for this list
matchingTags = []
for tagIndex in range(len(intentTagsList)):
    for sentenceIndex in range(len(seperateTagSentences(tagIndex))):
            matchingTags.append(intentTagsList[tagIndex])


# This was my vison for the final product; A dictionary with intent tags as the keys and lists of
#     questions/requests corresponding to each intent tag as values. Got clearification on what
#     I was actually supposed to make. 
finalProduct = dict()
for index in range(len(tagSentences)):
    finalProduct[intentTagsList[index]] = seperatedTagSentences[index]

# Possible System. Questions/requests are only edited properly when all are asked for (enter 2 times)
#     still working on fixing that
print("Intent Tags")
print(intentTagsList)
for index in range(len(tagSentences)):
    print("For", intentTagsList[index], "Tag, Press", index)

print("For All Tags, Press Enter (Leave Input Space Blank)")

userInput = input("Enter a Number: ")
if len(userInput) != 0:
    try:
        userInput = int(userInput)
        matchingTags = []
        for index in range(len(seperatedTagSentences[userInput])):
            matchingTags.append(intentTagsList[userInput])
        print("Questions/Requests Related to", intentTagsList[userInput])
        print(seperatedTagSentences[userInput])
        print("Matching Tags")
        print(matchingTags)
    except:
        print("Must enter a valid number")
        sys.exit()
else:
    print("All questions/requests")
    print(allSentencesSeperated)
    print("Matching Tags")
    print(matchingTags)
    
