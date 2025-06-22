# score_chain.py
import os
from langchain_openai import OpenAI       # requires langchain-openai==0.1.4
from langchain.prompts import PromptTemplate
from langchain.output_parsers import ResponseSchema, StructuredOutputParser

# ── define the structured JSON we want back ─────────────────────────────
score_schema  = ResponseSchema(name="score",  description="1-10 numeric score")
reason_schema = ResponseSchema(name="reasons", description="List of bullet reasons")
level_schema  = ResponseSchema(name="lead_strength", description="hot | warm | cold")
parser = StructuredOutputParser.from_response_schemas(
    [score_schema, reason_schema, level_schema]
)

# ── prompt template ─────────────────────────────────────────────────────
prompt = PromptTemplate(
    template=(
        "You are a B2B sales analyst.\n"
        "Input: name={name}, company={company}, job_title={job_title}\n"
        "{format_instructions}"
    ),
    input_variables=["name", "company", "job_title"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

# ── OpenAI LLM (instruct model) ─────────────────────────────────────────
llm = OpenAI(
    model="gpt-3.5-turbo-instruct",
    temperature=0.2,
    openai_api_key=os.getenv("OPENAI_API_KEY"),
)

# ── public function used by FastAPI ─────────────────────────────────────
def score_lead(payload: dict) -> dict:
    """Return structured lead-score JSON."""
    raw = llm(prompt.format(**payload), max_tokens=120)
    return parser.parse(raw)
