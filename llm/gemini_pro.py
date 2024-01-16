from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
load_dotenv()  # take environment variables from .env.

GOOGLE_API_KEY=os.getenv("GOOGLE_API_KEY")

# Set gemini pro as llm
llm = ChatGoogleGenerativeAI(model="gemini-pro",
                             verbose = True,
                             temperature = 0.6,
                             google_api_key=GOOGLE_API_KEY )