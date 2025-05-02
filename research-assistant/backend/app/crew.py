# backend/app/crew.py
"""
Create the research crew using crewAI
"""
from crewai import Crew, Task, Agent
from typing import Dict, Any, List
from .agents import create_agents


def create_research_crew(api_key: str, topic: str, focus_areas: List[str] = None):
    """Creates and returns a crew for research tasks"""
    
    # Create the agents
    research_agent, summarizer_agent, editor_agent = create_agents(api_key)
    
    # Format focus areas for prompt if provided
    focus_areas_str = ""
    if focus_areas and len(focus_areas) > 0:
        focus_areas_str = "Please focus particularly on these areas: " + ", ".join(focus_areas)
    
    # Create tasks
    research_task = Task(
        description=f"""Research the topic: {topic}. {focus_areas_str}
        
        Your research should be comprehensive and include:
        1. Key concepts and definitions
        2. Historical context and development
        3. Current state of knowledge
        4. Significant contributors and their work
        5. Recent advancements or discoveries
        6. Connections to related fields
        7. Open questions or areas of debate
        
        Structure your findings clearly with headings and subheadings.
        """,
        agent=research_agent,
        expected_output="A comprehensive research document with structured findings"
    )
    
    summarize_task = Task(
        description=f"""Take the research findings on {topic} and create a concise summary.
        
        Your summary should:
        1. Identify and highlight the most important information
        2. Organize content logically
        3. Be approximately 500-750 words
        4. Include all key points while eliminating redundancies
        5. Maintain accuracy while simplifying complex concepts
        
        The summary should be accessible to someone with general knowledge but not expertise in the field.
        """,
        agent=summarizer_agent,
        expected_output="A clear, concise summary of the research findings",
        context=[research_task]
    )
    
    editing_task = Task(
        description=f"""Transform the research summary on {topic} into a polished final report.
        
        Your edits should:
        1. Improve clarity and readability
        2. Ensure consistent tone and style
        3. Fix any grammar, punctuation, or formatting issues
        4. Enhance the overall presentation
        5. Verify that the content flows logically
        6. Ensure the report is professional and engaging
        
        The final report should be ready for presentation to stakeholders.
        """,
        agent=editor_agent,
        expected_output="A polished, professional final report",
        context=[summarize_task]
    )
    
    # Create the crew
    crew = Crew(
        agents=[research_agent, summarizer_agent, editor_agent],
        tasks=[research_task, summarize_task, editing_task],
        verbose=True
    )
    
    return crew


def run_research_process(api_key: str, topic: str, focus_areas: List[str] = None) -> Dict[str, Any]:
    """Run the full research process and return results"""
    
    # Create and run the crew
    crew = create_research_crew(api_key, topic, focus_areas)
    result = crew.kickoff()
    
    # Process and structure the results
    # Assuming the final output is from the editing task
    research_data = {
        "raw_research": crew.tasks[0].output if hasattr(crew.tasks[0], 'output') else "",
    }
    
    summary = crew.tasks[1].output if hasattr(crew.tasks[1], 'output') else ""
    final_report = result  # The final result should be the edited report
    
    return {
        "topic": topic,
        "research_data": research_data,
        "summary": summary,
        "final_report": final_report,
        "status": "complete"
    }

