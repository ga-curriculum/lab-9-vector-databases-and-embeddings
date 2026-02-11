# Lab 09: Building a Semantic Search System

**Duration:** 60 minutes  
**Format:** Hands-on Lab  
**Tools:** OpenAI API, ChromaDB, Python

---

## Overview

In this lab, you will build a complete semantic search system that:
1. Loads and chunks **real document data**
2. Generates embeddings using the **OpenAI API**
3. Stores vectors in **ChromaDB**
4. Performs **semantic search** queries
5. Compares results with **keyword search**

By the end, you'll have a working semantic search application that understands meaning, not just keywords.

---

## Learning Objectives

By the end of this lab, you will be able to:

1. Chunk documents for optimal embedding
2. Generate embeddings with the OpenAI API
3. Store and index documents in ChromaDB
4. Query using semantic search
5. Filter results with metadata
6. Compare semantic vs keyword search quality

---

## Scenario

You are building a **knowledge base search system** for RetailPulse's internal documentation. The current keyword search has problems:
- "How to boost sales" doesn't find "revenue optimization strategies"
- "Customer complaints" misses "handling negative feedback"
- Support team wastes time searching for documents

Your task: Build a semantic search system that understands meaning.

---

## Part 0: Environment Setup (5 minutes)

### Step 1: Install Dependencies

```bash
pip install openai chromadb pandas
```

### Step 2: Set Up API Key

```python
import os
os.environ["OPENAI_API_KEY"] = "your-api-key"
```

Or create a `.env` file:
```
OPENAI_API_KEY=your-api-key
```

### Step 3: Create Project Structure (i.e. clone this repository)

```bash
git clone https://git.generalassemb.ly/data-engineering-and-automation-with-ai/Lab-9-Vector-Databases-and-Embeddings.git
cd Lab-9-Vector-Databases-and-Embeddings/
```

### Step 4: Verify Setup

```python
from openai import OpenAI
import chromadb

client = OpenAI()
chroma = chromadb.Client()

# Test embedding
response = client.embeddings.create(
    model="text-embedding-3-small",
    input="Hello, world!"
)
print(f"Embedding dimensions: {len(response.data[0].embedding)}")
print("Setup complete!")
```

---

## Part 1: Prepare Document Data (10 minutes)

### Task 1.1: Create Sample Knowledge Base

Create a file `data/knowledge_base.py` with sample documents:

```python
"""
Sample knowledge base documents for RetailPulse.
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
```

### Task 1.2: Load and Explore Documents

```python
from data.knowledge_base import DOCUMENTS

print(f"Total documents: {len(DOCUMENTS)}")
print(f"\nCategories: {set(doc['category'] for doc in DOCUMENTS)}")
print(f"Departments: {set(doc['department'] for doc in DOCUMENTS)}")

# Preview first document
print(f"\nSample document:")
print(f"  Title: {DOCUMENTS[0]['title']}")
print(f"  Content: {DOCUMENTS[0]['content'][:100]}...")
```

---

## Part 2: Build the Vector Store (15 minutes)

### Task 2.1: Initialize ChromaDB

```python
import chromadb
from chromadb.utils import embedding_functions
import os

# Initialize ChromaDB with persistence
chroma_client = chromadb.PersistentClient(path="./chroma_db")

# Create OpenAI embedding function
openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=os.environ["OPENAI_API_KEY"],
    model_name="text-embedding-3-small"
)

# Create or get collection
collection = chroma_client.get_or_create_collection(
    name="knowledge_base",
    embedding_function=openai_ef,
    metadata={"description": "RetailPulse internal documentation"}
)

print(f"Collection created: {collection.name}")
print(f"Current document count: {collection.count()}")
```

### Task 2.2: Prepare Documents for Indexing

