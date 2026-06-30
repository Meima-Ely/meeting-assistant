import os
from dotenv import load_dotenv
from groq import Groq
from crewai import LLM

import crewai.llms.cache as _crewai_cache
_crewai_cache.mark_cache_breakpoint = lambda msg: msg

load_dotenv()

llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    api_key=os.environ.get("GROQ_API_KEY"),
    temperature=0,
)

groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))