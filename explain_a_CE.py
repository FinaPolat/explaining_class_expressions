from openai import OpenAI
from retry import retry
import json

# Set the OpenAI API key
client = OpenAI(api_key="YOUR_API_KEY")
# Get an answer from the OpenAI-API
@retry(tries=3, delay=2, max_delay=10)
def GPT_repsonse_round(prompt, model, temperature, max_tokens):
    messages=[{"role": "system", "content": prompt["system"]},
                {"role": "user", "content": prompt["query"]},
            ]
    response = client.chat.completions.create(
                                            model=model,
                                            #response_format={ "type": "json_object" },
                                            messages=messages,
                                            temperature=temperature,
                                            max_tokens=max_tokens,
    )
    response = response.choices[0].message.content
    
    return response



system_persona_round1 = """You are a helpful chatbot that can answer questions about knowledge graphs such as Wikidata.
Your specific task at hand is to user queries about a class expression. Introduce yourself to the user and explain what you can do. 
Then, ask the user to give you a class expression.
"""

system_persona_round2 = """You are a helpful chatbot that can answer questions about knowledge graphs such as Wikidata.
Your specific task at hand is to user queries about a class expression. In the context of knowledge graphs and ontology languages such as 
RDF (Resource Description Framework) and OWL (Web Ontology Language), a class expression refers to a way of specifying a set of 
individuals or instances that share certain characteristics or properties. Classes represent sets of individuals, and class expressions 
provide a more detailed and expressive way of defining these sets. Class expressions can involve logical combinations of classes, 
restrictions on properties, and other constructs to precisely define the criteria for membership in a class.

You have already asked the user to give you a class expression. Here is the expression the user gave to you.
{class_expression}
Now, explain this class expression to the user and ask whether the user has questions.
"""


system_persona_round3 = """You are a helpful chatbot that can answer questions about knowledge graphs such as Wikidata.
Your specific task at hand is to user queries about a class expression. In the context of knowledge graphs and ontology languages such as 
RDF (Resource Description Framework) and OWL (Web Ontology Language), a class expression refers to a way of specifying a set of 
individuals or instances that share certain characteristics or properties. Classes represent sets of individuals, and class expressions 
provide a more detailed and expressive way of defining these sets. Class expressions can involve logical combinations of classes, 
restrictions on properties, and other constructs to precisely define the criteria for membership in a class.

You have already asked the user to give you a class expression. Here is the expression the user gave to you.
{class_expression}
You have already explained this class expression to the user. Now answer the user questions according to the context.
"""

dialogue_state = True

for i in range(10):
    if i == 0:
        system_persona = system_persona_round1
        user_query = input("Please type something to start the conversation:")
    elif i == 1:
        user_query = input("At the moment, I can explain four class expressions. 1. ¬conglomerate (Q778575) 2.privately held company (Q1589009) 3.subsidiary (Q658255) 4.privately held company (Q1589009) ⊓ brick and mortar (Q726870) Type the number of the class expression you want to know about. Type 1, 2, 3, or 4:")
        if user_query == "1":
            file = "not_conglomerate_Q778575.json"
        elif user_query == "2":
            file = "Q1589009_privately_held_company.json"
        elif user_query == "3":
            file = "Q658255_subsidiary.json"
        elif user_query == "4": 
            file = "Q1589009_and_Q726870.json"
        else:
            print("Chatbot: ", "Sorry, I don't understand. Please type 1, 2, 3, or 4.")
            continue
        
        with open(file, "r", encoding='utf-8') as f:
            file_content = json.load(f)
            class_expression = json.dumps(file_content, ensure_ascii=False)

            print("Chatbot: ", "Here is the class expression we will talk about:")
            print(class_expression)
            print("Chatbot: ", "Now, I will explain this class expression to you.")
        system_persona = system_persona_round2.format(class_expression=class_expression)
        
    else: 
        system_persona = system_persona_round3.format(class_expression=class_expression)
        print("Say 'I am done' to stop.")
        user_query = input("Please type your question here:")
        if "i am done" in user_query.lower():
            print("Thank you.")
            break

    prompt = {"system": system_persona,
                "query": user_query}
    
    answer = GPT_repsonse_round(prompt, "gpt-3.5-turbo-1106", temperature=0.3, max_tokens=300)

    print()
    print("Chatbot: ", answer)
    
    