```python
from data.knowledge_base import DOCUMENTS

def prepare_documents(docs):
    """
    Prepare documents for ChromaDB.
    Combines title and content for better search.
    """
    documents = []
    metadatas = []
    ids = []
    
    for doc in docs:
        # Combine title and content for embedding
        text = f"{doc['title']}\n\n{doc['content']}"
        documents.append(text)
        
        # Store metadata for filtering
        metadatas.append({
            "title": doc["title"],
            "category": doc["category"],
            "department": doc["department"],
        })
        
        ids.append(doc["id"])
    
    return documents, metadatas, ids

documents, metadatas, ids = prepare_documents(DOCUMENTS)

print(f"Prepared {len(documents)} documents for indexing")
print(f"\nSample prepared document:")
print(documents[0][:200] + "...")
```

### Task 2.3: Index Documents

```python
# Clear existing documents (for re-runs)
if collection.count() > 0:
    collection.delete(ids=ids)

# Add documents to collection
collection.add(
    documents=documents,
    metadatas=metadatas,
    ids=ids
)

print(f"Indexed {collection.count()} documents")
```

---

## Part 3: Implement Semantic Search (15 minutes)

### Task 3.1: Basic Semantic Search

```python
def semantic_search(query: str, n_results: int = 3):
    """
    Perform semantic search on the knowledge base.
    """
    results = collection.query(
        query_texts=[query],
        n_results=n_results,
        include=["documents", "metadatas", "distances"]
    )
    
    return results

# Test search
query = "How can I boost our team's productivity?"
results = semantic_search(query)

print(f"Query: '{query}'")
print(f"\nTop {len(results['documents'][0])} results:")
for i, (doc, metadata, distance) in enumerate(zip(
    results['documents'][0], 
    results['metadatas'][0],
    results['distances'][0]
)):
    print(f"\n{i+1}. {metadata['title']}")
    print(f"   Category: {metadata['category']}")
    print(f"   Distance: {distance:.4f}")
    print(f"   Preview: {doc[:100]}...")
```

### Task 3.2: Search with Metadata Filtering

```python
def search_with_filter(query: str, category: str = None, department: str = None, n_results: int = 3):
    """
    Semantic search with optional metadata filters.
    """
    # Build filter
    where_filter = {}
    if category:
        where_filter["category"] = category
    if department:
        where_filter["department"] = department
    
    # Query with filter
    results = collection.query(
        query_texts=[query],
        n_results=n_results,
        where=where_filter if where_filter else None,
        include=["documents", "metadatas", "distances"]
    )
    
    return results

# Test: Search only in HR category
query = "employee evaluation process"
results = search_with_filter(query, category="hr")

print(f"Query: '{query}' (filtered by category='hr')")
print(f"\nResults:")
for i, (doc, metadata) in enumerate(zip(results['documents'][0], results['metadatas'][0])):
    print(f"  {i+1}. {metadata['title']} ({metadata['category']})")
```

### Task 3.3: Compare with Keyword Search

```python
def keyword_search(query: str, documents: list, n_results: int = 3):
    """
    Simple keyword search for comparison.
    """
    from data.knowledge_base import DOCUMENTS
    
    query_words = set(query.lower().split())
    
    # Score documents by keyword overlap
    scored_docs = []
    for doc in DOCUMENTS:
        text = f"{doc['title']} {doc['content']}".lower()
        text_words = set(text.split())
        
        # Count matching words
        matches = len(query_words.intersection(text_words))
        scored_docs.append((doc, matches))
    
    # Sort by score and return top N
    scored_docs.sort(key=lambda x: x[1], reverse=True)
    return scored_docs[:n_results]

# Compare search methods
test_queries = [
    "How to handle unhappy customers",  # Semantic: "complaints", "negative feedback"
    "boost revenue",  # Semantic: "sales", "increase"
    "working from home rules",  # Semantic: "remote work policy"
]

print("=" * 70)
print("COMPARISON: Keyword Search vs Semantic Search")
print("=" * 70)

for query in test_queries:
    print(f"\nQuery: '{query}'")
    
    # Keyword search
    keyword_results = keyword_search(query, DOCUMENTS)
    print(f"\n  Keyword Search:")
    for doc, score in keyword_results:
        print(f"    - {doc['title']} (matches: {score})")
    
    # Semantic search
    semantic_results = semantic_search(query)
    print(f"\n  Semantic Search:")
    for i, metadata in enumerate(semantic_results['metadatas'][0]):
        distance = semantic_results['distances'][0][i]
        print(f"    - {metadata['title']} (distance: {distance:.4f})")
```

