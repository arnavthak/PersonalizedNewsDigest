from dotenv import load_dotenv
from agents import Agent, Runner, trace
from tools import get_headlines, send_html_email
from prompts import get_rag_instructions, get_fetch_instructions, create_writer_user_prompt, get_writer_instructions, get_emailer_instructions, create_emailer_user_prompt
from models import HeadlinesOutput
import asyncio
from utils import get_fetch_params
from agents.mcp import MCPServerStdio

load_dotenv(override=True)


async def main():
    # User Input
    prompt = input("Enter your news preferences/interests:\n")
    recipient_email = input("Enter your email address:\n")

    # Stage 1: RAG

    rag_agent = Agent(
        name="RAG Agent",
        tools=[get_headlines],
        instructions=get_rag_instructions(),
        model="gpt-4.1",
        output_type=HeadlinesOutput
    )

    with trace("News Semantic Search"):
        result = await Runner.run(rag_agent, input=prompt, max_turns=20)
        structured = result.final_output
    
    print("Stage 1 complete!")
    
    # Stage 2: Fetch

    async with MCPServerStdio(params=get_fetch_params()) as fetch_server:
        await fetch_server.connect()

        news_agent = Agent(
            name="Fetch Agent",
            mcp_servers=[fetch_server],
            instructions=get_fetch_instructions(),
            model="gpt-4.1"
        )

        tasks = []

        for category in structured.headlines:
            for headline in category.headlines:
                async def fetch_article(headline=headline, category=category):
                    with trace(f"Fetch news article {headline.url} - {category}"):
                        result = await Runner.run(news_agent, input=headline.url, max_turns=20)
                        return f"{headline.url}:\n{result.final_output}"

                tasks.append(fetch_article())

        articles = await asyncio.gather(*tasks)
    
    print("Stage 2 complete!")

    # Stage 3: Writer

    writer_prompt = create_writer_user_prompt(articles=articles, user_preferences=prompt)

    news_agent = Agent(
        name="News Summarizer",
        instructions=get_writer_instructions(),
        model="gpt-4.1",
    )

    with trace("News Summary"):
        result = await Runner.run(news_agent, input=writer_prompt)
        news_markdown = result.final_output
    
    print("Stage 3 complete!")

    # Stage 4: Email

    email_agent = Agent(
        name="Email Agent",
        instructions=get_emailer_instructions(),
        tools=[send_html_email],
        model="gpt-4.1",
    )
        
    with trace("Email Agent"):
        result = await Runner.run(email_agent, input=create_emailer_user_prompt(news_markdown=news_markdown, recipient_email=recipient_email))

    print("Stage 4 complete!")

if __name__ == "__main__":
    asyncio.run(main())