---
title: TF-IDF and cosine similarity in pure Python for metadata ranking
type: decision
status: distilled
created: 2026-11-22
authors: [sidtricoder]
tags: [decision, similarity, ranking]
requirements: [FR-1, FR-2, FR-3, DC-3]
sources: [https://scikit-learn.org/stable/modules/feature_extraction.html#tfidf-term-weighting, https://en.wikipedia.org/wiki/Tf%E2%80%93idf]
---

# TF-IDF and cosine similarity in pure Python for metadata ranking

**Status:** accepted
**Issue / PR:** #21

## Context
The YouTube Data API has no related-videos or related-channels endpoint, so FR-1 to FR-3 must rank candidates by comparing metadata text: title, tags and description ([[youtube-api-methods]]). DC-3 asks for simple, transparent techniques. One request compares a seed against at most a few hundred candidates, and every reported score must be explainable to the user.

## Options considered
1. **scikit-learn's `TfidfVectorizer`.** Well tested, but it pulls in NumPy and SciPy, adds a large dependency to the server image for a few hundred short documents, and puts library code inside the pure domain layer ([[decision-package-layout]]).
2. **A small pure-Python implementation** over sparse dictionaries. About a hundred lines, no dependencies, easy to explain and test, and linear in the number of words.
3. **Embeddings from a language model.** Better semantic matching, but it needs a model or an external service, is harder to explain, and goes beyond the "simple techniques" DC-3 asks for.

## Decision
Option 2, in `youtube_sieve.domain.similarity`:

- **Tokens:** case-folded runs of letters, digits and combining marks, split on punctuation and underscores. Marks are kept because Python's `\w` drops them and would cut Hindi or other Indic words into pieces. A small English stop-word list and a two-character minimum remove noise; both are configurable.
- **Field weights:** title 3, tags 2, description 1, by default. Each field is cut to 1,000 characters first, so a long description cannot dominate or use unbounded memory.
- **Term weight:** log(1 + weighted count), which dampens repetition, so keyword stuffing in a title gains little.
- **Inverse document frequency:** the smoothed form used by scikit-learn, ln((1 + n) / (1 + df)) + 1, computed over the query and its candidates. Words shared by every candidate still count a little, but much less than rare words.
- **Comparison:** unit-length vectors compared by cosine similarity. Scores are clamped to [0, 1], sorted best first, and ties are ordered by id, so output never depends on input order.
- The query and repeated candidate ids are removed before scoring.

## Consequences
- Matching is lexical: "car" and "automobile" do not match. Tags and titles usually share vocabulary within a topic, so this is acceptable for now, and a different scorer can be added later behind the same interface.
- Non-text signals (same category, same language, duration), low-confidence flags and recommendation profiles build on these scores in later issues.
- All weights and limits are in `SimilarityConfig`, so tuning needs no code change.
- See [[tfidf-cosine-similarity]] for a worked IDF example and the interpretation of cosine scores.

## Related
- [[index]]
- [[decision-quota-budget-enforcement]]
- [[youtube-similarity-without-related-endpoint]]