---

## Part 4: Build Search Interface (10 minutes)

### Task 4.1: Create Search Function with Formatting

```python
def search_knowledge_base(query: str, category: str = None, n_results: int = 5):
    """
    User-friendly search function with formatted output.
    """
    # Build filter
    where_filter = {"category": category} if category else None
    
    # Search
    results = collection.query(
        query_texts=[query],
        n_results=n_results,
        where=where_filter,
        include=["documents", "metadatas", "distances"]
    )
    
    # Format output
    print(f"\n{'='*60}")
    print(f"Search Results for: '{query}'")
    if category:
        print(f"Filtered by category: {category}")
    print(f"{'='*60}")
    
    if not results['documents'][0]:
        print("\nNo results found.")
        return
    
    for i, (doc, metadata, distance) in enumerate(zip(
        results['documents'][0],
        results['metadatas'][0],
        results['distances'][0]
    )):
        # Convert distance to similarity percentage (approximate)
        similarity = max(0, (1 - distance) * 100)
        
        print(f"\n{i+1}. {metadata['title']}")
        print(f"   Category: {metadata['category']} | Department: {metadata['department']}")
        print(f"   Relevance: {similarity:.1f}%")
        print(f"   ---")
        # Show first 150 chars of content
        content_preview = doc.split('\n\n')[1][:150] if '\n\n' in doc else doc[:150]
        print(f"   {content_preview}...")

# Test the search interface
search_knowledge_base("how to deal with customer issues")
search_knowledge_base("team collaboration", category="management")
search_knowledge_base("data protection requirements")
```

### Task 4.2: Interactive Search Loop

```python
def interactive_search():
    """
    Interactive search interface.
    """
    print("\n" + "="*60)
    print("KNOWLEDGE BASE SEARCH")
    print("="*60)
    print("Commands: 'quit' to exit, 'category:X' to filter")
    print("Example: 'category:hr employee benefits'")
    
    while True:
        query = input("\nSearch: ").strip()
        
        if query.lower() == 'quit':
            print("Goodbye!")
            break
        
        if not query:
            continue
        
        # Check for category filter
        category = None
        if query.startswith("category:"):
            parts = query.split(" ", 1)
            category = parts[0].split(":")[1]
            query = parts[1] if len(parts) > 1 else ""
        
        if query:
            search_knowledge_base(query, category=category)

# Uncomment to run interactive mode
# interactive_search()
```

---

## Part 5: Evaluation and Analysis (5 minutes)

### Task 5.1: Test Edge Cases

```python
# Test queries that demonstrate semantic understanding
edge_cases = [
    # Synonym matching
    ("refund policy", "Should find 'Product Return Policy'"),
    
    # Concept matching
    ("make meetings more efficient", "Should find 'Team Productivity Tips'"),
    
    # Different phrasing
    ("keeping customer info safe", "Should find 'Data Privacy Guidelines'"),
    
    # Partial concept
    ("new hire training", "Should find 'Employee Onboarding Process'"),
]

print("Edge Case Testing")
print("="*60)

for query, expected in edge_cases:
    results = semantic_search(query, n_results=1)
    top_result = results['metadatas'][0][0]['title'] if results['metadatas'][0] else "No result"
    
    print(f"\nQuery: '{query}'")
    print(f"Expected: {expected}")
    print(f"Got: {top_result}")
    print(f"Distance: {results['distances'][0][0]:.4f}" if results['distances'][0] else "")
```

### Task 5.2: Measure Search Quality

