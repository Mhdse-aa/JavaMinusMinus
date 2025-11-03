import os
from lexer.tokenizer import tokenize

INPUT_PATH = os.path.join("input","sample.java")
OUTPUT_PATH = os.path.join("output","tokens_output.txt")

def ensure_dirs():
    os.makedirs("input", exist_ok=True)
    os.makedirs("output", exist_ok=True)

def load_input(path: str) -> str:
    if not os.path.exists(path):
        # create a small sample if not present
        sample = '''// sample JavaMinusMinus code
import my.pkg;
class Main extends BaseClass implements Runnable {
    public static void main(String[] args) {
        int x = 4_56;
        String s = "hello \\"world\\" \\n done";
        char c = '\\n';
        if (x >= 10 && x != 0) {
            x = x + 1;
        }
        // operators test
        boolean b = true || false && !false;
    }
}
'''
        with open(path, "w", encoding="utf-8") as f:
            f.write(sample)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def save_tokens(tokens, path: str):
    with open(path, "w", encoding="utf-8") as f:
        for t in tokens:
            f.write(f"{t['type']:6s}  '{t['lexeme']}'  line:{t['line']:3d} col:{t['col']:3d}\n")

def main():
    ensure_dirs()
    text = load_input(INPUT_PATH)
    tokens = tokenize(text)
    save_tokens(tokens, OUTPUT_PATH)
    print(f"Tokens saved to: {OUTPUT_PATH}")
    # also print a short sample
    for t in tokens:
        print(f"{t['type']:6s}  '{t['lexeme']}'  line:{t['line']:3d} col:{t['col']:3d}")

if __name__ == "__main__":
    main()
