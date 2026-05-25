from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.agents import initialize_agent, AgentType   # works on all versions
from tools import search_tool
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.3)



# AGENT 1 — Researcher
# Uses initialize_agent (compatible with all LangChain versions)


def make_researcher():
    return initialize_agent(
        tools=[search_tool],
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,  # ReAct pattern, no hub needed
        verbose=True,
        max_iterations=6,
        handle_parsing_errors=True
    )

def run_researcher(query: str, depth: int = 2) -> str:
    researcher = make_researcher()
    result = researcher.invoke({
        "input": (
            f"Research this topic thoroughly: '{query}'\n"
            f"Search at least {depth} times using different angles and keywords.\n"
            f"Collect facts, statistics, expert opinions, and recent developments.\n"
            f"Crucially, you MUST include the source URLs and references for all information gathered.\n"
            f"Return all findings in detail along with their source URLs."
        )
    })
    return result["output"]



# CHAIN 2 — Summarizer (LCEL chain, no agent needed)


_summarize_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are an expert research analyst. Your job is to read raw research "
        "findings and organize them into clean, structured bullet-point summaries. "
        "Group related points under clear section headings. "
        "You MUST preserve and cite all source URLs next to their corresponding points. "
        "Be thorough but concise."
    ),
    (
        "human",
        "Here are the raw research findings:\n\n{research}\n\n"
        "Topic: {topic}\n\n"
        "Please organize these into a structured summary with clear sections and bullet points, ensuring source URLs are kept intact."
    )
])

summarizer_chain = _summarize_prompt | llm | StrOutputParser()



# CHAIN 3 — Presenter (LCEL chain, no agent needed)


_present_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a professional research report writer. You write clear, "
        "well-structured, and insightful reports from research summaries. "
        "Your reports are detailed, professional, and easy to read. "
        "You always include a comprehensive list of references and sources at the end."
    ),
    (
        "human",
        "Write a complete research report on: '{topic}'\n\n"
        "Based on this research summary:\n\n{summary}\n\n"
        "Structure the report exactly like this:\n"
        "# {topic} — Research Report\n"
        "## Executive Summary\n"
        "## Key Findings\n"
        "## Detailed Analysis\n"
        "## Current Trends\n"
        "## Challenges and Limitations\n"
        "## Conclusion\n"
        "## References & Sources\n\n"
        "Write full paragraphs under each section. In the text, cite sources where appropriate, and list all URLs in the 'References & Sources' section."
    )
])

presenter_chain = _present_prompt | llm | StrOutputParser()



# FULL PIPELINE — Connects all 3 in sequence


def run_research(topic: str, breadth: int = 3, depth: int = 2) -> str:

    query_templates = [
        f"{topic} overview introduction basics",
        f"{topic} latest news developments 2025",
        f"{topic} key challenges problems limitations",
        f"{topic} real world applications use cases examples",
        f"{topic} future trends predictions experts"
    ]
    sub_queries = query_templates[:breadth]

    print(f"\n{'='*50}")
    print(f"Starting research on: {topic}")
    print(f"Breadth: {breadth} queries | Depth: {depth} searches each")
    print(f"{'='*50}\n")

    # Step 1 — Researcher
    all_findings = []
    for i, query in enumerate(sub_queries, 1):
        print(f"\n[Researcher] Query {i}/{breadth}: {query}")
        findings = run_researcher(query, depth=depth)
        all_findings.append(f"### Research Area {i}: {query}\n\n{findings}")

    combined_research = "\n\n".join(all_findings)

    # Step 2 — Summarizer
    print(f"\n[Summarizer] Organizing {breadth} research findings...")
    summary = summarizer_chain.invoke({
        "research": combined_research,
        "topic": topic
    })

    # Step 3 — Presenter
    print(f"\n[Presenter] Writing final report...")
    report = presenter_chain.invoke({
        "topic": topic,
        "summary": summary
    })

    print(f"\n{'='*50}")
    print("Research complete!")
    print(f"{'='*50}\n")

    return report