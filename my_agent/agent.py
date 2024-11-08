from typing import TypedDict, Literal

from langgraph.graph import StateGraph, END
from my_agent.utils.nodes import ( 
    call_model, 
    should_continue,
    tools,
    run_tool,
    run_oracle,
    router
)
from my_agent.utils.state import AgentState


# Define the config
class GraphConfig(TypedDict):
    model_name: Literal["anthropic", "openai"]


# Define a new graph
workflow = StateGraph(AgentState, config_schema=GraphConfig)

# Define the two nodes we will cycle between
workflow.add_node("oracle", run_oracle)
# workflow.add_node("action", tool_node)
# each one of these needs to be subgraphs
# https://langchain-ai.github.io/langgraph/how-tos/subgraph/#add-a-node-function-that-invokes-the-subgraph
workflow.add_node("mark_step_done_agent", run_tool)
workflow.add_node("check_step_completion", run_tool)
# workflow.add_node("stage_oracle", run_tool)
workflow.add_node("final_answer", run_tool)
workflow.add_node("lightRAG", run_tool)
# workflow.add_node("rag_search_filter", run_tool)
# workflow.add_node("rag_search", run_tool)
workflow.add_node("business_rules_engine", run_tool)
# workflow.add_node("workflow_agent", run_tool)









# Set the entrypoint as `agent`.  kw:change
# This means that this node is the first one called
workflow.set_entry_point("oracle")

# We now add a conditional edge
# workflow.add_conditional_edges(
#     # First, we define the start node. We use `agent`.
#     # This means these are the edges taken after the `agent` node is called.
#     "agent",
#     # Next, we pass in the function that will determine which node is called next.
#     should_continue,
#     # Finally we pass in a mapping.
#     # The keys are strings, and the values are other nodes.
#     # END is a specials node marking that the graph should finish.
#     # What will happen is we will call `should_continue`, and then the output of that
#     # will be matched against the keys in this mapping.
#     # Based on which one it matches, that node will then be called.
#     {
#         # If `tools`, then we call the tool node.
#         "continue": "action",
#         # Otherwise we finish.
#         "end": END,
#     },
# )
workflow.add_conditional_edges(
    source="oracle",  # where in graph to start
    path=router,  # function to determine which node is called
)


# create edges from each tool back to the oracle
for tool_obj in tools:
    if tool_obj.name != "final_answer":
        workflow.add_edge(tool_obj.name, "oracle")
# We now add a normal edge from `tools` to `agent`.
# This means that after `tools` is called, `agent` node is called next.
workflow.add_edge("final_answer", END)


# Finally, we compile it!
# This compiles it into a LangChain Runnable,
# meaning you can use it as you would any other runnable
graph = workflow.compile()






# https://langchain-ai.github.io/langgraph/how-tos/subgraph/#add-a-node-function-that-invokes-the-subgraph
# # Define subgraph
# class SubgraphState(TypedDict):
#     # note that none of these keys are shared with the parent graph state
#     bar: str
#     baz: str


# def subgraph_node_1(state: SubgraphState):
#     return {"baz": "baz"}


# def subgraph_node_2(state: SubgraphState):
#     return {"bar": state["bar"] + state["baz"]}


# subgraph_builder = StateGraph(SubgraphState)
# subgraph_builder.add_node(subgraph_node_1)
# subgraph_builder.add_node(subgraph_node_2)
# subgraph_builder.add_edge(START, "subgraph_node_1")
# subgraph_builder.add_edge("subgraph_node_1", "subgraph_node_2")
# subgraph = subgraph_builder.compile()


# # Define parent graph
# class ParentState(TypedDict):
#     foo: str


# def node_1(state: ParentState):
#     return {"foo": "hi! " + state["foo"]}


# def node_2(state: ParentState):
#     # transform the state to the subgraph state
#     response = subgraph.invoke({"bar": state["foo"]})
#     # transform response back to the parent state
#     return {"foo": response["bar"]}


# builder = StateGraph(ParentState)
# builder.add_node("node_1", node_1)
# # note that instead of using the compiled subgraph we are using `node_2` function that is calling the subgraph
# builder.add_node("node_2", node_2)
# builder.add_edge(START, "node_1")
# builder.add_edge("node_1", "node_2")
# graph = builder.compile()
