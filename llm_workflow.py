import operator
import os
from typing import Annotated, Literal, TypedDict

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import END, START, StateGraph

load_dotenv()

google_api_key = os.environ.get("MODEL_API_KEY")

# model = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite",
# google_api_key=google_api_key)

# class LLMState(TypedDict):
#   question: str
#   answer: str
#
#
# def get_initial_state(question: str | None = None) -> LLMState:
#   if question:
#     return {
#         "question": question,
#         "answer": "",
#     }
#
#   return {
#       "question": "What is the capital of France?",
#       "answer": "",
#   }
#
#
# def process_question(state: LLMState) -> LLMState:
#   question = state["question"]
#   prompt = f"Answer the following question: {question}"
#
#   res = model.invoke(prompt)
#   state["answer"] = res.content
#
#   return state
#
#
# graph = StateGraph(LLMState)
#
# graph.add_node("llm_qa", process_question)
# graph.add_edge(START, "llm_qa")
# graph.add_edge("llm_qa", END)
#
# workflow = graph.compile()
#
# final_state = workflow.invoke(get_initial_state())
#
# print("Question:", final_state["question"])
# print("Answer:", final_state["answer"])

#
# class RandomState(TypedDict):
#   d1: str
#   d2: str
#   d3: str
#   d4: str
#   score: Annotated[int, operator.add]
#   perform: str
#
#
# def update_d1(state: RandomState):
#   return {"d1": "updated value", "score": 5}
#
#
# def update_d2(state: RandomState):
#   return {"d2": "updated value", "score": 7}
#
#
# def update_d3(state: RandomState):
#   return {"d3": "updated value", "score": 1}
#
#
# def update_d4(state: RandomState):
#   return {"d4": "updated value"}
#
#
# graph = StateGraph(RandomState)
#
# graph.add_node("d1", update_d1)
# graph.add_node("d2", update_d2)
# graph.add_node("d3", update_d3)
# graph.add_node("d4", update_d4)
#
# graph.add_edge(START, "d1")
# graph.add_edge(START, "d2")
# graph.add_edge(START, "d3")
# graph.add_edge(START, "d4")
#
# graph.add_edge("d1", END)
# graph.add_edge("d2", END)
# graph.add_edge("d3", END)
# graph.add_edge("d4", END)
#
# workflow = graph.compile()
#
# final_state = workflow.invoke({
#     # "d1": "",
#     # "d2": "",
#     # "d3": "",
#     # "d4": "",
#     # "score": 0
# })
# print(final_state)
