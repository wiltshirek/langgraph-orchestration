# from langchain_community.tools.tavily_search import TavilySearchResults

from langchain_core.tools import tool
import random


##state is held but its effetively stateless.  all state is retrieved per action and on demand.
## not relying on memory.  this allows agents to assume different roles for a particular action
## oracle, for instance, can be an oracle for the entire workflow or, if given the correct state,
## the same oracle can assume control of a lower level stage in recursive fashion.
## in this way we should have one generic_stage_tool(works on all levels guided by prompts that contain
# all the info required for that action, no prior state required), oracle, business_rules_agent

# @tool("web_search")
# def web_search(query: str):
#     """Finds general knowledge information using Google search. Can also be used
#     to augment more 'general' knowledge to a previous specialist query."""
#     search = GoogleSearch({
#         **serpapi_params,
#         "q": query,
#         "num": 5
#     })
#     results = search.get_dict()["organic_results"]
#     contexts = "\n---\n".join(
#         ["\n".join([x["title"], x["snippet"], x["link"]]) for x in results]
#     )
#     return contexts

#  """Using the business rules below,[BUSINESS_RULES] find applicable violations in the state provided below[STATE].   
#     if no violations are found return an empty array using the format below [FORMAT].
#     if violations are found return an array list WITH A description for each violation using the format below [FORMAT].
    
#     [FORMAT]
#     {"business_rule_violation_number_1_description_here":""reason_for_violation_number_1_here""}
#     {"business_rule_violation_number_2_description_here":""reason_for_violation_number_2_here""}
#     """



# @tool("oracle")
# def oracle(query: str):  #access to all stage level tools.
#     """Govern a medical credentialing process by applying business rules and workflow instructions to each step
#      before selecting the best tool to complete the next step.  Workflow stages tools (regardless of level) are agents for that specific stage or step.  Ex:
#      workflow stage 1 is governed by the workflow_stage_1_tool.  Your goal is to complete the entire workflow.  You can verify this
#      by using the is_workflow_complete tool.  
#     quide the workflow  Your goal is to complete the entire workflow without any rule violations
#      or exceptions.  The completion status of each stage can be found by using the stage_complete_agent tool.  if you need more info on 
#      a particular stage then use the stage_state_tool.  You cannot move to the next stage unless all rules are satisfied by the previous stage.
#     quide the workflow
#     """
#     return True


@tool("business_rules_engine")
def business_rules_engine(query: str, business_rules: str, stage_number: str):
    """Applies business rules to the current state for this step to check for 
    business rule violations.  If there are no violations for any step you can 
    move on to the next stage.
    """
    random_num = random.choice([f"step 7 for this stage {stage_number} has a violation", "there are no exceptions to any business rules in this stage"])

    return random_num



# @tool("workflow_agent") #works for oracle and stages.
# def workflow_agent(query:str):
#     """Get info about a workflow step or stage"""
#     return "worflow agent was accessed for workflow info"

@tool("lightRAG")
def lightRAG(query:str):
    """Perform researc on private data"""
    return "light_rag_search_was called for some reason"


# @tool("stage_oracle")  #access to all tools requierd for this stage.
# def stage_oracle(query: str):
#     """you are the primary agent for this stage in the credentialin process.  
#      Govern a medical credentialing process by applying the business rules and workflow instructions found below to each step
#      each step must be processed in the order specified by the workflow.
#      you can mark each step as done once all rules have been satisfied.
#      when all steps are successfully completed without violation you can mark it as done using the proper tool.
#      before selecting the best tool to complete the next step.  Workflow stages tools (regardless of level) are agents for that specific stage or step.  Ex:
#      workflow stage 1 is governed by the workflow_stage_1_tool.  Your goal is to complete the entire workflow.  You can verify this
#      by using the is_workflow_complete tool.  
#     quide the workflow  Your goal is to complete the entire workflow without any rule violations
#      or exceptions.  The completion status of each stage can be found by using the stage_complete_agent tool.  if you need more info on 
#      a particular stage then use the stage_state_tool.  You cannot move to the next stage unless all rules are satisfied by the previous stage.
#     quide the workflow  """
#     return "stage_1_tool_called"



@tool("check_step_completion")
def check_step_completion(query: str):
    """checks if a step has been marked as completed."""
    random_num = random.choice(["yes, this step has been completed","no, this step is still in progress and has not been completed"])

    return "check_stage_completion was called."

@tool("mark_step_done_agent")
def mark_step_done_agent(query: str):
    """marks a step as completed or done"""

    #return list of violations, empty list is no violation.
    return "mark_step_done_agent was called to mark a step as done."


# @tool("rag_search_filter")
# def rag_search_filter(query: str, arxiv_id: str, workflow_step: int):
#     # """Finds information from our ArXiv database using a natural language query
#     # and a specific ArXiv ID. Allows us to learn more details about a specific paper."""
#     """Finds QA answer to get more detailed information about the query."""       
#     return "rag_search_filter was called to find more info about QA"

# @tool("rag_search")
# def rag_search(query: str):
#     """Finds specialist information on AI using a natural language query."""
#     # xq = encoder([query])
#     # xc = index.query(vector=xq, top_k=2, include_metadata=True)
#     # context_str = format_rag_contexts(xc["matches"])
#     return "rag_search"

@tool("final_answer")
def final_answer(
    introduction: str,
    research_steps: str,
    main_body: str,
    conclusion: str,
    sources: str
):
    """Returns a natural language response to the user in the form of a research
    report. There are several sections to this report, those are:
    - `introduction`: a short paragraph introducing the user's question and the
    topic we are researching.
    - `research_steps`: a few bullet points explaining the steps that were taken
    to research your report.
    - `main_body`: this is where the bulk of high quality and concise
    information that answers the user's question belongs. It is 3-4 paragraphs
    long in length.
    - `conclusion`: this is a short single paragraph conclusion providing a
    concise but sophisticated view on what was found.
    - `sources`: a bulletpoint list provided detailed sources for all information
    referenced during the research process
    """
    if type(research_steps) is list:
        research_steps = "\n".join([f"- {r}" for r in research_steps])
    if type(sources) is list:
        sources = "\n".join([f"- {s}" for s in sources])
    return ""


tools = [
    mark_step_done_agent,
    check_step_completion,
    lightRAG,
    business_rules_engine,
    final_answer
]

tool_str_to_func = {
    "check_step_completion": check_step_completion,
    "mark_step_done_agent": mark_step_done_agent,
    "final_answer": final_answer,
    "lightRAG":lightRAG,
    "business_rules_engine":business_rules_engine,

}



