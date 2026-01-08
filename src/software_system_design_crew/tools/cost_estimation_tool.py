from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field


class CostEstimationInput(BaseModel):
    """Input schema for Cost Estimation Tool."""
    project_scope: str = Field(..., description="Scope and complexity of the project")
    team_size: str = Field(..., description="Expected team size and composition")
    timeline: str = Field(..., description="Project timeline and milestones")
    infrastructure_requirements: str = Field(..., description="Infrastructure and hosting requirements")


class CostEstimationTool(BaseTool):
    name: str = "Cost Estimation Tool"
    description: str = (
        "Calculates comprehensive project costs including development, infrastructure, and operational expenses. "
        "Provides cost breakdowns, ROI analysis, and budget recommendations for software projects. "
        "Estimates licensing costs, cloud services, and maintenance expenses."
    )
    args_schema: Type[BaseModel] = CostEstimationInput

    def _run(self, project_scope: str, team_size: str, timeline: str, infrastructure_requirements: str) -> str:
        import re
        
        # Parse inputs
        team_numbers = re.findall(r'\d+', team_size)
        team_count = int(team_numbers[0]) if team_numbers else 5
        
        timeline_numbers = re.findall(r'\d+', timeline)
        months = int(timeline_numbers[0]) if timeline_numbers else 6
        
        # Cost calculations
        # Development costs (monthly rates in USD)
        roles_costs = {
            "senior_developer": 12000,
            "mid_developer": 8000,
            "junior_developer": 5000,
            "tech_lead": 15000,
            "architect": 18000,
            "devops": 10000,
            "qa_engineer": 7000,
            "ui_ux_designer": 8000,
            "product_manager": 12000,
            "scrum_master": 9000
        }
        
        # Estimate team composition based on size
        if team_count <= 3:
            team_composition = {
                "senior_developer": 1,
                "mid_developer": 1,
                "junior_developer": 1
            }
        elif team_count <= 6:
            team_composition = {
                "tech_lead": 1,
                "senior_developer": 2,
                "mid_developer": 2,
                "qa_engineer": 1
            }
        else:
            team_composition = {
                "architect": 1,
                "tech_lead": 1,
                "senior_developer": 3,
                "mid_developer": 3,
                "junior_developer": 2,
                "devops": 1,
                "qa_engineer": 2,
                "ui_ux_designer": 1,
                "product_manager": 1
            }
        
        # Calculate development costs
        monthly_dev_cost = sum(roles_costs[role] * count for role, count in team_composition.items())
        total_dev_cost = monthly_dev_cost * months
        
        # Infrastructure costs (monthly estimates)
        infra_base_cost = 500  # Basic hosting
        if "high" in infrastructure_requirements.lower() or "enterprise" in infrastructure_requirements.lower():
            infra_multiplier = 5
        elif "medium" in infrastructure_requirements.lower() or "scalable" in infrastructure_requirements.lower():
            infra_multiplier = 3
        else:
            infra_multiplier = 1
            
        monthly_infra_cost = infra_base_cost * infra_multiplier
        total_infra_cost = monthly_infra_cost * months
        
        # Additional costs
        licensing_cost = team_count * 200 * months  # Development tools and licenses
        testing_cost = total_dev_cost * 0.15  # 15% of dev cost for testing tools/services
        security_cost = total_dev_cost * 0.10  # 10% for security tools and audits
        contingency = (total_dev_cost + total_infra_cost) * 0.20  # 20% contingency
        
        # Total project cost
        total_cost = total_dev_cost + total_infra_cost + licensing_cost + testing_cost + security_cost + contingency
        
        # Operational costs (annual)
        annual_maintenance = total_dev_cost * 0.20  # 20% of dev cost annually
        annual_infra_ops = monthly_infra_cost * 12
        annual_licensing = team_count * 200 * 12
        
        cost_report = f"""
# Project Cost Estimation Report

## Project Overview
- **Scope:** {project_scope}
- **Team Size:** {team_count} members
- **Timeline:** {months} months
- **Infrastructure:** {infrastructure_requirements}

## Development Team Composition & Costs

### Team Structure:
"""
        
        for role, count in team_composition.items():
            role_name = role.replace('_', ' ').title()
            monthly_cost = roles_costs[role] * count
            total_role_cost = monthly_cost * months
            cost_report += f"- **{role_name}:** {count} × ${roles_costs[role]:,}/month = ${total_role_cost:,}\n"
        
        cost_report += f"""
### Development Cost Summary:
- **Monthly Development Cost:** ${monthly_dev_cost:,}
- **Total Development Cost:** ${total_dev_cost:,}

## Infrastructure Costs

### Cloud Infrastructure (Monthly):
- **Base Infrastructure:** ${infra_base_cost:,}
- **Scaling Factor:** {infra_multiplier}x
- **Monthly Infrastructure Cost:** ${monthly_infra_cost:,}
- **Total Infrastructure Cost ({months} months):** ${total_infra_cost:,}

### Infrastructure Breakdown:
- **Compute Resources:** ${monthly_infra_cost * 0.4:.0f}/month
- **Database Services:** ${monthly_infra_cost * 0.25:.0f}/month
- **Storage & CDN:** ${monthly_infra_cost * 0.15:.0f}/month
- **Networking & Security:** ${monthly_infra_cost * 0.10:.0f}/month
- **Monitoring & Logging:** ${monthly_infra_cost * 0.10:.0f}/month

## Additional Project Costs

### Tools & Licensing:
- **Development Tools:** ${licensing_cost:,}
- **Testing Tools & Services:** ${testing_cost:,}
- **Security Tools & Audits:** ${security_cost:,}

### Risk Management:
- **Contingency (20%):** ${contingency:,}

## Total Project Investment

| Category | Cost | Percentage |
|----------|------|------------|
| Development | ${total_dev_cost:,} | {(total_dev_cost/total_cost)*100:.1f}% |
| Infrastructure | ${total_infra_cost:,} | {(total_infra_cost/total_cost)*100:.1f}% |
| Tools & Licensing | ${licensing_cost:,} | {(licensing_cost/total_cost)*100:.1f}% |
| Testing | ${testing_cost:,} | {(testing_cost/total_cost)*100:.1f}% |
| Security | ${security_cost:,} | {(security_cost/total_cost)*100:.1f}% |
| Contingency | ${contingency:,} | {(contingency/total_cost)*100:.1f}% |
| **Total** | **${total_cost:,}** | **100%** |

## Operational Costs (Annual)

### Ongoing Expenses:
- **Maintenance & Support:** ${annual_maintenance:,}/year
- **Infrastructure Operations:** ${annual_infra_ops:,}/year
- **Software Licensing:** ${annual_licensing:,}/year
- **Security & Compliance:** ${annual_maintenance * 0.3:.0f}/year
- **Monitoring & Analytics:** ${annual_infra_ops * 0.1:.0f}/year

**Total Annual Operating Cost:** ${annual_maintenance + annual_infra_ops + annual_licensing + (annual_maintenance * 0.3) + (annual_infra_ops * 0.1):,.0f}

## Cost Optimization Strategies

### Development Cost Optimization:
- **Agile Development:** Reduce scope creep and rework
- **Code Reusability:** Leverage existing libraries and frameworks
- **Automation:** Implement CI/CD to reduce manual effort
- **Remote Team:** Consider distributed team for cost savings

### Infrastructure Cost Optimization:
- **Auto-scaling:** Pay only for resources used
- **Reserved Instances:** 30-60% savings for predictable workloads
- **Spot Instances:** Up to 90% savings for fault-tolerant workloads
- **Multi-cloud Strategy:** Optimize costs across providers

### Operational Cost Optimization:
- **Monitoring:** Proactive monitoring to prevent issues
- **Automation:** Reduce manual operational tasks
- **Performance Optimization:** Reduce resource consumption
- **Regular Reviews:** Quarterly cost optimization reviews

## ROI Analysis

### Revenue Projections (Assumptions):
- **Year 1 Revenue:** ${total_cost * 1.5:,.0f}
- **Year 2 Revenue:** ${total_cost * 2.5:,.0f}
- **Year 3 Revenue:** ${total_cost * 4:,.0f}

### Break-even Analysis:
- **Initial Investment:** ${total_cost:,}
- **Monthly Operating Cost:** ${(annual_maintenance + annual_infra_ops + annual_licensing)/12:,.0f}
- **Estimated Break-even:** 12-18 months

### 3-Year TCO (Total Cost of Ownership):
- **Initial Development:** ${total_cost:,}
- **3-Year Operations:** ${(annual_maintenance + annual_infra_ops + annual_licensing) * 3:,.0f}
- **Total 3-Year TCO:** ${total_cost + ((annual_maintenance + annual_infra_ops + annual_licensing) * 3):,.0f}

## Budget Recommendations

### Phase-based Budget Allocation:
1. **Phase 1 (MVP - {months//3} months):** ${total_cost * 0.4:,.0f}
2. **Phase 2 (Core Features - {months//3} months):** ${total_cost * 0.35:,.0f}
3. **Phase 3 (Advanced Features - {months//3} months):** ${total_cost * 0.25:,.0f}

### Risk Mitigation:
- **Reserve Fund:** ${contingency:,} (20% of project cost)
- **Scope Buffer:** Plan for 10-15% scope increase
- **Timeline Buffer:** Add 20% to timeline estimates

## Cost Monitoring & Control

### Key Metrics:
- **Burn Rate:** ${monthly_dev_cost + monthly_infra_cost:,}/month
- **Cost per Feature:** Track development cost per feature
- **Infrastructure Efficiency:** Cost per user/transaction
- **Team Productivity:** Story points per dollar spent

### Regular Reviews:
- **Weekly:** Team utilization and burn rate
- **Monthly:** Infrastructure costs and optimization
- **Quarterly:** ROI and budget variance analysis
- **Annually:** Total cost of ownership review
"""

        return cost_report
