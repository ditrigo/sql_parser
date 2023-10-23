def parse_string(s):
    if not s:
        return []
    res = []
    i = 0
    while i < len(s):
        if s[i] == "i" and s[i:i+3] == "if ":
            j = i + 3
            while j < len(s) and s[j] != ",":
                j += 1
            res.append(["if", s[i+3:j]])
            i = j + 2
        elif s[i] == "t" and s[i:i+5] == "then ":
            j = i + 5
            while j < len(s) and s[j] != ",":
                if s[j:j+4] == "else":
                    break
                elif s[j:j+3] == "if ":
                    parse_res, k = parse_string(s[j:])
                    res.append(["then", parse_res])
                    j += k
                else:
                    j += 1
            else:
                res.append(["then", s[i+5:j]])
                i = j + 2
        elif s[i] == "e" and s[i:i+5] == "else ":
            j = i + 5
            while j < len(s) and s[j] != ")":
                if s[j:j+3] == "if ":
                    parse_res, k = parse_string(s[j:])
                    res.append(["else", parse_res])
                    j += k
                else:
                    j += 1
            else:
                res.append(["else", s[i+5:j]])
                i = j + 2
        else:
            i += 1
    return res, i


s = "(if a+b>c, then (if d<e, then x, else y), else z)"
result = parse_string(s)
print(result)
