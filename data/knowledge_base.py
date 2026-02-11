"""
Sample knowledge base documents for RetailPulse.
Used in Lab 09: Building a Semantic Search System.

In production, these would come from your actual documentation.
"""

DOCUMENTS = [
    {
        "id": "doc_001",
        "title": "Increasing Sales Revenue",
        "content": "To boost sales and increase revenue, focus on upselling existing customers, improving product recommendations, and optimizing pricing strategies. Customer retention is often more cost-effective than acquisition.",
        "category": "sales",
        "department": "marketing"
    },
    {
        "id": "doc_002", 
        "title": "Handling Customer Complaints",
        "content": "When dealing with negative customer feedback, listen actively, acknowledge the issue, apologize sincerely, and offer a solution. Document all complaints for quality improvement analysis.",
        "category": "support",
        "department": "customer_service"
    },
    {
        "id": "doc_003",
        "title": "Employee Onboarding Process",
        "content": "New employee orientation includes company overview, department introduction, system access setup, and initial training. Complete all HR paperwork within the first week.",
        "category": "hr",
        "department": "human_resources"
    },
    {
        "id": "doc_004",
        "title": "Product Return Policy",
        "content": "Customers can return products within 30 days of purchase for a full refund. Items must be in original packaging. Defective products can be exchanged at any time under warranty.",
        "category": "policy",
        "department": "operations"
    },
    {
        "id": "doc_005",
        "title": "Team Productivity Tips",
        "content": "Improve team collaboration by setting clear goals, using project management tools, holding regular standups, and minimizing unnecessary meetings. Focus on outcomes, not hours worked.",
        "category": "management",
        "department": "operations"
    },
    {
        "id": "doc_006",
        "title": "Data Privacy Guidelines",
        "content": "All customer data must be encrypted at rest and in transit. Access is limited to authorized personnel only. Report any data breaches to the security team immediately.",
        "category": "security",
        "department": "it"
    },
    {
        "id": "doc_007",
        "title": "Marketing Campaign Best Practices",
        "content": "Effective marketing campaigns start with clear audience targeting, compelling messaging, and measurable KPIs. A/B test all major campaigns before full rollout.",
        "category": "marketing",
        "department": "marketing"
    },
    {
        "id": "doc_008",
        "title": "Inventory Management",
        "content": "Maintain optimal stock levels by monitoring sales velocity, setting reorder points, and using demand forecasting. Avoid both stockouts and excess inventory.",
        "category": "operations",
        "department": "operations"
    },
    {
        "id": "doc_009",
        "title": "Remote Work Policy",
        "content": "Employees may work remotely up to 3 days per week. Ensure reliable internet connection, use company VPN for secure access, and maintain regular communication with your team.",
        "category": "hr",
        "department": "human_resources"
    },
    {
        "id": "doc_010",
        "title": "Customer Loyalty Program",
        "content": "Our loyalty program rewards repeat customers with points, exclusive discounts, and early access to sales. Members spend 40% more than non-members on average.",
        "category": "sales",
        "department": "marketing"
    },
    {
        "id": "doc_011",
        "title": "Bug Reporting Process",
        "content": "When you find a software bug, document the steps to reproduce it, capture screenshots, note the browser/device used, and submit a ticket in the issue tracker with severity level.",
        "category": "engineering",
        "department": "it"
    },
    {
        "id": "doc_012",
        "title": "Performance Review Guidelines",
        "content": "Annual performance reviews assess goal achievement, skill development, and cultural contribution. Prepare self-assessment one week before the review meeting.",
        "category": "hr",
        "department": "human_resources"
    },
]


def get_all_documents():
    """Return all documents."""
    return DOCUMENTS


def get_documents_by_category(category: str):
    """Return documents filtered by category."""
    return [doc for doc in DOCUMENTS if doc["category"] == category]


def get_documents_by_department(department: str):
    """Return documents filtered by department."""
    return [doc for doc in DOCUMENTS if doc["department"] == department]


if __name__ == "__main__":
    print(f"Total documents: {len(DOCUMENTS)}")
    print(f"Categories: {set(doc['category'] for doc in DOCUMENTS)}")
    print(f"Departments: {set(doc['department'] for doc in DOCUMENTS)}")
