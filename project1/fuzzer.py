from fuzzingbook.GrammarFuzzer import EvenFasterGrammarFuzzer
from fuzzingbook.GeneratorGrammarFuzzer import GeneratorGrammarFuzzer
from fuzzingbook.GeneratorGrammarFuzzer import ProbabilisticGeneratorGrammarFuzzer
import grammar


class Fuzzer:
    def __init__(self):
        # This function must not be changed.
        self.grammar = grammar.grammar
        self.setup_fuzzer()
        self.fuzz_count = 0

    def setup_fuzzer(self):
        # This function may be changed.
        self.fuzzer = ProbabilisticGeneratorGrammarFuzzer(self.grammar)

    def fuzz_one_input(self) -> str:
        # This function should be implemented, but the signature may not change.
        return self.fuzzer.fuzz()


if __name__ == "__main__":
    fuzzer = Fuzzer()
    for i in range(5):
        print(fuzzer.fuzz_one_input())
