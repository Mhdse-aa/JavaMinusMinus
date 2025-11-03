from .nfa import NFA
from .token_nfas import (
    build_identifier_nfa, build_number_nfa, build_string_literal_nfa,
    build_char_literal_nfa, build_operator_nfas, build_delimiter_nfas,
    build_keyword_nfas, KEYWORDS
)
from typing import List, Dict, Tuple

IDENT_NFA = build_identifier_nfa()
NUMBER_NFA = build_number_nfa()
STRING_NFA = build_string_literal_nfa()
CHAR_NFA = build_char_literal_nfa()
OPERATOR_NFAS = build_operator_nfas()
DELIMITER_NFAS = build_delimiter_nfas()
KEYWORD_NFAS = build_keyword_nfas()

TOKEN_GROUPS = [
    ("STRING", STRING_NFA),
    ("CHAR", CHAR_NFA),
    ("NUMBER", NUMBER_NFA),
    ("IDENT", IDENT_NFA),
]
for op, nfa in OPERATOR_NFAS:
    TOKEN_GROUPS.append((f"OP_{op}", nfa))
for d, nfa in DELIMITER_NFAS:
    TOKEN_GROUPS.append((f"DELIM_{d}", nfa))
for kw, nfa in KEYWORD_NFAS:
    TOKEN_GROUPS.append((f"KW_{kw}", nfa))

def _pos_to_linecol(text: str, pos: int) -> Tuple[int,int]:
    line = text.count('\n', 0, pos) + 1
    last_n = text.rfind('\n', 0, pos)
    col = pos + 1 if last_n == -1 else pos - last_n
    return line, col

def tokenize(text: str) -> List[Dict]:
    tokens = []
    i = 0
    L = len(text)
    while i < L:
        ch = text[i]

        if ch.isspace():
            i += 1
            continue
        # line comment
        if text.startswith("//", i):
            j = text.find('\n', i)
            if j == -1: break
            i = j + 1
            continue
        # block comment
        if text.startswith("/*", i):
            j = text.find("*/", i+2)
            if j == -1:
                print(f"Unterminated block comment at pos {i}")
                break
            i = j + 2
            continue

        best_len = 0
        best_type = None
        best_lexeme = None

        # special literals
        if ch == '"':
            lm = STRING_NFA.longest_match_from(text, i)
            if lm > best_len:
                best_len = lm; best_type = "STRING"; best_lexeme = text[i:i+lm]
        if ch == "'":
            lm = CHAR_NFA.longest_match_from(text, i)
            if lm > best_len:
                best_len = lm; best_type = "CHAR"; best_lexeme = text[i:i+lm]

        # general NFAs
        for tlabel, nfa in TOKEN_GROUPS:
            lm = nfa.longest_match_from(text, i)
            if lm > best_len or (lm == best_len and lm>0 and tlabel.startswith("KW_")):
                best_len = lm
                best_type = tlabel
                best_lexeme = text[i:i+lm]

        if best_len == 0:
            line, col = _pos_to_linecol(text, i)
            print(f"[Lexer error] invalid token start at line {line}, col {col}: '{text[i]}'")
            i += 1
            continue

        # normalize type
        if best_type == "IDENT" and best_lexeme in KEYWORDS:
            token_type = "KW"
        elif best_type.startswith("KW_"):
            token_type = "KW"
        elif best_type.startswith("OP_"):
            token_type = "OP"
        elif best_type.startswith("DELIM_"):
            token_type = "DELIM"
        else:
            token_type = best_type

        line, col = _pos_to_linecol(text, i)
        tokens.append({
            "type": token_type,
            "lexeme": best_lexeme,
            "pos": i,
            "line": line,
            "col": col
        })
        i += best_len

    return tokens
