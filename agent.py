import os
from google.adk.agents import Agent
from .tools.discovery_engine import retrieve_product_details_from_search
import asyncio
from google.adk.tools import FunctionTool
from google.adk.sessions import InMemorySessionService, Session
from google.adk.runners import Runner
from google.genai import types

DATASTORE_ID = os.getenv("DATASTORE_ID")


search_tool = FunctionTool(func=retrieve_product_details_from_search)

#display_image_tool = FunctionTool(func=image_display)


root_agent = Agent(
    name="VertexAISearchAgent",
    model="gemini-2.0-flash",
    description="An agent that provides product information by searching a Vertex AI Search data store.",
    tools=[search_tool],
    instruction=""" You are a helpful assistant that give recommendations of products based on user query.
    Recommend products based on query using tools provided to you to find information from internal documents. 
    take help from search_tool tool to retrieve customized information about title and image url of retrieved products,
    at the end show title and image url to user
    """,
)

#and after retrieving title and image url use image_display tool to show image based on retrieved url.

APP_NAME = "product_app"
USER_ID = "1234"
SESSION_ID = "session1234"

async def setup_session_and_runner():
    session_service = InMemorySessionService()
    session = await session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)
    runner = Runner(agent=root_agent, app_name=APP_NAME, session_service=session_service)
    return session, runner

# Agent Interaction
async def call_agent_async(query):
    content = types.Content(role='user', parts=[types.Part(text=query)])
    session, runner = await setup_session_and_runner()
    events = runner.run_async(user_id=USER_ID, session_id=SESSION_ID, new_message=content)

    async for event in events:
        if event.is_final_response():
            final_response = event.content.parts[0].text
            print(f"final answer : {final_response}")
           
            


