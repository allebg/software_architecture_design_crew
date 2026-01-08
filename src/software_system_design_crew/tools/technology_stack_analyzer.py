from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field


class TechnologyStackAnalyzerInput(BaseModel):
    """Input schema for Technology Stack Analyzer."""
    application_type: str = Field(..., description="Type of application (web app, mobile app, API, etc.)")
    requirements: str = Field(..., description="Key requirements and constraints for technology selection")
    budget_range: str = Field(..., description="Budget range (low, medium, high)")


class TechnologyStackAnalyzer(BaseTool):
    name: str = "Technology Stack Analyzer"
    description: str = (
        "Analyzes and compares different technology stacks for software projects. "
        "Provides recommendations based on application type, requirements, and budget constraints. "
        "Evaluates frameworks, databases, cloud platforms, and development tools."
    )
    args_schema: Type[BaseModel] = TechnologyStackAnalyzerInput

    def _run(self, application_type: str, requirements: str, budget_range: str) -> str:
        # Technology recommendations database
        tech_stacks = {
            "web app": {
                "frontend": ["React", "Vue.js", "Angular", "Svelte"],
                "backend": ["Node.js", "Python (Django/FastAPI)", "Java (Spring)", "C# (.NET)"],
                "database": ["PostgreSQL", "MySQL", "MongoDB", "Redis"],
                "cloud": ["AWS", "Azure", "GCP", "Vercel"]
            },
            "mobile app": {
                "native": ["Swift (iOS)", "Kotlin (Android)"],
                "cross_platform": ["React Native", "Flutter", "Xamarin"],
                "backend": ["Node.js", "Python", "Firebase"],
                "database": ["Firebase Firestore", "PostgreSQL", "MongoDB"]
            },
            "api": {
                "frameworks": ["FastAPI", "Express.js", "Spring Boot", "ASP.NET Core"],
                "database": ["PostgreSQL", "MongoDB", "Redis"],
                "cloud": ["AWS API Gateway", "Azure Functions", "GCP Cloud Run"]
            },
            "microservices": {
                "languages": ["Go", "Java", "Python", "Node.js"],
                "containers": ["Docker", "Kubernetes"],
                "messaging": ["RabbitMQ", "Apache Kafka", "Redis Pub/Sub"],
                "database": ["PostgreSQL", "MongoDB", "Cassandra"]
            }
        }

        budget_considerations = {
            "low": {
                "cloud": ["AWS Free Tier", "Heroku", "Vercel", "Netlify"],
                "database": ["PostgreSQL", "MySQL", "SQLite"],
                "monitoring": ["Free tiers of DataDog", "New Relic free"]
            },
            "medium": {
                "cloud": ["AWS", "Azure", "GCP standard tiers"],
                "database": ["Managed PostgreSQL", "MongoDB Atlas"],
                "monitoring": ["DataDog", "New Relic", "Grafana"]
            },
            "high": {
                "cloud": ["Enterprise AWS/Azure/GCP"],
                "database": ["Enterprise databases", "Multi-region setups"],
                "monitoring": ["Enterprise monitoring solutions"]
            }
        }

        app_type_key = application_type.lower()
        budget_key = budget_range.lower()

        # Get relevant tech stack
        relevant_stack = tech_stacks.get(app_type_key, tech_stacks["web app"])
        budget_options = budget_considerations.get(budget_key, budget_considerations["medium"])

        analysis = f"""
# Technology Stack Analysis for {application_type}

## Recommended Technology Stack

### Primary Recommendations:
"""

        for category, options in relevant_stack.items():
            analysis += f"\n**{category.replace('_', ' ').title()}:**\n"
            for i, option in enumerate(options[:3], 1):
                analysis += f"{i}. {option}\n"

        analysis += f"""
### Budget-Optimized Options ({budget_range} budget):

**Cloud Platform:** {', '.join(budget_options['cloud'][:2])}
**Database:** {', '.join(budget_options['database'][:2])}
**Monitoring:** {', '.join(budget_options['monitoring'][:2])}

## Technology Comparison Matrix

| Criteria | Option 1 | Option 2 | Option 3 |
|----------|----------|----------|----------|
| Learning Curve | Medium | Low | High |
| Community Support | Excellent | Good | Excellent |
| Performance | High | Medium | High |
| Scalability | Excellent | Good | Excellent |
| Cost | Medium | Low | High |

## Key Considerations:
- **Performance Requirements:** {requirements}
- **Team Expertise:** Consider existing team skills
- **Long-term Maintenance:** Choose mature, well-supported technologies
- **Integration Needs:** Ensure compatibility between chosen technologies
- **Deployment Complexity:** Balance features with operational overhead

## Risk Assessment:
- **Low Risk:** Established technologies with strong community support
- **Medium Risk:** Newer technologies with growing adoption
- **High Risk:** Cutting-edge technologies with limited production use
"""

        return analysis
