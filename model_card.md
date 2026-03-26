# Model Card: Mood Machine

This repository contains two mood classification approaches for short text:

1. Rule-based model in mood_analyzer.py
2. ML model in ml_experiments.py (CountVectorizer + LogisticRegression)

## 1. Model Overview

Model type:
- This project uses and compares both a rule-based and an ML classifier.

Intended use:
- Classify short, informal text (social-style posts/messages) into one of four labels: positive, negative, neutral, mixed.
- Intended for learning and experimentation, not production mental-health or safety decisions.

How it works (brief):
- Rule-based: preprocess text into tokens, score sentiment cues, then map score to label.
- ML: learn token/word associations from SAMPLE_POSTS and TRUE_LABELS using bag-of-words features.

## 2. Data

Dataset description:
- The final dataset has 14 labeled examples in dataset.py.
- I expanded from the starter set by adding 8 new posts and labels.
- Added posts include slang, emojis/emoticons, sarcasm, and ambiguous/mixed phrasing.

How labeling was done:
- Labels were assigned manually based on overall tone and likely reader interpretation.
- Ambiguous posts were intentionally included and labeled mixed or neutral depending on balance.

Edge-case labels that are debatable:
- "Not bad, not great, just existing :)" labeled neutral.
- "Got the job!!! 😂 but now I am terrified" labeled mixed.
- "Had coffee, touched grass, still feel weirdly empty 🥲" labeled mixed.

Important dataset characteristics:
- Includes slang: lowkey, highkey, no cap, lol.
- Includes emojis/emoticons: :), :(, 🥲, 😂, 💀.
- Includes sarcasm: "I absolutely love getting stuck in traffic for 2 hours".
- Includes mixed-feeling posts with conflicting cues.

Known data issues:
- Very small dataset (14 items).
- No held-out test split; evaluation is on the same tiny label set.
- Limited dialect and cultural coverage.
- Label subjectivity is high on ambiguous examples.

## 3. Rule-Based Model Details

Preprocessing:
- Lowercases and trims text.
- Normalizes repeated letters (example: "soooo" -> "soo").
- Regex tokenization that keeps words plus target emojis/emoticons.

Scoring rules in mood_analyzer.py:
- Base lexicon scoring:
- Positive word -> +1
- Negative word -> -1
- Negation handling:
- If a sentiment token follows not/never/no, invert its sign.
- Emoji/emoticon scoring:
- Positive: :), :-), 😂 -> +1
- Negative: :(, :-(, 🥲, 💀 -> -1
- Slang scoring:
- "no cap" phrase -> +1
- "lol" -> -1
- "lowkey" and "highkey" currently neutral by themselves.
- Sarcasm heuristic:
- If love/loving/loved appears near words like traffic/stuck/commute/delay/line, apply -2 adjustment.

Label mapping:
- score > 0 -> positive
- score < 0 -> negative
- score == 0 and both positive+negative lexicon hits exist -> mixed
- otherwise -> neutral

Strengths:
- Transparent and easy to debug.
- Predictable on direct sentiment and hand-coded slang/emoji patterns.
- Improved substantially after adding emoji/slang and sarcasm rules.

Weaknesses:
- Depends heavily on hardcoded vocabulary.
- Mixed detection still underpowered when conflict comes from unknown words.
- Sarcasm handling is narrow and pattern-specific.

## 4. ML Model Details

Features:
- Bag-of-words representation via CountVectorizer.

Model:
- LogisticRegression trained on SAMPLE_POSTS and TRUE_LABELS.

Observed behavior:
- On this tiny in-sample evaluation, the model reached 1.00 accuracy.
- It learned patterns from the labels, including slang/emojis/sarcasm examples present in training.

Sensitivity to labels:
- Highly sensitive due to small data size.
- Changing even a few labels would strongly alter learned decision boundaries.

Strengths:
- Captured patterns that the earlier rule-based versions missed.
- Handled several mixed and sarcasm examples correctly once those examples existed in training data.

Weaknesses:
- 1.00 here is training-set performance, not evidence of real-world generalization.
- Can overfit spurious cues from tiny datasets.

## 5. Evaluation Summary

How evaluation was performed:
- Rule-based predictions were compared to TRUE_LABELS on SAMPLE_POSTS.
- ML model was trained and evaluated on the same SAMPLE_POSTS/TRUE_LABELS set.

Rule-based accuracy progression during development:
- Initial implementation: 0.36
- After emoji/slang logic: 0.57
- After sarcasm heuristic (love ... traffic): 0.64

ML accuracy:
- In-sample accuracy on the same dataset: 1.00

Examples the rule-based model got right:
- "I am not happy about this" -> negative (negation rule with sentiment word)
- "Lowkey proud of myself, no cap" -> positive (no cap slang phrase)
- "I absolutely love getting stuck in traffic for 2 hours" -> negative after sarcasm rule

Examples that repeatedly confuse the rule-based model:
- "Feeling tired but kind of hopeful" labeled mixed, often predicted negative because tired is in lexicon but hopeful is not.
- "Got the job!!! 😂 but now I am terrified" labeled mixed, often predicted positive because 😂 contributes positive and terrified is unknown.
- "Had coffee, touched grass, still feel weirdly empty 🥲" labeled mixed, often predicted negative because 🥲 is weighted negative.
- "That movie was wild 💀 I can't tell if I loved it or hated it" labeled mixed, often predicted negative because 💀 is negative and loved/hated variants are not robustly modeled in mixed logic.

## 6. Limitations

Specific, observed limitations:
- Lexicon coverage gap:
- "Feeling tired but kind of hopeful" -> hopeful is ignored, causing negative bias.
- Mixed-state compression:
- Posts with one known positive cue and one unknown negative cue collapse to positive or negative instead of mixed.
- Pattern-specific sarcasm:
- The sarcasm heuristic catches love...traffic but does not generalize to other sarcastic constructions.
- Small-data instability:
- With only 14 samples, both rule weights and ML behavior are fragile.
- Evaluation design limitation:
- ML result of 1.00 is on training data; no held-out split means generalization is unknown.

## 7. Ethical Considerations

Bias and scope:
- This model is optimized for short, English, internet-style text similar to the dataset.
- It may misinterpret users from language communities using different slang, dialect, emoji conventions, or cultural references.

Potential harms if misused:
- False negatives on distress-related text if phrasing is indirect or culturally specific.
- Overconfident sentiment interpretation for ambiguous human emotion.
- Privacy concerns if applied to personal messages without consent.

Appropriate use:
- Classroom exploration, prototyping, and model behavior analysis.
- Not suitable for high-stakes decisions about health, safety, hiring, discipline, or access to services.

## 8. Comparison and Improvement Ideas

Rule-based vs ML (current state):
- Rule-based is interpretable and controllable but misses nuance unless explicitly engineered.
- ML fit the provided labels much better on this dataset and corrected several prior rule failures.
- ML behavior is very label-sensitive because the training set is tiny and subjective.

Recommended next steps:
1. Add a held-out test set and report train/test accuracy separately.
2. Expand dataset diversity (dialects, age groups, writing styles, non-US slang).
3. Add more mixed examples and clearer annotation guidelines for ambiguous posts.
4. Replace CountVectorizer with TF-IDF and compare.
5. Improve rule-based mixed detection using cue pairs (for example, "but" contrasts).
6. Add confidence estimates and abstain behavior for uncertain inputs.
