from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from .tools import (
    TechnologyStackAnalyzer,
    ArchitecturePatternValidator,
    PerformanceCalculator,
    SecurityChecklistGenerator
)

@CrewBase
class SoftwareSystemDesignCrew():
    """Software System Design Crew for comprehensive architecture planning"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def requirements_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['requirements_analyst'],
            verbose=True
        )

    @agent
    def system_architect(self) -> Agent:
        return Agent(
            config=self.agents_config['system_architect'],
            tools=[ArchitecturePatternValidator(), PerformanceCalculator()],
            verbose=True
        )

    @agent
    def technology_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config['technology_specialist'],
            tools=[TechnologyStackAnalyzer()],
            verbose=True
        )

    @agent
    def security_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['security_engineer'],
            tools=[SecurityChecklistGenerator()],
            verbose=True
        )

    @agent
    def performance_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['performance_engineer'],
            tools=[PerformanceCalculator()],
            verbose=True
        )

    @task
    def requirements_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['requirements_analysis_task'],
        )

    @task
    def system_architecture_design_task(self) -> Task:
        return Task(
            config=self.tasks_config['system_architecture_design_task'],
        )

    @task
    def technology_selection_task(self) -> Task:
        return Task(
            config=self.tasks_config['technology_selection_task'],
        )

    @task
    def security_architecture_task(self) -> Task:
        return Task(
            config=self.tasks_config['security_architecture_task'],
        )

    @task
    def performance_optimization_task(self) -> Task:
        return Task(
            config=self.tasks_config['performance_optimization_task'],
        )

    @task
    def architecture_integration_task(self) -> Task:
        return Task(
            config=self.tasks_config['architecture_integration_task'],
            output_file='software_architecture_specification.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Software System Design Crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )
