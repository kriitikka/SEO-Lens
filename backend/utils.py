import re

def clean_text(text: str) -> str:
    """Remove extra whitespace and special characters."""
    return re.sub(r'\s+', ' ', text).strip()

def count_keywords(text: str, keyword: str) -> int:
    """Count keyword occurrences (case-insensitive)."""
    return len(re.findall(keyword, text, re.IGNORECASE))

# Test
if __name__ == "__main__":
    print(clean_text("  Hello    world!  "))  # "Hello world!"
    print(count_keywords("Python is great. Python rocks!", "python"))  # 2