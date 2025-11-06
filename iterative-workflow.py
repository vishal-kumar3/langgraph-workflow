import operator
import os
from typing import Annotated, Literal, TypedDict

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel, Field

load_dotenv()

google_api_key = os.environ.get("MODEL_API_KEY")

class TweetState(TypedDict):
  topic: str
  tweet: str

  evaluation: Literal["approved", "need_improvement"]
  feedback: str
  iterations: int
  max_iterations: int

  tweet_history: Annotated[list[str], operator.add]
  feedback_history: Annotated[list[str], operator.add]

class TweetEvaluation(BaseModel):
  evaluation: Literal["approved", "need_improvement"] = Field(..., description="Final evaluation result.")
  feedback: str = Field(..., description="Constructive feedback for the tweet.")

generate_tweet_model = ChatGoogleGenerativeAI(
  model="gemini-2.0-flash-lite",
  google_api_key=google_api_key
)

validate_tweet_model = ChatGoogleGenerativeAI(
  model="gemini-2.5-flash-lite",
  google_api_key=google_api_key,
  temperature=0
).with_structured_output(TweetEvaluation, method="json_schema")


def generate_tweet(state: TweetState):
  res = generate_tweet_model.invoke(f"Create tweet on {state["topic"]}\n Output in simple string, one tweet, and short")
  return { "tweet": res.content }

def evaluate_tweet(state: TweetState):
  messages = [
    SystemMessage("Evaluate the following tweeet and provide feedback for improvement. Tweet shouldn't be generic, copied, must be engaging, shouldn't have appeared many times!"),
    HumanMessage(f"Tweet topic: {state['topic']}\n Tweet: {state['tweet']}")
  ]

  res = validate_tweet_model.invoke(messages)

  return { 
    "evaluation": res.evaluation, 
    "tweet_history": [state["tweet"]], 
    "feedback": res.feedback,
    "feedback_history": [res.feedback]
  }

def optimize_tweet(state: TweetState):
  prompt = f"""
      Tweet topic: {state["topic"]}
      Tweet: {state["tweet"]}
      Feedback: {state["feedback"]}

      Rewrite the tweet based on above feedback.
      Provide just tweet string, and it should be short
    """

  res = generate_tweet_model.invoke(prompt)

  return { "tweet": res.content, "iterations": state["iterations"] + 1 }

def validate_tweet_or_reiterate(state: TweetState):
  if state["evaluation"] == "approved" or state["iterations"] >= state["max_iterations"]:
    return "approved"
  else:
    return "need_improvement"

graph = StateGraph(TweetState)

graph.add_node("generate_tweet", generate_tweet)
graph.add_node("evaluate_tweet", evaluate_tweet)
graph.add_node("optimize_tweet", optimize_tweet)

graph.add_edge(START, "generate_tweet")
graph.add_edge("generate_tweet", "evaluate_tweet")

graph.add_conditional_edges("evaluate_tweet", validate_tweet_or_reiterate, { "approved": END, "need_improvement": "optimize_tweet" })

graph.add_edge("optimize_tweet", "evaluate_tweet")

workflow = graph.compile()

initial_state: TweetState = {
  "topic": "Generative AI",
  "iterations": 1,
  "max_iterations": 5,
  "feedback_history": [],
  "tweet_history": []
}

final_state = workflow.invoke(initial_state)

print(f"Tweet[{final_state["iterations"]}]: ", final_state["tweet"])
print("Feedback: ", final_state["feedback"])

