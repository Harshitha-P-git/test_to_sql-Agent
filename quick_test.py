from langchain_ollama import ChatOllama
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent

print("Loading model...")
llm = ChatOllama(model="llama3.2", temperature=0)

print("Connecting to database...")
db = SQLDatabase.from_uri("sqlite:///example.db")

print("Creating agent...")
agent = create_sql_agent(llm=llm, db=db, verbose=True, agent_type="openai-tools")

print("Running test query...")
result = agent.invoke({"input": "How many rows are in each table?"})
print("\nFINAL ANSWER:", result["output"])
