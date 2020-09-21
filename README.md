README
======
This repository contains an information retrieval system for scientific literature search. The following state-of-the-art ranking algorithms can be used to rank the relevant articles:

1. Term Frequency
2. TF-IDF
3. Okapi BM25
4. Divergence from Randomness
5. Ranked Boolean Retrieval

## Folder Structure

```bash
├── bin  # Contains various scripts to setup the system
├── data # Dependencies
│   └── classifier # Section classifier dependencies
└── src
    ├── engine     # Implementation of the information retrieval system
    ├── evaluation # Helper scripts to evaluate our experiments
    ├── setup      # Helper scripts to setup the system
    ├── tests      # Test files
    └── webapp     # Flask files (Frontend)

```
