import os
from dotenv import load_dotenv

import json
from openai import OpenAI
import requests
from pydantic import BaseModel, Field

load_dotenv()

client = OpenAI(
    base_url="https://api.groq.com/openai/v1", api_key=os.getenv("GROQ-API-KEY")
)
