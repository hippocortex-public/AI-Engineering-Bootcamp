from collections import Counter
from dataclasses import dataclass
from pathlib import Path


END_WORD = "</w>"


def word_to_symbols(word: str) -> tuple[str, ...]:
    """Represent a word as characters plus an end-of-word marker."""
    return tuple(word) + (END_WORD,)


def corpus_to_vocab(corpus: str) -> dict[tuple[str, ...], int]:
    """Convert raw corpus text to a frequency vocabulary."""
    counts = Counter(corpus.lower().split())
    return {word_to_symbols(word): freq for word, freq in counts.items()}


def get_pair_stats(vocab: dict[tuple[str, ...], int]) -> Counter:
    """Count adjacent symbol pairs weighted by word frequency."""
    pairs = Counter()
    for symbols, freq in vocab.items():
        for i in range(len(symbols) - 1):
            pairs[(symbols[i], symbols[i + 1])] += freq
    return pairs


def merge_pair_in_symbols(
    symbols: tuple[str, ...],
    pair: tuple[str, str],
    replacement: str,
) -> tuple[str, ...]:
    """Merge all non-overlapping occurrences of a pair in one symbol sequence."""
    result: list[str] = []
    i = 0
    while i < len(symbols):
        if i < len(symbols) - 1 and (symbols[i], symbols[i + 1]) == pair:
            result.append(replacement)
            i += 2
        else:
            result.append(symbols[i])
            i += 1
    return tuple(result)


def merge_vocab(
    vocab: dict[tuple[str, ...], int],
    pair: tuple[str, str],
) -> dict[tuple[str, ...], int]:
    replacement = "".join(pair)
    return {
        merge_pair_in_symbols(symbols, pair, replacement): freq
        for symbols, freq in vocab.items()
    }


@dataclass(frozen=True)
class BPETokenizer:
    merges: list[tuple[str, str]]

    def encode_word(self, word: str) -> list[str]:
        symbols = word_to_symbols(word.lower())
        for pair in self.merges:
            symbols = merge_pair_in_symbols(symbols, pair, "".join(pair))
        return [symbol for symbol in symbols if symbol != END_WORD]

    def encode(self, text: str) -> list[str]:
        tokens: list[str] = []
        for word in text.split():
            tokens.extend(self.encode_word(word))
        return tokens

    def decode(self, tokens: list[str]) -> str:
        # Pedagogical approximation: BPE without whitespace tokens cannot fully reconstruct spaces.
        return " ".join(tokens)


def train_bpe(corpus: str, num_merges: int = 20) -> BPETokenizer:
    if num_merges < 0:
        raise ValueError("num_merges cannot be negative")

    vocab = corpus_to_vocab(corpus)
    merges: list[tuple[str, str]] = []

    for _ in range(num_merges):
        stats = get_pair_stats(vocab)
        if not stats:
            break

        # Deterministic tie-break: frequency desc, then lexical order.
        best_pair, best_count = sorted(
            stats.items(),
            key=lambda item: (-item[1], item[0]),
        )[0]

        if best_count < 2:
            break

        merges.append(best_pair)
        vocab = merge_vocab(vocab, best_pair)

    return BPETokenizer(merges=merges)


def main() -> None:
    current_dir = Path(__file__).resolve().parent
    corpus_path = current_dir.parent / "assets" / "sample_corpus.txt"
    corpus = corpus_path.read_text(encoding="utf-8")

    tokenizer = train_bpe(corpus, num_merges=25)

    print("Learned merges:")
    for index, merge in enumerate(tokenizer.merges, start=1):
        print(f"{index:02d}. {merge} -> {''.join(merge)}")

    sample = "AI engineers build context windows"
    encoded = tokenizer.encode(sample)

    print("\nSample:")
    print(sample)
    print("\nEncoded tokens:")
    print(encoded)
    print("\nApproximate decoded form:")
    print(tokenizer.decode(encoded))


if __name__ == "__main__":
    main()
