from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field


class SecurityChecklistInput(BaseModel):
    """Input schema for Security Checklist Generator."""
    application_type: str = Field(..., description="Type of application (web app, mobile app, API, etc.)")
    data_sensitivity: str = Field(..., description="Level of data sensitivity (low, medium, high)")
    compliance_requirements: str = Field(..., description="Required compliance frameworks (GDPR, HIPAA, SOX, etc.)")


class SecurityChecklistGenerator(BaseTool):
    name: str = "Security Checklist Generator"
    description: str = (
        "Generates comprehensive security requirements and validates security measures. "
        "Provides OWASP compliance checking, threat modeling templates, and security testing recommendations. "
        "Covers authentication, authorization, data protection, and compliance requirements."
    )
    args_schema: Type[BaseModel] = SecurityChecklistInput

    def _run(self, application_type: str, data_sensitivity: str, compliance_requirements: str) -> str:
        # OWASP Top 10 2021
        owasp_top_10 = [
            "Broken Access Control",
            "Cryptographic Failures", 
            "Injection",
            "Insecure Design",
            "Security Misconfiguration",
            "Vulnerable and Outdated Components",
            "Identification and Authentication Failures",
            "Software and Data Integrity Failures",
            "Security Logging and Monitoring Failures",
            "Server-Side Request Forgery (SSRF)"
        ]

        # Compliance frameworks
        compliance_frameworks = {
            "gdpr": {
                "name": "General Data Protection Regulation",
                "requirements": [
                    "Data encryption at rest and in transit",
                    "Right to be forgotten implementation",
                    "Data breach notification (72 hours)",
                    "Privacy by design principles",
                    "Consent management system",
                    "Data processing audit logs"
                ]
            },
            "hipaa": {
                "name": "Health Insurance Portability and Accountability Act",
                "requirements": [
                    "PHI encryption requirements",
                    "Access controls and audit logs",
                    "Business associate agreements",
                    "Risk assessment procedures",
                    "Incident response procedures",
                    "Employee training programs"
                ]
            },
            "sox": {
                "name": "Sarbanes-Oxley Act",
                "requirements": [
                    "Financial data integrity controls",
                    "Change management procedures",
                    "Access control documentation",
                    "Audit trail requirements",
                    "Segregation of duties",
                    "Regular security assessments"
                ]
            }
        }

        # Security measures by data sensitivity
        security_levels = {
            "low": {
                "authentication": ["Basic password requirements", "Session management"],
                "encryption": ["HTTPS/TLS", "Password hashing"],
                "monitoring": ["Basic logging", "Error tracking"]
            },
            "medium": {
                "authentication": ["Multi-factor authentication", "Password policies", "Account lockout"],
                "encryption": ["AES-256 encryption", "Key rotation", "Certificate management"],
                "monitoring": ["Security event logging", "Intrusion detection", "Regular audits"]
            },
            "high": {
                "authentication": ["Strong MFA", "Biometric authentication", "Zero-trust architecture"],
                "encryption": ["End-to-end encryption", "Hardware security modules", "Perfect forward secrecy"],
                "monitoring": ["Real-time threat detection", "SIEM integration", "Continuous monitoring"]
            }
        }

        sensitivity_level = data_sensitivity.lower()
        security_measures = security_levels.get(sensitivity_level, security_levels["medium"])

        security_report = f"""
# Security Architecture Report

## Application Security Profile
- **Application Type:** {application_type}
- **Data Sensitivity:** {data_sensitivity}
- **Compliance Requirements:** {compliance_requirements}

## OWASP Top 10 2021 Compliance Checklist

### Critical Security Controls:
"""

        for i, vulnerability in enumerate(owasp_top_10, 1):
            security_report += f"{i}. **{vulnerability}**\n   - [ ] Mitigation strategy implemented\n   - [ ] Testing procedures defined\n   - [ ] Monitoring controls in place\n\n"

        security_report += f"""
## Authentication & Authorization

### Authentication Requirements:
{chr(10).join(f'- {req}' for req in security_measures['authentication'])}

### Authorization Framework:
- [ ] Role-based access control (RBAC)
- [ ] Principle of least privilege
- [ ] API authentication (JWT/OAuth 2.0)
- [ ] Session management security
- [ ] Account lifecycle management

## Data Protection

### Encryption Requirements:
{chr(10).join(f'- {req}' for req in security_measures['encryption'])}

### Data Security Controls:
- [ ] Data classification scheme
- [ ] Data loss prevention (DLP)
- [ ] Secure data storage
- [ ] Secure data transmission
- [ ] Data backup encryption
- [ ] Secure data disposal

## Security Monitoring

### Monitoring & Logging:
{chr(10).join(f'- {req}' for req in security_measures['monitoring'])}

### Security Operations:
- [ ] Security incident response plan
- [ ] Vulnerability management program
- [ ] Security awareness training
- [ ] Regular security assessments
- [ ] Penetration testing schedule

## Application Security

### Secure Development:
- [ ] Security code review process
- [ ] Static application security testing (SAST)
- [ ] Dynamic application security testing (DAST)
- [ ] Interactive application security testing (IAST)
- [ ] Software composition analysis (SCA)
- [ ] Security testing in CI/CD pipeline

### Runtime Protection:
- [ ] Web application firewall (WAF)
- [ ] API rate limiting and throttling
- [ ] Input validation and sanitization
- [ ] Output encoding
- [ ] SQL injection prevention
- [ ] Cross-site scripting (XSS) protection
"""

        # Add compliance-specific requirements
        compliance_list = [c.strip().lower() for c in compliance_requirements.split(',')]
        
        for compliance in compliance_list:
            if compliance in compliance_frameworks:
                framework = compliance_frameworks[compliance]
                security_report += f"""
## {framework['name']} Compliance

### Required Controls:
{chr(10).join(f'- [ ] {req}' for req in framework['requirements'])}
"""

        security_report += f"""
## Infrastructure Security

### Network Security:
- [ ] Network segmentation
- [ ] Firewall configuration
- [ ] VPN for remote access
- [ ] DDoS protection
- [ ] SSL/TLS configuration
- [ ] Certificate management

### Cloud Security (if applicable):
- [ ] Identity and access management (IAM)
- [ ] Security groups and NACLs
- [ ] Encryption key management
- [ ] Cloud security posture management
- [ ] Container security scanning
- [ ] Serverless security controls

## Threat Modeling

### Threat Analysis Framework:
1. **Asset Identification**
   - Identify critical assets and data flows
   - Map trust boundaries
   - Document entry points

2. **Threat Identification**
   - Use STRIDE methodology
   - Identify potential attackers
   - Analyze attack vectors

3. **Vulnerability Assessment**
   - Technical vulnerabilities
   - Process vulnerabilities
   - Human factor vulnerabilities

4. **Risk Assessment**
   - Impact analysis
   - Likelihood assessment
   - Risk prioritization

## Security Testing Strategy

### Testing Types:
- [ ] **Penetration Testing:** Annual external assessment
- [ ] **Vulnerability Scanning:** Monthly automated scans
- [ ] **Code Security Review:** Every release
- [ ] **Security Regression Testing:** Continuous
- [ ] **Red Team Exercises:** Bi-annual (for high sensitivity)

### Security Metrics:
- Mean time to detect (MTTD) security incidents
- Mean time to respond (MTTR) to security incidents
- Number of vulnerabilities by severity
- Security training completion rates
- Compliance audit results

## Incident Response Plan

### Response Phases:
1. **Preparation:** Team, tools, and procedures
2. **Detection & Analysis:** Monitoring and triage
3. **Containment:** Immediate response actions
4. **Eradication:** Remove threat and vulnerabilities
5. **Recovery:** Restore normal operations
6. **Lessons Learned:** Post-incident review

### Communication Plan:
- Internal escalation procedures
- External notification requirements
- Regulatory reporting obligations
- Customer communication protocols

## Security Architecture Recommendations

### Immediate Priorities:
1. Implement multi-factor authentication
2. Enable comprehensive logging and monitoring
3. Conduct security architecture review
4. Establish vulnerability management process

### Medium-term Goals:
1. Implement zero-trust architecture
2. Deploy advanced threat detection
3. Establish security metrics and KPIs
4. Conduct regular security training

### Long-term Strategy:
1. Mature security operations center (SOC)
2. Implement security automation
3. Establish threat intelligence program
4. Achieve security certification compliance
"""

        return security_report
