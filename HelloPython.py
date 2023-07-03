# json files are in a key value format like dictionaries
import json
import re

jsonFileName = input("Enter json File: ")
# with makes sure opened files are automatically closed
try:
    with open(jsonFileName) as openedJson:
        # load takes and opened json file and converts it into an object very similar to a dictionary.
        jsonObject = json.load(openedJson)
except:
    print("Must input an existing json file")
    exit

# just leaned what a json is and have only worked with re methods on text file so converting json to text file
jsonString = json.dumps(jsonObject)
jsonAsTextFileName = input("Enter New txt File Name: ")
with open(jsonAsTextFileName, 'w') as jsonAsTextFile:
    jsonAsTextFile.write(jsonString)

# This segment opens the text file and uses regualar expressions to parse intent tags and questions
fileHandle = open(jsonAsTextFileName)
for line in fileHandle:
    intentTags = re.findall('{"tag": "([0-9a-zA-Z ]+)"', line)
    sentences = re.findall('"([A-Za-z0-9? ]+)"', line)
print(intentTags)
print(sentences)

lowercaseTags = [tag.lower() for tag in intentTags]
lowercaseSentences = [sentence.lower() for sentence in sentences]


for sentence in sentences:
    sentence = sentence.trans