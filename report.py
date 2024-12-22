import requests
from datetime import datetime, timezone
import logging
import os
from typing import Dict, List, Optional, Tuple

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class BrandAnalysisFramework:
    def __init__(self, api_url: str, api_key: str):
        self.api_url = api_url
        self.api_key = api_key
        self.current_date = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        self.username = "wanghaisheng"
        self.section_prompts = self._initialize_prompts()

    def _initialize_prompts(self) -> Dict[str, Dict]:
        """Initialize optimized analysis prompts."""
        return {
            "executive_summary": {
                "title": "Executive Summary",
                "prompt": """
Provide a comprehensive executive summary for {brand_name} analyzing:

1. Brand Overview
- Core business and value proposition
- Market positioning and target audience
- Key differentiators and unique selling points

2. Legitimacy Assessment
- Overall trustworthiness rating
- Key strengths and potential concerns
- Market reputation and presence

3. Key Findings
- Trust indicators and red flags
- Competitive advantages
- Areas requiring consumer attention

Format: Clear, concise paragraphs with actionable insights
Length: 3-4 paragraphs
Tone: Professional and objective
"""
            },
            "trust_analysis": {
                "title": "Trust and Risk Analysis",
                "prompt": """
Conduct a detailed trust and risk analysis for {brand_name}:

1. Trust Indicators
- Business registration and legal compliance
- Industry certifications and partnerships
- Market presence and history
- Professional associations and acknowledgments

2. Risk Assessment
- Common consumer concerns
- Reported issues and complaints
- Security and privacy considerations
- Financial stability indicators

3. Verification Methods
- Available trust verification tools
- Background check resources
- Consumer protection measures

Provide specific examples and evidence for each point.
"""
            },
            "market_legitimacy": {
                "title": "Market and Industry Legitimacy",
                "prompt": """
Evaluate {brand_name}'s market and industry legitimacy:

1. Industry Position
- Market share and competitive standing
- Industry reputation and recognition
- Compliance with standards
- Professional affiliations

2. Business Practices
- Operational transparency
- Ethical standards
- Environmental responsibility
- Labor practices

3. Market Performance
- Customer satisfaction metrics
- Growth and stability indicators
- Innovation and adaptation
- Industry benchmarks

Include comparative analysis with industry standards.
"""
            },
            "customer_experience": {
                "title": "Customer Experience Analysis",
                "prompt": """
Analyze the customer experience with {brand_name}:

1. Product/Service Quality
- Quality consistency
- Value for money
- Performance metrics
- Customer satisfaction rates

2. Customer Service
- Response time and accessibility
- Problem resolution effectiveness
- Communication channels
- Support quality

3. Customer Feedback Analysis
- Review authenticity assessment
- Common praise points
- Recurring complaints
- Resolution patterns

Include specific examples and statistical data where available.
"""
            },
            "security_privacy": {
                "title": "Security and Privacy Assessment",
                "prompt": """
Evaluate {brand_name}'s security and privacy measures:

1. Data Protection
- Privacy policy analysis
- Data collection practices
- Information security measures
- Compliance with regulations

2. Transaction Security
- Payment processing security
- Fraud prevention measures
- Refund and dispute policies
- Financial transaction safeguards

3. Online Safety
- Website security features
- User data protection
- Third-party security certifications
- Incident response procedures

Focus on concrete measures and verifiable security features.
"""
            },
            "recommendations": {
                "title": "Consumer Recommendations",
                "prompt": """
Provide detailed recommendations regarding {brand_name}:

1. Consumer Guidance
- Due diligence checklist
- Risk mitigation strategies
- Best practices for engagement
- Warning signs to watch

2. Decision Support
- Pros and cons analysis
- Alternative options
- Safety measures
- Value assessment

3. Action Items
- Verification steps
- Protection measures
- Engagement guidelines
- Resource links

Make recommendations specific and actionable.
"""
            }
        }

    def _call_api(self, prompt: str, max_tokens: int = 1000) -> str:
        """Make API call with error handling."""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": "gpt-4",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": max_tokens,
                "temperature": 0.7
            }
            
            response = requests.post(self.api_url, json=data, headers=headers)
            
            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"].strip()
            else:
                logging.error(f"API call failed: {response.status_code}")
                return ""
                
        except Exception as e:
            logging.error(f"API call error: {e}")
            return ""

    def generate_analysis(self, brand_data: Dict) -> Tuple[str, str]:
        """Generate complete brand analysis report."""
        brand_name = brand_data.get('name', '')
        report_content = f"""# Brand Legitimacy Analysis: {brand_name}
Generated on: {self.current_date}
Analyst: {self.username}

"""
        # Generate table of contents
        toc = "## Table of Contents\n\n"
        for section in self.section_prompts.values():
            toc += f"- [{section['title']}](#{section['title'].lower().replace(' ', '-')})\n"
        report_content += f"{toc}\n---\n\n"

        # Generate each section
        for section_name, section_data in self.section_prompts.items():
            prompt = section_data['prompt'].format(brand_name=brand_name)
            content = self._call_api(prompt)
            report_content += f"## {section_data['title']}\n\n{content}\n\n---\n\n"

        return report_content, f"Brand Analysis - {brand_name}"

    def save_report(self, content: str, brand_name: str, output_dir: str = "reports") -> str:
        """Save the generated report to file."""
        try:
            os.makedirs(output_dir, exist_ok=True)
            
            filename = f"{brand_name.lower().replace(' ', '-')}-analysis-{datetime.now().strftime('%Y%m%d')}.md"
            filepath = os.path.join(output_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            logging.info(f"Report saved to: {filepath}")
            return filepath
            
        except Exception as e:
            logging.error(f"Error saving report: {e}")
            return ""

def main():
    # Configuration
    API_URL = "YOUR_API_URL"
    API_KEY = "YOUR_API_KEY"
    
    # Sample brand data
    brand_data = {
        "name": "GitHub Daily Event Blog Update Tool",
        "industry": "Developer Tools",
        "description": "A tool for converting GitHub events to blog updates",
        "website": "https://github.com/wanghaisheng/github-daily-event-to-blog-update",
        "features": [
            "GitHub event processing",
            "Blog content generation",
            "Automated updates"
        ]
    }
    
    # Initialize analyzer
    analyzer = BrandAnalysisFramework(API_URL, API_KEY)
    
    # Generate report
    report_content, title = analyzer.generate_analysis(brand_data)
    
    # Save report
    report_path = analyzer.save_report(report_content, brand_data['name'])
    
    if report_path:
        print(f"Analysis report generated successfully: {report_path}")
    else:
        print("Failed to generate report")

if __name__ == "__main__":
    main()
