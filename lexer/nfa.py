from typing import Set, Dict, List

class NFA:
    def __init__(self, states: Set[int], transitions: Dict[int, Dict[str, List[int]]], start: int, accepts: Set[int]):
        self.states = set(states)
        self.transitions = {s:dict(m) for s,m in transitions.items()}
        self.start = start
        self.accepts = set(accepts)

    @classmethod
    def from_string(cls, s: str, start_state: int = 0):
        states = set(range(start_state, start_state + len(s) + 1))
        transitions = {}
        for i, ch in enumerate(s):
            transitions.setdefault(start_state + i, {}).setdefault(ch, []).append(start_state + i + 1)
        return cls(states, transitions, start_state, {start_state + len(s)})

    def add_transition(self, a: int, symbol: str, b: int):
        self.transitions.setdefault(a, {}).setdefault(symbol, []).append(b)
        self.states.add(a); self.states.add(b)

    def epsilon_closure(self, states: Set[int]) -> Set[int]:
        stack = list(states)
        closure = set(states)
        while stack:
            s = stack.pop()
            for ns in self.transitions.get(s, {}).get('', []):
                if ns not in closure:
                    closure.add(ns)
                    stack.append(ns)
        return closure

    def move(self, states: Set[int], symbol: str) -> Set[int]:
        res = set()
        for s in states:
            for ns in self.transitions.get(s, {}).get(symbol, []):
                res.add(ns)
        return res

    def longest_match_from(self, text: str, pos: int) -> int:
        cur = self.epsilon_closure({self.start})
        max_accept = 0
        
        if cur & self.accepts:
            max_accept = 0
        i = pos
        while i < len(text):
            ch = text[i]
            cur = self.epsilon_closure(self.move(cur, ch))
            if not cur:
                break
            if cur & self.accepts:
                max_accept = i - pos + 1
            i += 1
        return max_accept
