from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_classic.agents import (
    AgentExecutor,
    create_tool_calling_agent,
)
from langchain_core.tools import create_retriever_tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from db.db import get_db
from rag.retriever import get_vectorstore

load_dotenv()


def build_agent() -> AgentExecutor:
    llm = ChatGoogleGenerativeAI(model="gemini-3.6-flash", temperature=0)
    vectorstore = get_vectorstore()
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

    pdf_tool = create_retriever_tool(
        retriever,
        name="pdf_search",
        description=(
            "Search the Standard Veterinary Treatment Guidelines for "
            "diagnosis, treatment protocols, dosages, or clinical guidance "
            "on livestock and poultry diseases. Not for statistics/counts."
        ),
    )

    db = get_db()
    sql_toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    sql_tools = sql_toolkit.get_tools()

    tools = [pdf_tool] + sql_tools

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a veterinary/livestock data assistant. You have a "
                "pdf_search tool for treatment guidelines, plus SQL tools "
                "over a database with these tables:\n"
                "- disease_by_species: Disease, Species, Outbreak, Attack, "
                "Death (no year column)\n"
                "- national_incidence_2005_2011: one row per disease, wide "
                "year columns like '2005_Outbreak', '2005_Attack', "
                "'2005_Death'\n"
                "- national_incidence_2005_2015: same shape, wide columns "
                "like 'Outbreak_2005', extended to 2015\n"
                "- livestock_census: village-level livestock/poultry "
                "headcounts for Maharashtra (District, block/town, village/"
                "ward, and per-species/breed counts)\n"
                "Always inspect a table's schema before querying it. "
                "Combine pdf_search and SQL tools when a question needs "
                "both (e.g. severity + treatment). State which source(s) "
                "you used.",
            ),
            MessagesPlaceholder("chat_history", optional=True),
            ("human", "{input}"),
            MessagesPlaceholder("agent_scratchpad"),
        ]
    )

    agent = create_tool_calling_agent(llm, tools, prompt)
    return AgentExecutor(agent=agent, tools=tools, verbose=True)


if __name__ == "__main__":
    try:
        executor = build_agent()
        response = executor.invoke(
            {
                "input": (
                    "How many outbreaks of Foot & Mouth Disease were there "
                    "nationally in 2015, and what does the treatment guide "
                    "recommend for managing it?"
                )
            }
        )
        print(response["output"])
    except Exception as error:
        if "quota" in str(error).lower() or "resource_exhausted" in str(error).lower():
            print(
                "Gemini API quota is exhausted. Check the account associated "
                "with GEMINI_API_KEY and try again."
            )
        else:
            raise