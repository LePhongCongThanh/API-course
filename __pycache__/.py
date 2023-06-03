def merge_strings(word1, word2):
    merged = ""
    length = max(len(word1), len(word2))
    
    for i in range(length):
        if i < len(word1):
            merged += word1[i]
        if i < len(word2):
            merged += word2[i]
    
    return merged