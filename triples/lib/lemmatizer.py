
def simple_lemmatize(word: str) -> str:
    
    if not isinstance(word, str) or not word.strip():
        return ""

    word = word.lower().strip()

    # Very basic rules
    if word.endswith("ies") and len(word) > 3:
        return word[:-3] + "y"  # e.g., "stories" -> "story"
    elif word.endswith("ing") and len(word) > 4:
        return word[:-3]        # e.g., "running" -> "run"
    elif word.endswith("ed") and len(word) > 3:
        return word[:-2]        # e.g., "played" -> "play"
    elif word.endswith("s") and len(word) > 2:
        return word[:-1]        # e.g., "cats" -> "cat"
    return word


if __name__ == '__main__': 
     """
     
     """ 
     # Test the function
     words = ["stories", "running", "played", "cats", "better"]
     for w in words:
         print(f"{w} -> {simple_lemmatize(w)}")