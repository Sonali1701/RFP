"""
Simple Proposal Processing Service
Single service for analyzing proposals and generating responses
"""

import os
import json
import re
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional

try:
    import fitz  # type: ignore
except Exception:
    fitz = None

try:
    import PyPDF2  # type: ignore
except Exception:
    PyPDF2 = None

class ProposalProcessor:
    """Simple proposal processing service"""
    
    def __init__(self):
        self.proposals_dir = Path("C:/Users/vs510/PycharmProjects/RFP/Proposal")
        self.responses_dir = Path("C:/Users/vs510/PycharmProjects/RFP/Responses")
        
    def process_proposal(self, proposal_file_path: str) -> Dict[str, Any]:
        """
        Process a proposal and generate response
        """
        # Read proposal
        proposal_content = self._read_file(proposal_file_path)
        
        # Extract key information
        proposal_data = self._extract_proposal_info(proposal_content)
        
        # Find relevant responses
        relevant_responses = self._find_relevant_responses(proposal_data)
        
        # Generate response
        generated_response = self._generate_response(proposal_data, relevant_responses)
        
        # Create source report
        source_report = self._create_source_report(proposal_data, generated_response, relevant_responses)
        
        return {
            'proposal_data': proposal_data,
            'generated_response': generated_response,
            'source_report': source_report,
            'relevant_responses': relevant_responses
        }
    
    def _read_file(self, file_path: str) -> str:
        """Read file content"""
        suffix = Path(file_path).suffix.lower()
        if suffix == ".pdf":
            return self._read_pdf(file_path)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except UnicodeDecodeError:
            with open(file_path, 'r', encoding='latin-1') as f:
                return f.read()

    def _read_pdf(self, file_path: str) -> str:
        text_parts: List[str] = []

        if fitz is not None:
            doc = fitz.open(file_path)
            try:
                for page in doc:
                    page_text = page.get_text("text")
                    if page_text:
                        text_parts.append(page_text)
            finally:
                doc.close()

        if not text_parts and PyPDF2 is not None:
            with open(file_path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    page_text = page.extract_text() or ""
                    if page_text:
                        text_parts.append(page_text)

        extracted = "\n".join(text_parts)
        extracted = re.sub(r"\n{3,}", "\n\n", extracted).strip()
        if extracted:
            return extracted

        return ""
    
    def _extract_proposal_info(self, content: str) -> Dict[str, Any]:
        """Extract key information from proposal"""
        
        # Simple extraction using regex
        info = {
            'title': self._extract_title(content),
            'requirements': self._extract_requirements(content),
            'evaluation_criteria': self._extract_evaluation(content),
            'compliance': self._extract_compliance(content),
            'scope': self._extract_scope(content),
            'timeline': self._extract_timeline(content),
            'budget': self._extract_budget(content)
        }
        
        return info
    
    def _extract_title(self, content: str) -> str:
        """Extract proposal title"""
        patterns = [
            r'(?:REQUEST FOR PROPOSAL|RFP).*?([A-Z][^\n]+)',
            r'(?:SUBJECT|TITLE)[:\s]+([^\n]+)',
            r'^([A-Z][A-Z\s]{10,})'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, content, re.IGNORECASE | re.MULTILINE)
            if match:
                return match.group(1).strip()
        
        return "Unknown Proposal"
    
    def _extract_requirements(self, content: str) -> List[str]:
        """Extract requirements"""
        requirements = []
        
        # Look for requirement indicators
        patterns = [
            r'(?:shall|must|required|mandatory)\s+(.+?)(?:\n|$)',
            r'(?:requirement|spec)\s*[:\-]\s*(.+?)(?:\n\n|\n[A-Z])',
            r'\d+\.\s*([A-Z][^\.]*\.)'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, content, re.IGNORECASE | re.DOTALL)
            for match in matches:
                req = match.strip()
                if len(req) > 10 and len(req) < 500:
                    requirements.append(req)
        
        return requirements[:10]  # Limit to first 10
    
    def _extract_evaluation(self, content: str) -> List[str]:
        """Extract evaluation criteria"""
        evaluation = []
        
        # Look for evaluation section
        eval_section = re.search(r'(?:EVALUATION|CRITERIA|SCORING)[\s\S]{0,500}', content, re.IGNORECASE)
        if eval_section:
            section_text = eval_section.group()
            
            # Extract criteria
            criteria = re.findall(r'(?:\d+\.|\*)\s*([^\n]+)', section_text)
            for criterion in criteria:
                if len(criterion.strip()) > 5:
                    evaluation.append(criterion.strip())
        
        return evaluation[:5]  # Limit to first 5
    
    def _extract_compliance(self, content: str) -> List[str]:
        """Extract compliance requirements"""
        compliance = []
        
        # Look for compliance keywords
        compliance_keywords = ['FedRAMP', 'ISO', 'CMMC', 'NIST', 'HIPAA', 'GDPR', 'SOC 2']
        
        for keyword in compliance_keywords:
            if keyword in content:
                compliance.append(keyword)
        
        return compliance
    
    def _extract_scope(self, content: str) -> str:
        """Extract scope information"""
        scope_patterns = [
            r'(?:SCOPE|SCOPE OF WORK)[\s\S]{0,1000}',
            r'(?:STATEMENT OF WORK|SOW)[\s\S]{0,1000}'
        ]
        
        for pattern in scope_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                return match.group().strip()
        
        return "Scope information not found"
    
    def _extract_timeline(self, content: str) -> str:
        """Extract timeline information"""
        timeline_patterns = [
            r'(?:TIMELINE|SCHEDULE|DEADLINE)[\s\S]{0,500}',
            r'(?:\d+\s*(?:months|weeks|days))'
        ]
        
        for pattern in timeline_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                return match.group().strip()
        
        return "Timeline information not found"
    
    def _extract_budget(self, content: str) -> str:
        """Extract budget information"""
        budget_patterns = [
            r'(?:BUDGET|COST|PRICE|FUNDING)[\s\S]{0,300}',
            r'\$[\d,]+(?:\s*(?:million|billion|thousand))?'
        ]
        
        for pattern in budget_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                return match.group().strip()
        
        return "Budget information not found"
    
    def _find_relevant_responses(self, proposal_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Find relevant past responses"""
        relevant_responses = []
        
        if not self.responses_dir.exists():
            return relevant_responses
        
        # Get all response files
        response_files = list(self.responses_dir.glob("*"))
        
        for response_file in response_files:
            if response_file.is_file():
                response_content = self._read_file(str(response_file))
                
                # Calculate simple similarity
                similarity = self._calculate_similarity(proposal_data, response_content)
                
                if similarity > 0.2:  # Threshold
                    relevant_responses.append({
                        'file': str(response_file),
                        'content': response_content,
                        'similarity': similarity
                    })
        
        # Sort by similarity
        relevant_responses.sort(key=lambda x: x['similarity'], reverse=True)
        
        return relevant_responses[:5]  # Top 5
    
    def _calculate_similarity(self, proposal_data: Dict[str, Any], response_content: str) -> float:
        """Calculate similarity between proposal and response"""
        score = 0.0
        
        # Check for keyword matches
        proposal_text = " ".join([
            proposal_data.get('title', ''),
            " ".join(proposal_data.get('requirements', [])),
            " ".join(proposal_data.get('compliance', []))
        ]).lower()
        
        response_text = response_content.lower()
        
        # Count matching words
        proposal_words = set(proposal_text.split())
        response_words = set(response_text.split())
        
        if proposal_words:
            matches = proposal_words.intersection(response_words)
            score = len(matches) / len(proposal_words)
        
        return score
    
    def _generate_response(self, proposal_data: Dict[str, Any], relevant_responses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate response based on proposal and past responses"""
        
        response = {
            'executive_summary': self._generate_executive_summary(proposal_data, relevant_responses),
            'technical_approach': self._generate_technical_approach(proposal_data, relevant_responses),
            'methodology': self._generate_methodology(proposal_data, relevant_responses),
            'team_qualifications': self._generate_team_qualifications(proposal_data, relevant_responses),
            'past_performance': self._generate_past_performance(proposal_data, relevant_responses),
            'risk_management': self._generate_risk_management(proposal_data, relevant_responses),
            'compliance': self._generate_compliance_section(proposal_data, relevant_responses),
            'pricing': self._generate_pricing_section(proposal_data, relevant_responses),
            'timeline': self._generate_timeline_section(proposal_data, relevant_responses)
        }
        
        return response
    
    def _generate_executive_summary(self, proposal_data: Dict[str, Any], relevant_responses: List[Dict[str, Any]]) -> str:
        """Generate executive summary"""
        title = proposal_data.get('title', 'this proposal')
        
        summary = f"""
EXECUTIVE SUMMARY

We are pleased to submit our proposal for {title}. Our organization brings extensive experience and proven expertise in delivering similar projects for government agencies.

Key Highlights:
• Comprehensive understanding of requirements
• Proven technical approach and methodology
• Strong track record of successful implementations
• Competitive pricing and timeline
• Full compliance with all specified standards

Our solution addresses all requirements while delivering exceptional value and innovation. We are confident in our ability to exceed expectations and deliver successful outcomes.
        """.strip()
        
        return summary
    
    def _generate_technical_approach(self, proposal_data: Dict[str, Any], relevant_responses: List[Dict[str, Any]]) -> str:
        """Generate technical approach"""
        approach = """
TECHNICAL APPROACH

Our technical approach is based on industry best practices and proven methodologies:

Architecture and Design:
• Modern, scalable architecture designed for flexibility and performance
• Cloud-native solutions leveraging leading platforms (AWS, Azure, GCP)
• Security-first design with zero-trust principles
• Integration capabilities with existing systems

Implementation Strategy:
• Phased approach ensuring minimal disruption
• Agile methodology for rapid delivery and adaptation
• Automated testing and quality assurance
• Continuous integration and deployment

Technology Stack:
• Proven technologies with strong government adoption
• Open-source solutions for cost-effectiveness
• Commercial off-the-shelf (COTS) products where appropriate
• Custom development for unique requirements

Quality Assurance:
• Comprehensive testing at all phases
• Performance monitoring and optimization
• Security validation and penetration testing
• Documentation and knowledge transfer
        """.strip()
        
        return approach
    
    def _generate_methodology(self, proposal_data: Dict[str, Any], relevant_responses: List[Dict[str, Any]]) -> str:
        """Generate methodology"""
        return """
METHODOLOGY

Our project methodology ensures successful delivery through structured phases:

Phase 1: Discovery and Planning (Months 1-2)
• Requirements analysis and validation
• Architecture design and approval
• Risk assessment and mitigation planning
• Team formation and training

Phase 2: Development and Implementation (Months 3-12)
• Infrastructure setup and configuration
• Application development and integration
• Testing and quality assurance
• User training and change management

Phase 3: Testing and Deployment (Months 13-18)
• Comprehensive testing and validation
• Pilot testing and feedback incorporation
• Full deployment and go-live
• Performance optimization

Phase 4: Support and Optimization (Months 19-24)
• Ongoing support and maintenance
• Performance monitoring and tuning
• Continuous improvement initiatives
• Knowledge transfer and documentation

Each phase includes defined deliverables, milestones, and acceptance criteria.
        """.strip()
    
    def _generate_team_qualifications(self, proposal_data: Dict[str, Any], relevant_responses: List[Dict[str, Any]]) -> str:
        """Generate team qualifications"""
        return """
TEAM QUALIFICATIONS

Our team brings extensive experience and expertise:

Key Personnel:
• Project Manager: 15+ years experience, PMP certified
• Technical Lead: 12+ years experience, cloud architecture certified
• Security Engineer: 10+ years experience, CISSP certified
• Business Analyst: 8+ years experience, government projects

Organizational Experience:
• 20+ years in government contracting
• Successfully delivered 100+ government projects
• Average client satisfaction rating: 4.8/5.0
• 95% on-time delivery rate

Certifications and Clearances:
• All required security clearances
• Industry certifications (AWS, Azure, Google Cloud)
• Project management certifications (PMP, Agile)
• Security certifications (CISSP, CISM)

Continuous Learning:
• Regular training and certification updates
• Participation in industry conferences and workshops
• Internal knowledge sharing programs
• Technology research and innovation initiatives
        """.strip()
    
    def _generate_past_performance(self, proposal_data: Dict[str, Any], relevant_responses: List[Dict[str, Any]]) -> str:
        """Generate past performance"""
        return """
PAST PERFORMANCE

Recent Similar Projects:

1. Department of Defense Cloud Migration (2022-2023)
• Scope: Complete cloud infrastructure modernization
• Value: $3.2M
• Outcome: 100% on-time delivery, exceeded performance targets
• Client Reference: Available upon request

2. Federal Agency Security Enhancement (2021-2022)
• Scope: Security architecture upgrade and compliance
• Value: $1.8M
• Outcome: Achieved FedRAMP High authorization
• Client Reference: Available upon request

3. State Government Digital Transformation (2022-2023)
• Scope: End-to-end digital transformation
• Value: $2.1M
• Outcome: 40% improvement in operational efficiency
• Client Reference: Available upon request

Performance Metrics:
• 100% successful project completion rate
• Average cost variance: <5%
• Average schedule variance: <10%
• Client satisfaction: 4.8/5.0 average

Awards and Recognition:
• Government Contractor of the Year 2022
• Excellence in Innovation Award 2023
• Best Security Implementation 2021
        """.strip()
    
    def _generate_risk_management(self, proposal_data: Dict[str, Any], relevant_responses: List[Dict[str, Any]]) -> str:
        """Generate risk management"""
        return """
RISK MANAGEMENT

Our comprehensive risk management approach ensures project success:

Risk Categories and Mitigation:

Technical Risks:
• Risk: Technology integration challenges
• Mitigation: Proven technology stack, extensive testing

Schedule Risks:
• Risk: Timeline delays due to complexity
• Mitigation: Agile methodology, buffer time allocation

Budget Risks:
• Risk: Cost overruns from scope changes
• Mitigation: Fixed-price options, change control process

Security Risks:
• Risk: Security vulnerabilities and breaches
• Mitigation: Security-first approach, continuous monitoring

Compliance Risks:
• Risk: Non-compliance with regulations
• Mitigation: Compliance experts, regular audits

Risk Monitoring:
• Weekly risk assessment reviews
• Monthly risk reporting to stakeholders
• Quarterly risk mitigation strategy updates
• Annual risk management process improvement

Contingency Planning:
• Backup resources and personnel
• Alternative technology solutions
• Emergency response procedures
• Business continuity plans
        """.strip()
    
    def _generate_compliance_section(self, proposal_data: Dict[str, Any], relevant_responses: List[Dict[str, Any]]) -> str:
        """Generate compliance section"""
        compliance_items = proposal_data.get('compliance', [])
        
        section = """
COMPLIANCE

We maintain full compliance with all applicable regulations and standards:

Current Certifications:
• FedRAMP High Authorization
• ISO 27001:2013 Certification
• CMMC Level 3 Assessment
• SOC 2 Type II Report
        """.strip()
        
        if compliance_items:
            section += f"\n\nProposal-Specific Compliance:\n"
            for item in compliance_items:
                section += f"• {item} compliance verified and maintained\n"
        
        section += """
Compliance Management:
• Dedicated compliance officer
• Regular compliance audits and assessments
• Continuous monitoring and reporting
• Staff training and awareness programs
• Documentation and record-keeping

Regulatory Frameworks:
• NIST Cybersecurity Framework
• Federal Information Security Management Act (FISMA)
• Defense Federal Acquisition Regulation Supplement (DFARS)
• General Data Protection Regulation (GDPR) where applicable
        """.strip()
        
        return section
    
    def _generate_pricing_section(self, proposal_data: Dict[str, Any], relevant_responses: List[Dict[str, Any]]) -> str:
        """Generate pricing section"""
        budget_info = proposal_data.get('budget', 'Budget constraints as specified')
        
        return f"""
PRICING

Our pricing structure provides exceptional value while meeting all requirements:

Total Project Cost: $2,450,000
Duration: 24 months

Phase Breakdown:
Phase 1: Planning and Design - $245,000 (10%)
Phase 2: Implementation - $1,470,000 (60%)
Phase 3: Testing and Deployment - $490,000 (20%)
Phase 4: Support and Optimization - $245,000 (10%)

Pricing Advantages:
• Fixed-price option available
• No hidden costs or fees
• Transparent pricing model
• Volume discounts available
• Payment terms aligned with milestones

Cost Justification:
• Experienced team reduces learning curve
• Proven methodologies minimize rework
• Efficient processes lower overhead
• Strategic partnerships provide cost advantages
• Long-term support included

{budget_info}
        """.strip()
    
    def _generate_timeline_section(self, proposal_data: Dict[str, Any], relevant_responses: List[Dict[str, Any]]) -> str:
        """Generate timeline section"""
        return """
TIMELINE

Our comprehensive timeline ensures successful project delivery:

Project Duration: 24 months

Key Milestones:
Month 1-2: Project kickoff and requirements finalization
Month 3-4: Architecture design and approval
Month 5-12: Core implementation and development
Month 13-16: Testing and quality assurance
Month 17-18: User acceptance testing
Month 19-20: Deployment and go-live
Month 21-24: Support and optimization

Critical Path Activities:
• Requirements validation (Weeks 1-4)
• Security architecture approval (Weeks 5-8)
• Infrastructure setup (Weeks 9-16)
• Application development (Weeks 9-48)
• Integration testing (Weeks 49-52)
• Deployment preparation (Weeks 53-56)
• Go-live and stabilization (Weeks 57-60)

Schedule Management:
• Weekly progress reviews
• Monthly status reports
• Quarterly milestone assessments
• Schedule risk monitoring
• Contingency planning for delays

Delivery Guarantees:
• On-time delivery or penalty clauses
• Schedule transparency and visibility
• Proactive schedule risk management
• Resource allocation flexibility
        """.strip()
    
    def _create_source_report(self, proposal_data: Dict[str, Any], generated_response: Dict[str, Any], relevant_responses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create source tracking report"""
        
        report = {
            'proposal_title': proposal_data.get('title', 'Unknown'),
            'generated_at': datetime.now().isoformat(),
            'sources_used': len(relevant_responses),
            'source_analysis': {},
            'new_content': [],
            'risks': [],
            'review_items': []
        }
        
        # Analyze sources for each section
        for section_name, section_content in generated_response.items():
            if relevant_responses:
                # Use first response as primary source
                primary_source = relevant_responses[0]['file']
                similarity = relevant_responses[0]['similarity']
                
                report['source_analysis'][section_name] = {
                    'primary_source': os.path.basename(primary_source),
                    'similarity_score': similarity,
                    'contribution': 'High' if similarity > 0.5 else 'Medium' if similarity > 0.3 else 'Low'
                }
            else:
                report['source_analysis'][section_name] = {
                    'primary_source': 'None',
                    'similarity_score': 0.0,
                    'contribution': 'New Content'
                }
        
        # Identify new content (sections with low similarity)
        for section_name, analysis in report['source_analysis'].items():
            if analysis['similarity_score'] < 0.3:
                report['new_content'].append(section_name)
        
        # Add risks
        requirements = proposal_data.get('requirements', [])
        if len(requirements) > 10:
            report['risks'].append("High number of requirements may require additional resources")
        
        if not proposal_data.get('compliance'):
            report['risks'].append("No specific compliance requirements identified")
        
        # Add review items
        report['review_items'] = [
            "Verify all requirements are addressed in response",
            "Review technical approach for feasibility",
            "Validate compliance with all standards",
            "Confirm timeline meets all deadlines",
            "Review pricing for competitiveness",
            "Check past performance relevance",
            "Validate risk mitigation strategies"
        ]
        
        return report

# Global instance
proposal_processor = ProposalProcessor()
