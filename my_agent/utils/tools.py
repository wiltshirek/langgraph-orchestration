# from langchain_community.tools.tavily_search import TavilySearchResults

from langchain_core.tools import tool


##state is held but its effetively stateless.  all state is retrieved per action and on demand.
## not relying on memory.  this allows agents to assume different roles for a particular action
## oracle, for instance, can be an oracle for the entire workflow or, if given the correct state,
## the same oracle can assume control of a lower level stage in recursive fashion.
## in this way we should have one generic_stage_tool(works on all levels guided by prompts that contain
# all the info required for that action, no prior state required), oracle, business_rules_agent

@tool("web_search")
def web_search(query: str):
    """Finds general knowledge information using Google search. Can also be used
    to augment more 'general' knowledge to a previous specialist query."""
    search = GoogleSearch({
        **serpapi_params,
        "q": query,
        "num": 5
    })
    results = search.get_dict()["organic_results"]
    contexts = "\n---\n".join(
        ["\n".join([x["title"], x["snippet"], x["link"]]) for x in results]
    )
    return contexts



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

@tool("stage_stage")
def stage_state():
    """"returns the state for a particular stage"""

@tool("business_rules_engine")
def business_rules_engine(query: str):
    """Using the following stage 2 business rules {BR}, find applicable violations in [state here].   
    if no violations are found return an empty array using the format below.
    if violations are found return an array list of violations using the format below.
    if its okay to move on to the next step then return current and next stage name as a Tuple 
    if given 
    list the violations in tuple form {rule_violations:[], stage_info:[current_stage,next_stage ]
    if the number of violations is > 0 then return stage_info:[current_stage, current_stage]
    so the Oracle uses the workflow 
    stage 2 in the credentialing workflow process},  steps {}  using Google search. Can also be used
    to augment more 'general' knowledge to a previous specialist query."""
    return {"rule_violations":[]}


@tool("workflow_agent") #works for oracle and stages.
def workflow_agent(query:str):
    """return primary workflow info; retrn next stage based on current stage
    return second level workflow info; retrn next step based on current step
    return third xxxxxxxxx"""
    return "2"

@tool("lightRAG")
def lightRAG(query:str):
    """you are a helpful research assistant."""
    """this tool is in its own world.  consider a lambda for this since
    its like a 3rd party tool not related to the workflow"""
    return "light_rag_search"


@tool("stage_oracle")  #access to all tools requierd for this stage.
def stage_oracle(query: str):
    """you are the primary agent for this stage in the credentialin process.  
     Govern a medical credentialing process by applying the business rules and workflow instructions found below to each step
     each step must be processed in the order specified by the workflow.
     you can mark each step as done once all rules have been satisfied.
     when all steps are successfully completed without violation you can mark it as done using the proper tool.
     before selecting the best tool to complete the next step.  Workflow stages tools (regardless of level) are agents for that specific stage or step.  Ex:
     workflow stage 1 is governed by the workflow_stage_1_tool.  Your goal is to complete the entire workflow.  You can verify this
     by using the is_workflow_complete tool.  
    quide the workflow  Your goal is to complete the entire workflow without any rule violations
     or exceptions.  The completion status of each stage can be found by using the stage_complete_agent tool.  if you need more info on 
     a particular stage then use the stage_state_tool.  You cannot move to the next stage unless all rules are satisfied by the previous stage.
    quide the workflow  """
    return "stage_1_tool_called"



@tool("check_step_completion")
def check_step_completion(query: str):
    """checks if a step has been marked as completed.  if not apply business rules below to the following step: STEP
    and return list of violations, empty list is no violation."""
    return "check_stage_completion"

@tool("mark_step_done_agent")
def mark_step_done_agent(query: str):
    """marks a step as completed"""

    #return list of violations, empty list is no violation.
    return "mark_step_doen_agent"


@tool("rag_search_filter")
def rag_search_filter(query: str, arxiv_id: str, workflow_step: int):
    # """Finds information from our ArXiv database using a natural language query
    # and a specific ArXiv ID. Allows us to learn more details about a specific paper."""
    """Finds QA answer to get more detailed information about the query.  
       Use the following Business Rules to decide whether the use of this tool doesnt violat
       a business rule in this specific use case, i.e. from this specific node/edge combination.  other incomng nodes 
       to the next step may not have the same restrictions.  seems like the agent needs to consider the 
       edge rules.  try to do this in the should continue.  regardless, these need to be edge level rules
       {business_rule_1_related_to_THIS WORKFLOW_STEP, business_rule_2_related_to_THIS WORKFLOW_STEP
        business_rule_3_related_to_THIS WORKFLOW_STEP } to """
    return "rag_search_filter"

@tool("rag_search")
def rag_search(query: str):
    """Finds specialist information on AI using a natural language query."""
    # xq = encoder([query])
    # xc = index.query(vector=xq, top_k=2, include_metadata=True)
    # context_str = format_rag_contexts(xc["matches"])
    return "rag_search"

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
    rag_search,
    rag_search_filter,
    mark_step_done_agent,
    check_step_completion,
    stage_oracle,
    lightRAG,
    workflow_agent,
    business_rules_engine,
    final_answer
]

tool_str_to_func = {
    "rag_search_filter": rag_search_filter,
    "rag_search": rag_search,
    "check_step_completion": check_step_completion,
    "web_search": web_search,
    "mark_step_done_agent": mark_step_done_agent,
    "final_answer": final_answer,
    "lightRAG":lightRAG,
    "business_rules_engine":business_rules_engine,
    "workflow_agent":workflow_agent


}



