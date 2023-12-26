from typing import List
from fuzzingbook.GrammarFuzzer import (
    DerivationTree,
    EvenFasterGrammarFuzzer,
    GrammarFuzzer,
)
from fuzzingbook.Grammars import trim_grammar, opts
from fuzzingbook.GeneratorGrammarFuzzer import GeneratorGrammarFuzzer
from fuzzingbook.GeneratorGrammarFuzzer import ProbabilisticGeneratorGrammarFuzzer
from fuzzingbook.GeneratorGrammarFuzzer import exp_order, exp_post_expansion_function
import grammar
from grammar import store


class MyFuzzer(ProbabilisticGeneratorGrammarFuzzer):
    # def expand_tree_once(self, tree: DerivationTree) -> DerivationTree:
    #     # Apply inherited method.  This also calls `expand_tree_once()` on all
    #     # subtrees.
    #     symbol, children = tree
    #     print(f"expanding symbol: {symbol}...")
    #     new_tree: DerivationTree = GrammarFuzzer.expand_tree_once(self, tree)

    #     (symbol, children) = new_tree
    #     if all(
    #         [
    #             exp_post_expansion_function(expansion) is None
    #             for expansion in self.grammar[symbol]
    #         ]
    #     ):
    #         # No constraints for this symbol
    #         return new_tree

    #     if self.any_possible_expansions(tree):
    #         # Still expanding
    #         return new_tree

    #     return self.run_post_functions_locally(new_tree)

    def choose_tree_expansion(
        self, tree: DerivationTree, expandable_children: List[DerivationTree]
    ) -> int:
        """Return index of subtree in `expandable_children`
        to be selected for expansion. Defaults to random."""
        (symbol, tree_children) = tree
        assert isinstance(tree_children, list)

        if len(expandable_children) == 1:
            # No choice
            return GrammarFuzzer.choose_tree_expansion(self, tree, expandable_children)

        expansion = self.find_expansion(tree)
        given_order = exp_order(expansion)
        if given_order is None:
            # No order specified
            return GrammarFuzzer.choose_tree_expansion(self, tree, expandable_children)

        nonterminal_children = [c for c in tree_children if c[1] != []]
        assert len(nonterminal_children) == len(
            given_order
        ), "Order must have one element for each nonterminal"

        # Find expandable child with lowest ordering
        min_given_order = None
        j = 0
        for k, expandable_child in enumerate(expandable_children):
            while (
                j < len(nonterminal_children)
                and expandable_child != nonterminal_children[j]
            ):
                j += 1
            assert j < len(nonterminal_children), "Expandable child not found"
            if self.log:
                print(
                    "Expandable child #%d %s has order %d"
                    % (k, expandable_child[0], given_order[j])
                )

            if min_given_order is None or given_order[j] < given_order[min_given_order]:
                min_given_order = k

        assert min_given_order is not None

        if self.log:
            print(
                "Returning expandable child #%d %s"
                % (min_given_order, expandable_children[min_given_order][0])
            )

        return min_given_order

    def fuzz_tree(self) -> DerivationTree:
        while True:
            tree = GrammarFuzzer.fuzz_tree(self)
            return tree


class Fuzzer:
    def __init__(self):
        # This function must not be changed.
        self.grammar = grammar.grammar
        self.setup_fuzzer()
        self.fuzz_count = 0

    def setup_fuzzer(self):
        # This function may be changed.
        self.grammar["<start>"] = [("<phase-1>", opts(prob=1.0)), "<phase-2>"]
        self.fuzzer = MyFuzzer(trim_grammar(self.grammar))

    def fuzz_one_input(self) -> str:
        # This function should be implemented, but the signature may not change.
        if self.fuzz_count > 20:
            self.grammar["<start>"] = ["<phase-1>", "<phase-2>"]
            self.fuzzer = MyFuzzer(trim_grammar(self.grammar))

        self.fuzz_count += 1
        return self.fuzzer.fuzz()


if __name__ == "__main__":
    from pprint import pprint

    fuzzer = Fuzzer()
    another_one = True
    while another_one:
        print(fuzzer.fuzz_one_input())
        pprint(store.store)
        another_one = input("another one?") == ""
