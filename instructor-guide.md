# Lab 09 Instructor Guide: Building a Semantic Search System

**Duration:** 60 minutes  
**Format:** Hands-on Lab

---

## Lab Overview

Students build a complete semantic search system using ChromaDB and OpenAI embeddings. They'll compare results with keyword search, demonstrating why semantic search matters for modern AI applications.

---

## Pre-Lab Checklist

### Requirements

- [ ] Python 3.8+
- [ ] OpenAI API key (with credits)
- [ ] Internet connection
- [ ] `pip install openai chromadb pandas`

### Common Setup Issues

| Issue | Solution |
|-------|----------|
| OpenAI API error | Verify API key is set correctly |
| ChromaDB import error | Ensure chromadb is installed: `pip install chromadb` |
| Rate limit errors | Add delays between API calls or reduce batch size |
| Persistence issues | Use `chromadb.Client()` (in-memory) instead of `PersistentClient` |

---

## Time Allocation

| Part | Duration | Focus |
|------|----------|-------|
| Part 0: Setup | 5 min | Environment, API key |
| Part 1: Prepare Data | 10 min | Load documents, understand structure |
| Part 2: Build Vector Store | 15 min | ChromaDB, indexing |
| Part 3: Semantic Search | 15 min | Queries, filtering, comparison |
| Part 4: Search Interface | 10 min | User-friendly output |
| Part 5: Evaluation | 5 min | Quality measurement |

---

## Part-by-Part Guidance

### Part 0: Setup (5 min)

**Key Points:**
- API key must be set before running any code
- ChromaDB runs in-memory by default (no external server)
- Test the embedding generation to verify setup

**If Students Have Issues:**
- No OpenAI key: They can pair with someone who has one
- Corporate firewall: May need to use a personal network/hotspot

---

### Part 1: Prepare Data (10 min)

**Key Points:**
- Documents combine title + content for richer embeddings
- Metadata enables filtering (category, department)
- IDs must be unique

**Teaching Moment:**
> "We combine title and content because the embedding captures the *overall meaning*. A title like 'Remote Work Policy' helps the embedding understand the topic."

---

### Part 2: Build Vector Store (15 min)

**Key Points:**
- `embedding_function` handles automatic embedding generation
- `add()` generates embeddings and indexes in one call
- ChromaDB uses HNSW indexing by default

**Discussion Prompt:**
> "What happens when we call `collection.add()`?"

*Answer: ChromaDB sends text to OpenAI, gets embeddings back, stores vectors, and builds the search index.*

**Common Mistakes:**
- Forgetting to set the embedding function
- Duplicate IDs causing errors
- Not clearing collection on re-runs

---

### Part 3: Semantic Search (15 min)

**Key Points:**
- `query_texts` automatically generates query embedding
- `distances` shows how close/far results are
- Metadata filtering narrows search scope

**Critical Teaching Moment:**
The keyword vs semantic comparison is the core insight of this lab.

> "Look at the query 'How to handle unhappy customers'. Keyword search finds nothing because the word 'unhappy' isn't in the documents. Semantic search finds 'Handling Customer Complaints' because it understands the *meaning*."

Walk through the comparison output slowly.

---

### Part 4: Search Interface (10 min)

**Key Points:**
- Formatting makes results readable
- Similarity percentage is approximate (derived from distance)
- Interactive mode shows real-world usage

**If Time is Short:**
Skip the interactive loop — students can explore after class.

---

### Part 5: Evaluation (5 min)

**Key Points:**
- Recall@k measures search quality
- Ground truth needed for evaluation
- 100% recall is ideal but not always achievable

**Discussion Prompt:**
> "We got 80% recall. What could cause the missed cases?"

*Possible answers: Embedding quality, document chunking, query ambiguity.*

---

## Common Student Questions

### Q: Why ChromaDB instead of Pinecone?
**A:** ChromaDB is easier for learning — no cloud setup, auto-embeddings, runs locally. Pinecone is better for production scale.

### Q: How many documents can ChromaDB handle?
**A:** Tens of thousands easily. Beyond 100K, consider Pinecone or Weaviate.

### Q: Why combine title and content?
**A:** The title provides context that helps the embedding. "Remote Work Policy" + content is better than content alone.

### Q: What's a good distance/similarity score?
**A:** Depends on the data. Generally, distance < 0.3 is very similar, < 0.5 is related, > 0.7 is probably not relevant.

### Q: How do embeddings handle typos?
**A:** Reasonably well for minor typos, but not perfectly. Production systems often add spell-check.

---

## Assessment Criteria

| Criterion | Points | Description |
|-----------|--------|-------------|
| Setup Complete | 10 | ChromaDB and OpenAI working |
| Documents Indexed | 20 | All 12 documents in collection |
| Basic Search | 25 | Semantic search returns results |
| Filtered Search | 15 | Metadata filtering works |
| Comparison Complete | 20 | Keyword vs semantic comparison |
| Evaluation Run | 10 | Recall@k measured |

**Total: 100 points**

---

## Wrap-Up Discussion (5 minutes)

After the lab, discuss:

1. **When would keyword search still be better?**
   - Expected: Exact matches (SKUs, names), when users know exact terms

2. **What surprised you about semantic search results?**
   - Expected: Finding synonyms, understanding concepts

3. **How would you improve this system for production?**
   - Expected: More documents, hybrid search, better chunking, caching

---

## Connection to Next Module

Set expectations:

> "Today you built *retrieval* — finding relevant documents. Next session, we'll combine this with *generation* — using an LLM to answer questions based on what we retrieve. That's RAG: Retrieval-Augmented Generation."

---

## Post-Lab Notes

- Students who finish early should try stretch goals
- Note any OpenAI rate limit issues for future planning
- Collect feedback on document examples (were they relatable?)

---

## Resources for Instructors

- [ChromaDB Documentation](https://docs.trychroma.com/)
- [OpenAI Embeddings Guide](https://platform.openai.com/docs/guides/embeddings)
- [Pinecone Learning Center](https://www.pinecone.io/learn/)