```python
# Ground truth: queries with known relevant documents
test_cases = [
    {"query": "customer refund", "relevant_id": "doc_004"},
    {"query": "team efficiency", "relevant_id": "doc_005"},
    {"query": "protect user data", "relevant_id": "doc_006"},
    {"query": "loyalty rewards", "relevant_id": "doc_010"},
    {"query": "report software issues", "relevant_id": "doc_011"},
]

def evaluate_search(test_cases, k=3):
    """
    Evaluate search quality using recall@k.
    """
    hits = 0
    
    for case in test_cases:
        results = collection.query(
            query_texts=[case["query"]],
            n_results=k
        )
        
        # Check if relevant doc is in top k
        result_ids = results['ids'][0]
        if case["relevant_id"] in result_ids:
            hits += 1
            position = result_ids.index(case["relevant_id"]) + 1
            print(f"✓ '{case['query']}' → Found at position {position}")
        else:
            print(f"✗ '{case['query']}' → Not in top {k}")
    
    recall = hits / len(test_cases)
    print(f"\nRecall@{k}: {recall:.1%} ({hits}/{len(test_cases)})")
    return recall

evaluate_search(test_cases)
```

---

## Stretch Goals (Optional)

### Stretch 1: Add More Documents

Expand the knowledge base with your own documents:

```python
new_docs = [
    {
        "id": "doc_013",
        "title": "Your Document Title",
        "content": "Your document content...",
        "category": "your_category",
        "department": "your_department"
    },
]

# Add to collection
new_documents, new_metadatas, new_ids = prepare_documents(new_docs)
collection.add(documents=new_documents, metadatas=new_metadatas, ids=new_ids)
```

### Stretch 2: Visualize Embeddings

Use dimensionality reduction to visualize document clusters:

```python
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt

# Get all embeddings
all_data = collection.get(include=["embeddings", "metadatas"])
embeddings = all_data['embeddings']
categories = [m['category'] for m in all_data['metadatas']]

# Reduce to 2D
tsne = TSNE(n_components=2, random_state=42)
embeddings_2d = tsne.fit_transform(embeddings)

# Plot
plt.figure(figsize=(10, 8))
for cat in set(categories):
    mask = [c == cat for c in categories]
    plt.scatter(
        embeddings_2d[mask, 0], 
        embeddings_2d[mask, 1], 
        label=cat, 
        alpha=0.7
    )
plt.legend()
plt.title("Document Embeddings (t-SNE)")
plt.show()
```

### Stretch 3: Hybrid Search

Combine keyword and semantic search:

```python
def hybrid_search(query: str, n_results: int = 5):
    """
    Combine keyword and semantic search results.
    """
    # Get semantic results
    semantic = semantic_search(query, n_results=n_results)
    
    # Get keyword results
    keyword = keyword_search(query, DOCUMENTS, n_results=n_results)
    
    # Combine and deduplicate (simple RRF-style fusion)
    combined = {}
    
    for i, id in enumerate(semantic['ids'][0]):
        combined[id] = combined.get(id, 0) + (1 / (i + 1))
    
    for i, (doc, _) in enumerate(keyword):
        combined[doc['id']] = combined.get(doc['id'], 0) + (1 / (i + 1))
    
    # Sort by combined score
    ranked = sorted(combined.items(), key=lambda x: x[1], reverse=True)
    
    return ranked[:n_results]
```

---

## Submission Checklist

Before completing the lab, verify:

- [ ] ChromaDB collection created and populated
- [ ] Basic semantic search working
- [ ] Metadata filtering working
- [ ] Comparison with keyword search completed
- [ ] Edge cases tested
- [ ] Search quality evaluated

---

## Key Concepts Applied

| Concept | Where Applied |
|---------|---------------|
| Embeddings | OpenAI API generates vectors |
| Vector storage | ChromaDB stores and indexes |
| Similarity search | `collection.query()` |
| Metadata filtering | `where` parameter |
| Chunking | Combining title + content |
| Evaluation | Recall@k measurement |

---

## Cleanup

```python
# Delete the persistent database (optional)
import shutil
shutil.rmtree("./chroma_db", ignore_errors=True)
```
