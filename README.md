# Software Architecture Design Crew

A CrewAI-powered multi-agent system that collaborates to design comprehensive software architecture for any application. This crew consists of 5 specialized AI agents working together to analyze requirements, design system architecture, select technologies, plan security, and optimize performance.

## 🚀 Features

- **Requirements Analysis** - Comprehensive functional and non-functional requirements gathering
- **System Architecture Design** - Scalable architecture patterns and component design
- **Technology Selection** - Optimal tech stack recommendations with trade-off analysis
- **Security Planning** - OWASP compliance, threat modeling, and security architecture
- **Performance Optimization** - Scalability planning, caching strategies, and monitoring
- **Integrated Documentation** - Complete architecture specification output

## 🤖 AI Agents

### 1. Requirements Analyst
- Analyzes business requirements and constraints
- Documents user stories and acceptance criteria
- Identifies system boundaries and assumptions

### 2. System Architect
- Designs overall system structure and components
- Defines architectural patterns and design decisions
- Plans for scalability and maintainability
- **Tools**: Architecture Pattern Validator, Performance Calculator

### 3. Technology Specialist
- Selects optimal technology stack
- Evaluates frameworks, databases, and cloud services
- Provides technology decision matrix with pros/cons
- **Tools**: Technology Stack Analyzer

### 4. Security Engineer
- Designs comprehensive security architecture
- Ensures OWASP compliance and best practices
- Plans authentication, authorization, and data protection
- **Tools**: Security Checklist Generator

### 5. Performance Engineer
- Plans performance optimization strategies
- Designs caching, load balancing, and monitoring
- Calculates resource requirements and scaling needs
- **Tools**: Performance Calculator

## 🛠️ Custom Tools

- **Technology Stack Analyzer** - Compares and recommends tech stacks
- **Architecture Pattern Validator** - Validates design patterns and identifies anti-patterns
- **Performance Calculator** - Estimates resource needs and performance metrics
- **Security Checklist Generator** - Creates security requirements and compliance checklists

## 📋 Prerequisites

- Python >=3.10 <3.13
- CrewAI installed (`uv tool install crewai`)
- OpenAI API key or Google API key

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone <repository-url>
cd software_system_design_crew
```

### 2. Install Dependencies
```bash
crewai install
```

### 3. Configure Environment
Create a `.env` file with your API key:
```bash
# For OpenAI (recommended)
OPENAI_API_KEY=your_openai_api_key_here
MODEL=gpt-4o-mini

# OR for Google Gemini
GOOGLE_API_KEY=your_google_api_key_here
MODEL=gemini-1.5-flash
```

### 4. Customize Your Project
Edit `src/software_system_design_crew/main.py` and update the inputs:

```python
inputs = {
    'application_type': 'Your application type',  # e.g., 'Mobile app', 'API service'
    'user_load': 'Expected user load',           # e.g., '1,000 users', '50,000 requests/sec'
    'timeline': 'Project timeline'               # e.g., '3 months', '1 year'
}
```

### 5. Run the Crew
```bash
crewai run
```

## 📊 Output

The crew generates a comprehensive `software_architecture_specification.md` file containing:

- **Requirements Analysis** - Functional/non-functional requirements
- **System Architecture** - High-level design and component breakdown
- **Technology Stack** - Recommended technologies with justification
- **Security Architecture** - Security controls and compliance measures
- **Performance Strategy** - Optimization and scaling recommendations
- **Implementation Roadmap** - Phases, milestones, and next steps

## 🎯 Example Use Cases

### Web Application
```python
inputs = {
    'application_type': 'E-commerce web application',
    'user_load': '10,000 concurrent users',
    'timeline': '8 months'
}
```

### Mobile App
```python
inputs = {
    'application_type': 'Social media mobile app',
    'user_load': '100,000 daily active users',
    'timeline': '12 months'
}
```

### API Service
```python
inputs = {
    'application_type': 'RESTful API service',
    'user_load': '50,000 requests per second',
    'timeline': '4 months'
}
```

### Microservices Platform
```python
inputs = {
    'application_type': 'Microservices platform',
    'user_load': '1 million transactions per day',
    'timeline': '18 months'
}
```

## 🔧 Customization

### Adding New Agents
1. Define agent in `src/software_system_design_crew/config/agents.yaml`
2. Add agent method in `src/software_system_design_crew/crew.py`
3. Assign relevant tools to the agent

### Creating Custom Tools
1. Create tool file in `src/software_system_design_crew/tools/`
2. Implement `BaseTool` class with `_run` method
3. Add tool to `__init__.py` and assign to agents

### Modifying Tasks
Edit `src/software_system_design_crew/config/tasks.yaml` to:
- Change task descriptions and expected outputs
- Modify task dependencies with `context` parameter
- Add new tasks to the workflow

## 🧪 Testing

Run with different scenarios:
```bash
# Test with different inputs
crewai run

# Train the crew (requires iterations and filename)
crewai train 5 training_data.pkl

# Replay specific task
crewai replay <task_id>
```

## 📝 Project Structure

```
software_system_design_crew/
├── src/
│   └── software_system_design_crew/
│       ├── __init__.py
│       ├── main.py                 # Entry point with inputs
│       ├── crew.py                 # Crew configuration
│       ├── config/
│       │   ├── agents.yaml         # Agent definitions
│       │   └── tasks.yaml          # Task definitions
│       └── tools/                  # Custom tools
│           ├── __init__.py
│           ├── technology_stack_analyzer.py
│           ├── architecture_pattern_validator.py
│           ├── performance_calculator.py
│           └── security_checklist_generator.py
├── .env                           # Environment variables
├── .gitignore
├── pyproject.toml
└── README.md
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built with [CrewAI](https://crewai.com)
- Inspired by software architecture best practices
- Uses OpenAI GPT models for AI agents
