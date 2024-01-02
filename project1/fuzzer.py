from typing import Any, Dict, List, Set, Union
from fuzzingbook.GrammarFuzzer import (
    DerivationTree,
    EvenFasterGrammarFuzzer,
    GrammarFuzzer,
    nonterminals,
)
from pprint import pprint
from fuzzingbook.Grammars import Grammar, trim_grammar, exp_string, opts
from fuzzingbook.GeneratorGrammarFuzzer import GeneratorGrammarFuzzer
from fuzzingbook.GeneratorGrammarFuzzer import (
    ProbabilisticGrammarCoverageFuzzer,
    ProbabilisticGeneratorGrammarFuzzer,
    ProbabilisticGrammarFuzzer,
    ProbabilisticGeneratorGrammarCoverageFuzzer,
)
from fuzzingbook.GeneratorGrammarFuzzer import exp_order, exp_post_expansion_function
from fuzzingbook.Grammars import Expansion
import grammar
from grammar import store
from time import time, sleep


class MyFuzzer(ProbabilisticGeneratorGrammarFuzzer):
    def __init__(
        self,
        grammar: Grammar,
        *,
        replacement_attempts: int = 10,
        precompute_costs=True,
        symbol_costs={},
        expansion_costs={},
        **kwargs,
    ):
        super(GeneratorGrammarFuzzer, self).__init__(
            grammar, replacement_attempts=replacement_attempts
        )
        super(ProbabilisticGrammarFuzzer, self).__init__(grammar, **kwargs)

        # super(GeneratorGrammarFuzzer, self).__init__(grammar, replacement_attempts)
        # super(ProbabilisticGrammarCoverageFuzzer, self).__init__(grammar, **kwargs)

        self._symbol_costs: Dict[str, Union[int, float]] = symbol_costs
        self._expansion_costs: Dict[Expansion, Union[int, float]] = expansion_costs

        if precompute_costs:
            self.precompute_costs()

        # Make sure we now call the caching methods
        self.symbol_cost = self.new_symbol_cost  # type: ignore
        self.expansion_cost = self.new_expansion_cost  # type: ignore

    def new_symbol_cost(self, symbol: str, seen: Set[str] = set()) -> Union[int, float]:
        # print("okay...")
        return self._symbol_costs[symbol]

    def new_expansion_cost(
        self, expansion: Expansion, seen: Set[str] = set()
    ) -> Union[int, float]:
        # print("okay...")
        expansion = exp_string(expansion)
        return self._expansion_costs[expansion]

    def precompute_costs(self) -> None:
        tic = time()
        for symbol in self.grammar:
            if symbol not in self._symbol_costs:
                self._symbol_costs[symbol] = self.symbol_cost(symbol)

            for expansion in self.grammar[symbol]:
                expansion = exp_string(expansion)
                if expansion not in self._expansion_costs:
                    self._expansion_costs[expansion] = self.expansion_cost(expansion)

        toc = time()

    def symbol_cost(self, symbol: str, seen: Set[str] = set()) -> Union[int, float]:
        if symbol not in self._symbol_costs:
            expansions = self.grammar[symbol]
            self._symbol_costs[symbol] = min(
                self.expansion_cost(e, seen | {symbol}) for e in expansions
            )
        return self._symbol_costs[symbol]

    def expansion_cost(
        self, expansion: Expansion, seen: Set[str] = set()
    ) -> Union[int, float]:
        expansion = exp_string(expansion)
        if expansion not in self._expansion_costs:
            symbols = nonterminals(expansion)
            if len(symbols) == 0:
                self._expansion_costs[expansion] = 1  # no symbol
            elif any(s in seen for s in symbols):
                self._expansion_costs[expansion] = float("inf")
            else:
                self._expansion_costs[expansion] = (
                    sum(self.symbol_cost(s, seen) for s in symbols) + 1
                )
        return self._expansion_costs[expansion]

    def expand_tree_once(self, tree: DerivationTree) -> DerivationTree:
        # Apply inherited method.  This also calls `expand_tree_once()` on all
        # subtrees.
        symbol, children = tree
        # print(f"expanding symbol: {symbol}...")
        new_tree: DerivationTree = GrammarFuzzer.expand_tree_once(self, tree)

        (symbol, children) = new_tree
        if all(
            [
                exp_post_expansion_function(expansion) is None
                for expansion in self.grammar[symbol]
            ]
        ):
            # No constraints for this symbol
            return new_tree

        if self.any_possible_expansions(tree):
            # Still expanding
            return new_tree

        return self.run_post_functions_locally(new_tree)

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
        self.grammar["<start>"] = [
            ("<phase-1>", opts(prob=1.0)),
            "<phase-2>",
            "<phase-3>",
        ]
        self.fuzzer = MyFuzzer(
            trim_grammar(self.grammar),
            # compute_costs=True
        )

    def fuzz_one_input(self) -> str:
        # This function should be implemented, but the signature may not change.
        if self.fuzz_count == 50:
            self.grammar["<start>"] = [
                ("<phase-1>", opts(prob=0.0)),
                ("<phase-2>", opts(prob=1.0)),
                ("<phase-3>", opts(prob=0.0)),
            ]
            self.fuzzer = MyFuzzer(
                trim_grammar(self.grammar),
                precompute_costs=False,
                symbol_costs=self.fuzzer._symbol_costs,
                expansion_costs=self.fuzzer._expansion_costs,
            )
        if self.fuzz_count == 100:
            self.grammar["<start>"] = [
                ("<phase-1>", opts(prob=0.05)),
                ("<phase-2>", opts(prob=0.05)),
                "<phase-3>",
            ]
            self.fuzzer = MyFuzzer(
                trim_grammar(self.grammar),
                precompute_costs=False,
                symbol_costs=self.fuzzer._symbol_costs,
                expansion_costs=self.fuzzer._expansion_costs,
            )

        self.fuzz_count += 1
        return self.fuzzer.fuzz()


if __name__ == "__main__":
    from time import time

    fuzz1 = Fuzzer()
    fuzz_count = 0
    time_diff = 0
    tic = time()
    while time_diff < 30 * 60:
        fuzz1.fuzz_one_input()
        fuzz_count += 1
        toc = time()
        time_diff = toc - tic
    print(fuzz_count)
