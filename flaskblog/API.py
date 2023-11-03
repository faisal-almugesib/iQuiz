import json
import openai
from flask import jsonify

openai.api_key = ""

text_input = input('Enter text:')
text = str(text_input)
text = text.strip()

prompt = f"\n\n{text}\nGenerate 10 multiple choice questions that covers the whole provided article and exactly 3 answers choices based on the following article:: number of the question. the question that covers the article.\n a) choice A \n b) choice B \n c) choice C. "

response = openai.Completion.create(
                engine="text-davinci-002",
                prompt=prompt,
                max_tokens=3000,  # You can adjust this based on your needs
                n = 10,  # Number of questions to generate
                stop=None,
                temperature=0.7  # You can adjust this for creativity
            )

# This is the response
print("The questions are:")
#print(response["choices"][0]["text"])

questions = []
print(response.choices)
print("\n----------------------------------------------------------------------------------------------------------\n")
print("\n----------------------------------------------------------------------------------------------------------\n")

j = 0
for i, item in enumerate(response.choices):
    text = item.text.strip().split('\n')
    cleaned_text = [line.strip() for line in text if line.strip()]
    #print(cleaned_text)
    #print(len(cleaned_text))
print(cleaned_text)

t= False
if cleaned_text[4] == "2.":#set boolen if there is /n after the question number to jump it always
    t= True


print("\n----------------------------------------------------------------------------------------------------------\n")
j=0
while j < len(cleaned_text) - 3:
    question_text = cleaned_text[j]

    answer_options = cleaned_text[j+1:j+4]

    questions.append({
        "question": question_text,
        "options": answer_options
    })

    j += 4
    #correct_answer = answer_options[0].strip()  # The first option is the correct answer
    #options = [option.strip() for j, option in enumerate(answer_options)]
    #j+=4
    if t:
        j+=1
    

    


print( (questions))

print("\n----------------------------------------------------------------------------------------------------------\n")
for index, q in enumerate(questions):
    #print(f"Question{index + 1}: {q['question']}")
    print(q['question'])
    for i,a in enumerate(q['options']):
        print(a)
    print("\n")

