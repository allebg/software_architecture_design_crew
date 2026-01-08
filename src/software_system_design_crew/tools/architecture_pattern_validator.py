from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field


class ArchitecturePatternValidatorInput(BaseModel):
    """Input schema for Architecture Pattern Validator."""
    architecture_description: str = Field(..., description="Description of the proposed architecture")
    application_type: str = Field(..., description="Type of application being built")
    expected_load: str = Field(..., description="Expected user load and traffic patterns")


class ArchitecturePatternValidator(BaseTool):
    name: str = "Architecture Pattern Validator"
    description: str = (
        "Validates architectural decisions against best practices and design principles. "
        "Identifies potential anti-patterns, suggests improvements, and ensures scalability. "
        "Provides recommendations for architectural patterns based on application requirements."
    )
    args_schema: Type[BaseModel] = ArchitecturePatternValidatorInput

    def _run(self, architecture_description: str, application_type: str, expected_load: str) -> str:
        # Architecture patterns database
        patterns = {
            "microservices": {
                "best_for": ["high scalability", "large teams", "complex domains"],
                "pros": ["Independent deployment", "Technology diversity", "Fault isolation"],
                "cons": ["Complexity", "Network overhead", "Data consistency challenges"],
                "anti_patterns": ["Distributed monolith", "Chatty services", "Shared databases"]
            },
            "monolithic": {
                "best_for": ["small teams", "simple domains", "rapid prototyping"],
                "pros": ["Simple deployment", "Easy testing", "Performance"],
                "cons": ["Scaling limitations", "Technology lock-in", "Large codebase"],
                "anti_patterns": ["Big ball of mud", "God object", "Tight coupling"]
            },
            "layered": {
                "best_for": ["enterprise applications", "clear separation of concerns"],
                "pros": ["Clear structure", "Testability", "Maintainability"],
                "cons": ["Performance overhead", "Rigid structure"],
                "anti_patterns": ["Skip layers", "Circular dependencies"]
            },
            "event_driven": {
                "best_for": ["real-time systems", "loose coupling", "scalability"],
                "pros": ["Loose coupling", "Scalability", "Responsiveness"],
                "cons": ["Complexity", "Debugging difficulty", "Event ordering"],
                "anti_patterns": ["Event storm", "Missing events", "Tight event coupling"]
            }
        }

        # Analyze architecture description for patterns
        desc_lower = architecture_description.lower()
        detected_patterns = []
        
        if any(word in desc_lower for word in ["microservice", "service", "api gateway"]):
            detected_patterns.append("microservices")
        if any(word in desc_lower for word in ["monolith", "single application", "one deployment"]):
            detected_patterns.append("monolithic")
        if any(word in desc_lower for word in ["layer", "tier", "presentation", "business", "data"]):
            detected_patterns.append("layered")
        if any(word in desc_lower for word in ["event", "message", "queue", "pub/sub"]):
            detected_patterns.append("event_driven")

        # Load analysis
        load_level = "low"
        if any(word in expected_load.lower() for word in ["high", "million", "thousands"]):
            load_level = "high"
        elif any(word in expected_load.lower() for word in ["medium", "moderate", "hundreds"]):
            load_level = "medium"

        validation_report = f"""
# Architecture Pattern Validation Report

## Detected Patterns:
{', '.join(detected_patterns) if detected_patterns else 'No specific patterns detected'}

## Pattern Analysis:
"""

        for pattern in detected_patterns:
            if pattern in patterns:
                p = patterns[pattern]
                validation_report += f"""
### {pattern.replace('_', ' ').title()} Pattern

**Strengths:**
{chr(10).join(f'- {pro}' for pro in p['pros'])}

**Potential Issues:**
{chr(10).join(f'- {con}' for con in p['cons'])}

**Watch out for these anti-patterns:**
{chr(10).join(f'- {anti}' for anti in p['anti_patterns'])}
"""

        validation_report += f"""
## Recommendations for {application_type} with {expected_load} load:

### Architecture Suitability:
"""

        if load_level == "high":
            validation_report += """
- **Microservices** recommended for high scalability
- Consider **Event-driven architecture** for real-time processing
- Implement **CQRS** pattern for read/write optimization
- Use **Circuit breaker** pattern for fault tolerance
"""
        elif load_level == "medium":
            validation_report += """
- **Modular monolith** or **microservices** both viable
- **Layered architecture** suitable for maintainability
- Consider **Database per service** if using microservices
"""
        else:
            validation_report += """
- **Monolithic architecture** sufficient for current needs
- **Layered architecture** for clear separation
- Plan for future scaling with modular design
"""

        validation_report += """
## Design Principles Checklist:

### ✅ SOLID Principles
- [ ] Single Responsibility Principle
- [ ] Open/Closed Principle  
- [ ] Liskov Substitution Principle
- [ ] Interface Segregation Principle
- [ ] Dependency Inversion Principle

### ✅ Scalability Patterns
- [ ] Load balancing strategy
- [ ] Caching implementation
- [ ] Database sharding/partitioning
- [ ] Asynchronous processing

### ✅ Reliability Patterns
- [ ] Circuit breaker implementation
- [ ] Retry mechanisms with backoff
- [ ] Health checks and monitoring
- [ ] Graceful degradation

## Potential Issues Identified:
- Review service boundaries for proper domain alignment
- Ensure data consistency strategy is defined
- Validate communication patterns between components
- Check for proper error handling and logging

## Next Steps:
1. Review detected anti-patterns in current design
2. Implement recommended patterns for your use case
3. Plan for monitoring and observability
4. Design for testability and maintainability
"""

        return validation_report
