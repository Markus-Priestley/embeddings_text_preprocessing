import json
import re
import nltk
from nltk.stem import WordNetLemmatizer
import string
import sys
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords

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
intentTagsList = re.findall('{"tag": "([0-9a-zA-Z_ ]+)"', jsonString)
# Edits tags until sufficient
# Lowercase
intentTagsList = [tag.lower() for tag in intentTagsList]
lemmatizer = WordNetLemmatizer()
# Lematizes
intentTagsList = [lemmatizer.lemmatize(tag) for tag in intentTagsList]
# Removes punctuation
intentTagsList = [tag.translate(str.maketrans('', '', string.punctuation)) for tag in intentTagsList]
# Removes stopwords
stopWords = set(stopwords.words('english'))
for index in range(len(intentTagsList)):
    intentTagsList[index] = [word for word in intentTagsList[index].split() if word not in stopWords]
    intentTagsList[index] = " ".join(intentTagsList[index])
# Sentence tokenize 
intentTagsList = [sent_tokenize(tag) for tag in intentTagsList]
# Now steps will be taken in order to seperate each tags questions/requests into their own lists

# Parses all questions/requests into tagSentences list where each idex contains all the
#     questions/requests for the tag at the same index on the intentTagsList
tagSentences = re.findall('"patterns": \[([A-Za-z0-9?.,)\-( "\'+]*)\]', jsonString)

# Creates a list with each individual questions/request for the first tag in the intentTagsList
index0TagSentences = re.findall('"([A-Za-z0-9?., ]+)"', tagSentences[0])

# This function does the same thing as index0TagSentence's assignment (creates a list of sentences/requests
#     for a single tag from a list of all sentences/requests) but can be used for any tag. This is where each
#     tag is edited (lematized, lowercase, punct removed, and tokenized)
def seperateTagSentences(tagIndex):
    editedTagSentences = re.findall('"([A-Za-z0-9?+., )\-(\']+)"', tagSentences[tagIndex])
    editedTagSentences = [sentence.lower() for sentence in editedTagSentences]
    lemmatizer = WordNetLemmatizer()
    editedTagSentences = [lemmatizer.lemmatize(sentence) for sentence in editedTagSentences]
    editedTagSentences = [sentence.translate(str.maketrans('', '', string.punctuation)) for sentence in editedTagSentences]
    for index in range(len(editedTagSentences)):
        editedTagSentences[index] = [word for word in editedTagSentences[index].split() if word not in stopWords]
        editedTagSentences[index] = " ".join(editedTagSentences[index])
    editedTagSentences = [sent_tokenize(sentence) for sentence in editedTagSentences]
    return editedTagSentences

# Creates a list similar to tagSentences, but each index is a list with a list containing
#     questions/requests as entries
seperatedTagSentences = []
for index in range(len(tagSentences)):
     seperatedTagSentences.append(seperateTagSentences(index))

# Creates a list with every sentence/request seperated individually as the indexes of the list
allSentencesSeperated = []
for tagIndex in range(len(tagSentences)):
    for sentenceIndex in range(len(seperateTagSentences(tagIndex))):
        allSentencesSeperated.append(seperateTagSentences(tagIndex)[sentenceIndex])

# Creates matching tags for allSentencesSeperated list
allMatchingTags = []
for tagIndex in range(len(intentTagsList)):
    for sentenceIndex in range(len(seperateTagSentences(tagIndex))):
            allMatchingTags.append(intentTagsList[tagIndex])


# Possible System
print("Intent Tags. Total:" , len(intentTagsList))
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
        for index in range(len(seperatedTagSentences[userInput])):
            print("Intent Tag:", matchingTags[userInput], "Questions/Request:", seperatedTagSentences[userInput][index])
        print("Total Questions/Requests:", len(seperatedTagSentences[userInput]))
    except:
        print("Must enter a valid number")
        sys.exit()
else:
    print("All questions/requests")
    for index in range(len(allSentencesSeperated)):
        print("Intent Tag:", allMatchingTags[index], "Questions/Request:", allSentencesSeperated[index])
    print("Total Questions/Requests:", len(allSentencesSeperated))
    