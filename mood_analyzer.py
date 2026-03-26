# mood_analyzer.py
"""
Rule based mood analyzer for short text snippets.

This class starts with very simple logic:
  - Preprocess the text
  - Look for positive and negative words
  - Compute a numeric score
  - Convert that score into a mood label
"""

import re
from typing import List, Dict, Tuple, Optional

from dataset import POSITIVE_WORDS, NEGATIVE_WORDS


class MoodAnalyzer:
    """
    A very simple, rule based mood classifier.
    """

    def __init__(
        self,
        positive_words: Optional[List[str]] = None,
        negative_words: Optional[List[str]] = None,
    ) -> None:
        # Use the default lists from dataset.py if none are provided.
        positive_words = positive_words if positive_words is not None else POSITIVE_WORDS
        negative_words = negative_words if negative_words is not None else NEGATIVE_WORDS

        # Store as sets for faster lookup.
        self.positive_words = set(w.lower() for w in positive_words)
        self.negative_words = set(w.lower() for w in negative_words)

        self._emoji_scores = {
            ":)": 1,
            ":-)": 1,
            "😂": 1,
            "😍": 2,
            "🤩": 2,
            ":(": -1,
            ":-(": -1,
            "🥲": -1,
            "💀": -1,
            "😭": -2,
            "😤": -1,
            "🙄": -1,
        }
        self._slang_scores = {
            "lowkey": 0,
            "highkey": 0,
            "lol": -1,
            "ugh": -1,
            "yay": 1,
            "meh": 0,
            "yikes": -1,
            "oof": -1,
        }

    # ---------------------------------------------------------------------
    # Preprocessing
    # ---------------------------------------------------------------------

    def preprocess(self, text: str) -> List[str]:
        """
        Convert raw text into a list of tokens the model can work with.

        TODO: Improve this method.

        Right now, it does the minimum:
          - Strips leading and trailing whitespace
          - Converts everything to lowercase
          - Splits on spaces

        Ideas to improve:
          - Remove punctuation
          - Handle simple emojis separately (":)", ":-(", "🥲", "😂")
          - Normalize repeated characters ("soooo" -> "soo")
        """
        cleaned = text.strip().lower()

        # Collapse long repeated letters to keep expressive spelling consistent.
        cleaned = re.sub(r"([a-z])\1{2,}", r"\1\1", cleaned)

        # Keep common emoticons and emojis as explicit tokens.
        token_pattern = r":-\)|:\)|:-\(|:\(|🥲|😂|💀|😍|🤩|😭|😤|🙄|[a-z0-9]+(?:'[a-z0-9]+)?"
        tokens = re.findall(token_pattern, cleaned)

        return tokens

    # ---------------------------------------------------------------------
    # Scoring logic
    # ---------------------------------------------------------------------

    def score_text(self, text: str) -> int:
        """
        Compute a numeric "mood score" for the given text.

        Positive words increase the score.
        Negative words decrease the score.

        TODO: You must choose AT LEAST ONE modeling improvement to implement.
        For example:
          - Handle simple negation such as "not happy" or "not bad"
          - Count how many times each word appears instead of just presence
          - Give some words higher weights than others (for example "hate" < "annoyed")
          - Treat emojis or slang (":)", "lol", "💀") as strong signals
        """
        tokens = self.preprocess(text)
        score = 0

        negation_words = {"not", "never", "no", "dont", "don't",
                          "won't", "wont", "isn't", "isnt", "didn't", "didnt",
                          "doesn't", "doesnt", "without"}

        # Words that carry stronger or weaker sentiment than the default ±1.
        word_weights = {
            # strong positives
            "love": 2, "amazing": 2, "fantastic": 2, "wonderful": 2,
            "thrilled": 2, "excellent": 2, "brilliant": 2, "perfect": 2,
            # mild positives
            "okay": 0.5, "fine": 0.5, "nice": 0.5, "cool": 0.5,
            # strong negatives
            "hate": -2, "terrible": -2, "awful": -2, "miserable": -2,
            "hopeless": -2, "worthless": -2, "devastated": -2, "terrified": -2,
            # mild negatives
            "annoyed": -0.5, "tired": -0.5, "boring": -0.5,
        }

        # Extra sentiment cues from emojis/emoticons and common slang.
        emoji_scores = self._emoji_scores
        slang_scores = self._slang_scores

        i = 0
        while i < len(tokens):
          token = tokens[i]

          # Treat "no cap" as a phrase-level positive slang signal.
          if i + 1 < len(tokens) and token == "no" and tokens[i + 1] == "cap":
            score += 1
            i += 2
            continue

          sentiment_value = 0

          if token in self.positive_words:
            sentiment_value = word_weights.get(token, 1)
          elif token in self.negative_words:
            sentiment_value = word_weights.get(token, -1)
          elif token in emoji_scores:
            sentiment_value = emoji_scores[token]
          elif token in slang_scores:
            sentiment_value = slang_scores[token]

          if sentiment_value != 0:
            # Look back up to 2 tokens for a negation word.
            negation_window = tokens[max(0, i - 2):i]
            if any(t in negation_words for t in negation_window):
              sentiment_value *= -1
            score += sentiment_value

          i += 1

        # Heuristic sarcasm rule: phrases like "love ... traffic" are
        # usually complaints, not positive sentiment.
        sarcasm_context = {"traffic", "stuck", "jam", "commute", "delay", "line"}
        for i, token in enumerate(tokens):
          if token not in {"love", "loving", "loved"}:
            continue

          window_end = min(len(tokens), i + 6)
          if any(t in sarcasm_context for t in tokens[i + 1:window_end]):
            score -= 4
            break

        return score

    # ---------------------------------------------------------------------
    # Label prediction
    # ---------------------------------------------------------------------

    def predict_label(self, text: str) -> str:
        """
        Turn the numeric score for a piece of text into a mood label.

        The default mapping is:
          - score > 0  -> "positive"
          - score < 0  -> "negative"
          - score == 0 -> "neutral"

        TODO: You can adjust this mapping if it makes sense for your model.
        For example:
          - Use different thresholds (for example score >= 2 to be "positive")
          - Add a "mixed" label for scores close to zero
        Just remember that whatever labels you return should match the labels
        you use in TRUE_LABELS in dataset.py if you care about accuracy.
        """
        score = self.score_text(text)

        tokens = self.preprocess(text)
        has_positive = any(
            token in self.positive_words or self._emoji_scores.get(token, 0) > 0
            for token in tokens
        )
        has_negative = any(
            token in self.negative_words or self._emoji_scores.get(token, 0) < 0
            for token in tokens
        )

        # Use a threshold of ±1.5 so weak mixed signals don't force a label.
        if score >= 1.5:
            return "positive"
        if score <= -1.5:
            return "negative"

        # Score is ambiguous — use word presence to distinguish mixed vs neutral.
        if has_positive and has_negative:
            return "mixed"
        if score > 0 and has_positive:
            return "positive"
        if score < 0 and has_negative:
            return "negative"
        return "neutral"

    # ---------------------------------------------------------------------
    # Explanations (optional but recommended)
    # ---------------------------------------------------------------------

    def explain(self, text: str) -> str:
        """
        Return a short string explaining WHY the model chose its label.

        TODO:
          - Look at the tokens and identify which ones counted as positive
            and which ones counted as negative.
          - Show the final score.
          - Return a short human readable explanation.

        Example explanation (your exact wording can be different):
          'Score = 2 (positive words: ["love", "great"]; negative words: [])'

        The current implementation is a placeholder so the code runs even
        before you implement it.
        """
        tokens = self.preprocess(text)

        positive_hits: List[str] = []
        negative_hits: List[str] = []
        score = 0

        for token in tokens:
            if token in self.positive_words:
                positive_hits.append(token)
                score += 1
            if token in self.negative_words:
                negative_hits.append(token)
                score -= 1

        return (
            f"Score = {score} "
            f"(positive: {positive_hits or '[]'}, "
            f"negative: {negative_hits or '[]'})"
        )
