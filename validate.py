import re

re.findall(r"[aeiou]", "hello world")    # every vowel
re.findall(r"[a-z]", "Hi There")         # lowercase letters only
re.findall(r"[A-Za-z0-9]", "abc_123!")   # letters+digits, no _ or !
re.findall(r"[^0-9]", "abc123")          # ^ inside [] means NOT — non-digits