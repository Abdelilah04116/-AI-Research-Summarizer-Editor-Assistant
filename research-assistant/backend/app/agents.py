"""Define the agents for the research assistant
"""
from crewai import Agent
from langchain_openai import ChatOpenAI


def create_agents(api_key: str):
    """Create the crew of agents"""
    # Choose the LLM
    llm = ChatOpenAI(
        model="gpt-4o",
        temperature=0,
        api_key=api_key
    )

    # Research Agent
    research_agent = Agent(
        role="Research Specialist",
        goal="Find comprehensive and accurate information on research topics",
        backstory="""You are an expert research specialist with years of experience in 
        gathering, analyzing, and structuring information. You have the ability to
        quickly identify reliable sources and extract the most relevant information.""",
        verbose=True,
        allow_delegation=False,
        llm=llm,
        tools=[]  # Could add web search tools here
    )

    # Summarizer Agent
    summarizer_agent = Agent(
        role="Information Synthesizer",
        goal="Create concise, accurate, and well-structured summaries from research data",
        backstory="""You are a talented synthesizer of information with a remarkable 
        ability to identify key points and create clear, organized summaries. You excel 
        at distilling complex concepts into accessible content without losing important details.""",
        verbose=True,
        allow_delegation=False,
        llm=llm
    )

    # Editor Agent
    editor_agent = Agent(
        role="Content Editor",
        goal="Transform summaries into polished, professional reports",
        backstory="""You are a meticulous editor with a keen eye for detail and a strong 
        command of language. You improve the clarity, flow, and presentation of content
        while maintaining the accuracy of the information.""",
        verbose=True,
        allow_delegation=False,
        llm=llm
    )

    return research_agent, summarizer_agent, editor_agent

