def parse_string(s):

    res = []
    i = 0
    while i < len(s):
        if s[i] == "i" and s[i:i+3] == "if ":
            j = i + 3