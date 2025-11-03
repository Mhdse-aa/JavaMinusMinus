from .nfa import NFA
from typing import List, Tuple

KEYWORDS = [
    "class","interface","extends","implements","public","private","protected","internal","static","void","abstract",
    "if","else","while","for","break","continue","return","new","this","import","true","false","null","boolean","int","char","String"
]

# -------- Identifier ----------
def build_identifier_nfa(start:int=0) -> NFA:
    # [a-zA-Z$_][a-zA-Z0-9$_]*
    nfa = NFA(states=set(), transitions={}, start=start, accepts=set())
    s0 = start; s1 = start+1
    nfa.states.update({s0,s1})
    letters = [chr(c) for c in range(ord('a'), ord('z')+1)] \
            + [chr(c) for c in range(ord('A'), ord('Z')+1)] \
            + ['_', '$']
    alnum = letters + [str(d) for d in range(10)]
    for ch in letters:
        nfa.add_transition(s0, ch, s1)
    for ch in alnum:
        nfa.add_transition(s1, ch, s1)
    nfa.accepts.add(s1)
    return nfa

# -------- Numbers ----------
def build_number_nfa(start:int=1000) -> NFA:

    nfa = NFA(states=set(), transitions={}, start=start, accepts=set())
    s0=start; s1=start+1; s2=start+2; s3=start+3
    nfa.states.update({s0,s1,s2,s3})
    digits = [str(d) for d in range(10)]
    nonzero = [str(d) for d in range(1,10)]

    nfa.add_transition(s0, '0', s3)

    for d in nonzero:
        nfa.add_transition(s0, d, s1)

    for d in digits:
        nfa.add_transition(s1, d, s1)
    nfa.add_transition(s1, '_', s2)
    
    for d in digits:
        nfa.add_transition(s2, d, s1)

    nfa.accepts.add(s1)
    nfa.accepts.add(s3)
    return nfa

# -------- String ----------
def build_string_literal_nfa(start:int=2000) -> NFA:
    nfa = NFA(states=set(), transitions={}, start=start, accepts=set())
    s0=start; s1=start+1; s_esc=start+2; s_end=start+3
    nfa.add_transition(s0, '"', s1)
    for ch_code in range(32,127):
        ch = chr(ch_code)
        if ch not in {'"', '\\'}:
            nfa.add_transition(s1, ch, s1)
    nfa.add_transition(s1, '\\', s_esc)
    for ch_code in range(32,127):
        nfa.add_transition(s_esc, chr(ch_code), s1)
    nfa.add_transition(s1, '"', s_end)
    nfa.accepts.add(s_end)
    return nfa

# -------- Char ----------
def build_char_literal_nfa(start:int=3000) -> NFA:
    nfa = NFA(states=set(), transitions={}, start=start, accepts=set())
    s0=start; s1=start+1; s_esc=start+2; s_char=start+3; s_end=start+4
    nfa.add_transition(s0, "'", s1)
    for ch_code in range(32,127):
        ch = chr(ch_code)
        if ch not in {"'", "\\"}:
            nfa.add_transition(s1, ch, s_char)
    nfa.add_transition(s1, "\\", s_esc)
    for ch_code in range(32,127):
        nfa.add_transition(s_esc, chr(ch_code), s_char)
    nfa.add_transition(s_char, "'", s_end)
    nfa.accepts.add(s_end)
    return nfa

# -------- Operators ----------
def build_operator_nfas(start:int=4000) -> List[Tuple[str,NFA]]:
    ops = [
        "**","==","!=","<=" ,">=", "&&","||",
        "+","-","*","/","%","<",">","!","=",
        ".length","."
    ]
    nfas = []
    cur = start
    for op in ops:
        nfa = NFA.from_string(op, start_state=cur)
        nfas.append((op, nfa))
        cur += len(op) + 2
    return nfas

# -------- Delimiters ----------
def build_delimiter_nfas(start:int=6000) -> List[Tuple[str,NFA]]:
    delims = [';', ',', '{', '}', '[', ']', '(', ')', '.']
    nfas = []
    cur = start
    for d in delims:
        nfa = NFA.from_string(d, start_state=cur)
        nfas.append((d, nfa))
        cur += 3
    return nfas

# -------- Keywords ----------
def build_keyword_nfas(start:int=8000) -> List[Tuple[str,NFA]]:
    nfas = []
    cur = start
    for kw in KEYWORDS:
        nfa = NFA.from_string(kw, start_state=cur)
        nfas.append((kw, nfa))
        cur += len(kw) + 2
    return nfas
