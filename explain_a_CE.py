from openai import OpenAI
from retry import retry
import json
import os


system_persona_round1 = """You are ENEXA Explanantion Chatbot that can answer questions about class expressions learned by the ENEXA pipeline.
Introduce yourself to the user and explain what you can do and stop.
"""

system_persona_round2 = """You are ENEXA Explanantion Chatbot that can answer questions about class expressions learned by the ENEXA pipeline.
Your specific task at hand is to answer user queries about a class expression. In the context of knowledge graphs and ontology languages such as 
RDF (Resource Description Framework) and OWL (Web Ontology Language), a class expression refers to a way of specifying a set of 
individuals or instances that share certain characteristics or properties. Classes represent sets of individuals, and class expressions 
provide a more detailed and expressive way of defining these sets. Class expressions can involve logical combinations of classes, 
restrictions on properties, and other constructs to precisely define the criteria for membership in a class.
You have already asked the user to select a class expression that you know. Here is the expression and the context.
{class_expression}
Answer the user questions according to the context.
"""

system_persona_round3 = """ You are ENEXA Explanantion Chatbot that can answer questions about class expressions learned by the ENEXA pipeline.
Your specific task at hand is to answer user queries about a class expression. In the context of knowledge graphs and ontology languages such as 
RDF (Resource Description Framework) and OWL (Web Ontology Language), a class expression refers to a way of specifying a set of 
individuals or instances that share certain characteristics or properties. Classes represent sets of individuals, and class expressions 
provide a more detailed and expressive way of defining these sets. Class expressions can involve logical combinations of classes, 
restrictions on properties, and other constructs to precisely define the criteria for membership in a class.
You have already asked the user to select a class expression that you know. Here is the expression and the context.
{class_expression}
Here is the log of the conversation so far.
{log}
Answer the user questions accordingly.
"""


# Get an answer from the OpenAI-API
@retry(tries=3, delay=2, max_delay=10)
def GPT_repsonse_round(api_key, prompt, model, temperature, max_tokens):
    # Set the OpenAI API key
    client = OpenAI(api_key=api_key)
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



def dialog_design(api_key):

    dialog_log = {}
    for i in range(20):
        if i == 0:
            system_persona = system_persona_round1
            user_query = input("Please type something to start the conversation: ")
        if i == 1:
            user_choice = input("At the moment, I can explain four class expressions. \n1. Not conglomerate (Q778575) \n2. Privately held company (Q1589009) \n3. Subsidiary (Q658255) \n4. Privately held company (Q1589009) and Brick and mortar (Q726870) \nPlease select the number of the class expression you want to know about: 1, 2, 3, or 4: ")

            if user_choice == "1":
                user_choice_of_class_expression = "Not conglomerate (Q778575)"
                file = "not_conglomerate_Q778575.json"

            if user_choice == "2":
                user_choice_of_class_expression = "Privately held company (Q1589009)"
                file = "Q1589009_privately_held_company.json"

            if user_choice == "3":
                user_choice_of_class_expression = "subsidiary (Q658255)"
                file = "Q658255_subsidiary.json"

            if user_choice == "4": 
                user_choice_of_class_expression = "privately held company (Q1589009) and brick and mortar (Q726870)"
                file = "Q1589009_and_Q726870.json"

            print(f"\nChatbot: Great! You would like to know about {user_choice_of_class_expression}")

            with open(file, "r", encoding='utf-8') as f:
                file_content = json.load(f)
                class_expression = json.dumps(file_content, ensure_ascii=False)
        
            user_query = input("What would you like to know about this class expression? Please type your question here: ")
            system_persona = system_persona_round2.format(class_expression=class_expression)
        
        if i > 1:
        
            user_query = input("\nPlease enter your question here to continue or type 'I am done' to stop. ")
            system_persona = system_persona_round3.format(class_expression=class_expression, log=dialog_log)

            if "i am done" in user_query.lower():
                print("Chatbot: Thank you for talking to me. Bye!")
                break
        
        prompt = {"system": system_persona,
        
                "query": user_query}
        
        #print("###############################################")
        #print(prompt["system"])
        #print("###############################################")
        
        answer = GPT_repsonse_round(api_key,prompt, "gpt-3.5-turbo-1106", temperature=0.3, max_tokens=300)

        dialog_log[i] = {"user": user_query, "chatbot": answer}
        
        print()
        
        print("Chatbot: ", answer)
        

def explain_a_CE():
    OpenAI_key = os.environ.get('OPENAI_API_KEY')
    if OpenAI_key == None or OpenAI_key == "":
        OpenAI_key = input("I couldn't get the key from environment variables. Please enter your OpenAI key here: ").strip()
    else:
        print("OpenAI key found in environment variables.")
        
    dialog_design(OpenAI_key)

if __name__ == "__main__":
    explain_a_CE()
    