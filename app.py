from crewai import Agent,Task,Crew,Process,LLM
from crewai_tools import WebsiteSearchTool
import streamlit as st
import os 
from dotenv import load_dotenv
load_dotenv()

api_key = st.sidebar.text_input("Enter the OpenAI API Key",type="password")

os.environ["OPENAI_API_KEY"] = api_key

st.title("Network Troubleshooting Agent!")




yt_tool = WebsiteSearchTool("https://www.dnsstuff.com/network-troubleshooting-steps")

# agent
response_agent = Agent(
    role='Network Support',
    goal="You are a network support agent, respond to the user to resolve the network issue {issue}, by searching the webpage",
    backstory=("Being a network troubleshooting agent, you are responsible to respond to the user's"
               "query, by finding the optimal solutions and giving a consise reply"),
    
    memory = True,
    allow_delegation= True,
    tools = [yt_tool],
    
    
)


# Task
response_task = Task(
    description="Respond to the user query, with a solution to the network issue {issue}, by getting the solution from the web page",
    expected_output= "A concise response to the user within 20 to 30 words, regarding the network issue and the solution to it",
    agent=response_agent
)


crew = Crew(
    agents=[response_agent],
    tasks=[response_task],
    share_crew=True,
    
    process=Process.sequential,
    
    
)



# Add a base message to the messages
if "messages" not in st.session_state:
    st.session_state['messages'] = [
        {'role' : "assistant","content" : "Hey, I am a network troubleshooting chatbot, how can i help you?"}
    ]


for msg in st.session_state.messages:
    st.chat_message(msg['role']).write(msg['content'])

if prompt:=st.chat_input(placeholder="My internet is working slow..."):
    st.session_state['messages'].append({
        'role' : "user",
        'content' : prompt
    })
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        
        response = crew.kickoff(inputs = {"issue" : prompt})
        st.session_state.messages.append({"role":"assistant","content":response.raw})
        st.write(response.raw)














