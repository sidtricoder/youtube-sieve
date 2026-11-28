---
title: How TF-IDF and cosine similarity rank video metadata
type: research
status: distilled
created: 2026-11-22
updated: 2026-11-28
authors: [romirG]
tags: [similarity, ranking]
requirements: [FR-1, FR-2, FR-3, FR-5]
sources:
  - https://scikit-learn.org/stable/modules/feature_extraction.html#tfidf-term-weighting
  - src/youtube_sieve/domain/similarity.py
---

# How TF-IDF and cosine similarity rank video metadata

Suppose a seed and two candidates all contain “tutorial”, but only the seed and one candidate contain “soldering”. With three documents, scikit-learn's smoothed inverse document frequency gives “tutorial” a weight of 1 and “soldering” a weight of about 1.29. The formula is `idf = 1 + ln((1 + N) / (1 + df))`, where each document counts once toward a term's document frequency, however often it repeats the term.

## From words to a score

youtube-sieve case-folds text, preserves Unicode combining marks and drops short tokens and configured stop words. The English stop list is a tuning choice for multilingual metadata. A title occurrence contributes 3 to a term's count, a tag occurrence 2 and a description occurrence 1. The project multiplies `ln(1 + weighted count)` by IDF, so repeating a tag brings diminishing returns. Compute IDF once over the seed and its unique candidates so every comparison uses the same weights.

Cosine is the dot product divided by the product of the two vector lengths. After scaling both vectors to unit length, summing the products for shared terms gives the score. Identical nonempty vectors score 1, disjoint vectors score 0, and the project assigns 0 when tokenisation leaves either vector empty. Synonyms with no shared tokens also score 0.

## Relevance to youtube-sieve

For FR-1 through FR-3 this gives a reproducible lexical ranking. For FR-5 it gives a relevance order to consider when filling a playlist. A later scorer could combine cosine with a bounded same-category bonus using explicit weights. Report each contribution separately so a reviewer can see why an item moved. Apply hard constraints such as remaining playlist time independently of that score.

See [[decision-tfidf-similarity]] for the adopted defaults and the choice of a sparse implementation.

## Related
- [[decision-tfidf-similarity]]
- [[youtube-similarity-without-related-endpoint]]
- [[index]]
