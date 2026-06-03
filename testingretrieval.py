import os
from dotenv import load_dotenv

import json
from groq import Groq
from pydantic import BaseModel, Field

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
