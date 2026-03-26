"""
Shared data for the Mood Machine lab.

This file defines:
  - POSITIVE_WORDS: starter list of positive words
  - NEGATIVE_WORDS: starter list of negative words
  - SAMPLE_POSTS: short example posts for evaluation and training
  - TRUE_LABELS: human labels for each post in SAMPLE_POSTS
"""

# ---------------------------------------------------------------------
# Starter word lists
# ---------------------------------------------------------------------

POSITIVE_WORDS = [
    "happy",
    "great",
    "good",
    "love",
    "excited",
    "awesome",
    "fun",
    "chill",
    "relaxed",
    "amazing",
    # expanded
    "joy",
    "joyful",
    "fantastic",
    "wonderful",
    "thankful",
    "grateful",
    "blessed",
    "thrilled",
    "proud",
    "peaceful",
    "motivated",
    "hopeful",
    "cheerful",
    "delighted",
    "pleasant",
    "enjoy",
    "enjoyed",
    "enjoying",
    "glad",
    "smile",
    "laugh",
    "laughing",
    "win",
    "winning",
    "won",
    "perfect",
    "brilliant",
    "excellent",
    "nice",
    "cool",
    "sweet",
]

NEGATIVE_WORDS = [
    "sad",
    "bad",
    "terrible",
    "awful",
    "angry",
    "upset",
    "tired",
    "stressed",
    "hate",
    "boring",
    # expanded
    "miserable",
    "lonely",
    "anxious",
    "worried",
    "frustrated",
    "disappointed",
    "exhausted",
    "hopeless",
    "terrified",
    "scared",
    "depressed",
    "empty",
    "lost",
    "hurt",
    "pain",
    "cry",
    "crying",
    "cried",
    "dread",
    "dreading",
    "failed",
    "failure",
    "useless",
    "worthless",
    "annoyed",
    "irritated",
    "overwhelmed",
    "broken",
    "drained",
    "numb",
]

# ---------------------------------------------------------------------
# Starter labeled dataset
# ---------------------------------------------------------------------

# Short example posts written as if they were social media updates or messages.
SAMPLE_POSTS = [
    "I love this class so much",
    "Today was a terrible day",
    "Feeling tired but kind of hopeful",
    "This is fine",
    "So excited for the weekend",
    "I am not happy about this",
    "Lowkey proud of myself, no cap",
    "Highkey done with today :(",
    "I absolutely love getting stuck in traffic for 2 hours",
    "Got the job!!! 😂 but now I am terrified",
    "Had coffee, touched grass, still feel weirdly empty 🥲",
    "That movie was wild 💀 I can't tell if I loved it or hated it",
    "Not bad, not great, just existing :)",
    "Everyone forgot my birthday lol",
    # added examples
    "I can't believe how wonderful today turned out",
    "Feeling hopeless and completely drained",
    "Don't really know how I feel about this",
    "Ugh, another Monday. I hate this.",
    "So grateful for my friends, they really came through 😂",
    "Passed the exam but I don't even care anymore",
    "Everything is falling apart and I just feel numb",
    "Honestly not bad today, kind of peaceful",
    "I won but it doesn't feel worth it 🥲",
    "Finally done with that project, feeling great!",
]

# Human labels for each post above.
# Allowed labels in the starter:
#   - "positive"
#   - "negative"
#   - "neutral"
#   - "mixed"
TRUE_LABELS = [
    "positive",  # "I love this class so much"
    "negative",  # "Today was a terrible day"
    "mixed",     # "Feeling tired but kind of hopeful"
    "neutral",   # "This is fine"
    "positive",  # "So excited for the weekend"
    "negative",  # "I am not happy about this"
    "positive",  # "Lowkey proud of myself, no cap"
    "negative",  # "Highkey done with today :("
    "negative",  # "I absolutely love getting stuck in traffic for 2 hours" (sarcasm)
    "mixed",     # "Got the job!!! 😂 but now I am terrified"
    "mixed",     # "Had coffee, touched grass, still feel weirdly empty 🥲"
    "mixed",     # "That movie was wild 💀 I can't tell if I loved it or hated it"
    "neutral",   # "Not bad, not great, just existing :)"
    "negative",  # "Everyone forgot my birthday lol"
    "positive",  # "I can't believe how wonderful today turned out"
    "negative",  # "Feeling hopeless and completely drained"
    "neutral",   # "Don't really know how I feel about this"
    "negative",  # "Ugh, another Monday. I hate this."
    "positive",  # "So grateful for my friends, they really came through 😂"
    "mixed",     # "Passed the exam but I don't even care anymore"
    "negative",  # "Everything is falling apart and I just feel numb"
    "positive",  # "Honestly not bad today, kind of peaceful"
    "mixed",     # "I won but it doesn't feel worth it 🥲"
    "positive",  # "Finally done with that project, feeling great!"
]

# TODO: Add 5-10 more posts and labels.
#
# Requirements:
#   - For every new post you add to SAMPLE_POSTS, you must add one
#     matching label to TRUE_LABELS.
#   - SAMPLE_POSTS and TRUE_LABELS must always have the same length.
#   - Include a variety of language styles, such as:
#       * Slang ("lowkey", "highkey", "no cap")
#       * Emojis (":)", ":(", "🥲", "😂", "💀")
#       * Sarcasm ("I absolutely love getting stuck in traffic")
#       * Ambiguous or mixed feelings
#
# Tips:
#   - Try to create some examples that are hard to label even for you.
#   - Make a note of any examples that you and a friend might disagree on.
#     Those "edge cases" are interesting to inspect for both the rule based
#     and ML models.
#
# Example of how you might extend the lists:
#
# SAMPLE_POSTS.append("Lowkey stressed but kind of proud of myself")
# TRUE_LABELS.append("mixed")
#
# Remember to keep them aligned:
#   len(SAMPLE_POSTS) == len(TRUE_LABELS)
