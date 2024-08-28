from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from langchain_google_genai import ChatGoogleGenerativeAI
from newsletter_crew.tools.custom_tool import Search, FindSimilar, GetContents
from datetime import datetime
import os

# Uncomment the following line to use an example of a custom tool
# from newsletter_crew.tools.custom_tool import MyCustomTool

# Check our tools documentations for more information on how to use them
# from crewai_tools import SerperDevTool

@CrewBase
class NewsletterCrew:
    """NewsletterCrew crew"""
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    def llm(self):
        google_api_key = os.getenv("GOOGLE_API_KEY")
        return ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            verbose=True,
            temperature=0.5,
            google_api_key=google_api_key
        )

    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config["researcher"],
            tools=[Search(), FindSimilar(), GetContents()],
            verbose=True,
            llm=self.llm(),
        )

    @agent
    def editor(self) -> Agent:
        return Agent(
            config=self.agents_config["editor"],
            verbose=True,
            tools=[Search(), FindSimilar(), GetContents()],
            llm=self.llm(),
        )

    @agent
    def designer(self) -> Agent:
        return Agent(
            config=self.agents_config["designer"],
            verbose=True,
            llm=self.llm(),
            allow_delegation=False,
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config["research_task"],
            agent=self.researcher(),
            output_file=f'logs/{datetime.now().strftime("%Y-%m-%d_%H-%M")}_research_task.md',
        )

    @task
    def edit_task(self) -> Task:
        return Task(
            config=self.tasks_config["edit_task"],
            agent=self.editor(),
            output_file=f'logs/{datetime.now().strftime("%Y-%m-%d_%H-%M")}_edit_task.md',
        )

    @task
    def newsletter_task(self) -> Task:
        return Task(
            config=self.tasks_config["newsletter_task"],
            agent=self.designer(),
            output_file=f'logs/{datetime.now().strftime("%Y-%m-%d_%H-%M")}_newsletter.html',
        )

    @crew
    def crew(self) -> Crew:
        """Creates the NewsletterCrew crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=2,
            # process=Process.hierarchical, # Uncomment if you want to use hierarchical processing
        )
