# Implement your grammar here in the `grammar` variable.
# You may define additional functions, e.g. for generators.
# You may not import any other modules written by yourself.
# That is, your entire implementation must be in `grammar.py`
# and `fuzzer.py`.

import string
import random
from fuzzingbook.Grammars import opts


def get_random_string():
    alpha = list(string.ascii_letters)
    name_length = random.randint(5, 10)
    result = "".join(
        [alpha[random.randint(0, len(alpha) - 1)] for _ in range(name_length)]
    )
    return result


class Store:
    def __init__(self):
        self.store = {}
        self.query_processors = []

    def get_table_names(self):
        return set(self.store.keys())

    def set_table(self, table_name, table_info):
        self.store[table_name] = table_info

    def remove_table(self, table_name):
        assert table_name in self.store
        self.store.pop(table_name)

    def get_table(self, table_name):
        return self.store[table_name]

    def append_query_processor(self, query_processor):
        # print(f"append_query_processor: {query_processor}"
        self.query_processors.append(query_processor(self))
        return True

    def pop_query_processor(self):
        # print(f"pop_query_processor: {self.query_processors}")
        self.query_processors.pop()
        return True

    def get_query_processor(self):
        assert len(self.query_processors) > 0
        return self.query_processors[-1]


class QueryProcessor:
    def __init__(self, store: Store) -> None:
        self.store = store
        self.table_name = None

    def get_new_table_name(self):
        table_names = self.store.get_table_names()
        new_name = get_random_string()
        while new_name in table_names:
            new_name = get_random_string()

        self.store.set_table(new_name, {})
        self.table_name = new_name

        return new_name

    def get_new_column_name(self):
        assert self.table_name is not None
        current_table = self.store.get_table(self.table_name)

        new_name = get_random_string()

        while new_name in current_table.keys():
            new_name = get_random_string()

        current_table[new_name] = ""
        self.store.set_table(self.table_name, current_table)

        return new_name

    def get_table_name(self):
        result = random.choice(list(self.store.get_table_names()))
        self.table_name = result
        return self.table_name

    def get_column_name(self):
        assert self.table_name is not None
        current_table = self.store.get_table(self.table_name)
        return random.choice(list(current_table.keys()))

    def update_table_name(self, new_table_name):
        assert self.table_name is not None
        table_info = self.store.get_table(self.table_name)
        self.store.set_table(new_table_name, table_info)
        self.store.remove_table(self.table_name)
        self.table_name = new_table_name
        return True

    def update_column_name(self, column_name, new_column_name):
        assert self.table_name is not None
        current_table = self.store.get_table(self.table_name)
        current_table[new_column_name] = current_table[column_name]
        current_table.pop(column_name)
        self.store.set_table(self.table_name, current_table)
        return True

    def delete_column_name(self, table_name, column_name):
        assert self.table_name is not None
        current_table = self.store.get_table(self.table_name)
        current_table.pop(column_name)
        self.store.set_table(self.table_name, current_table)
        return True


class CreateTableProcessor:
    def __init__(self, store: Store) -> None:
        self.qp = QueryProcessor(store)

    def get_new_table_name(self):
        return self.qp.get_new_table_name()

    def get_new_column_name(self):
        return self.qp.get_new_column_name()

    def get_table_name(self):
        return self.qp.get_table_name()

    def get_column_name(self):
        return self.qp.get_column_name()


class SelectProcessor:
    def __init__(self, store: Store) -> None:
        self.qp = QueryProcessor(store)

    def get_table_name(self):
        # print(f"select_processor get_table_name...")
        return self.qp.get_table_name()

    def get_column_name(self):
        return self.qp.get_column_name()


class AlterTableProcessor:
    def __init__(self, store: Store) -> None:
        self.qp = QueryProcessor(store)

    def get_table_name(self):
        return self.qp.get_table_name()

    def get_new_table_name(self):
        return self.qp.get_new_table_name()

    def get_new_column_name(self):
        return self.qp.get_new_column_name()

    def get_column_name(self):
        return self.qp.get_column_name()

    def update_table_name(self, new_table_name):
        return self.qp.update_table_name(new_table_name)

    def update_column_name(self, column_name, new_column_name):
        return self.qp.update_column_name(column_name, new_column_name)

    def delete_column_name(self, table_name, column_name):
        return self.qp.delete_column_name(table_name, column_name)


store = Store()

create_table_stmt = {
    "<create-table-stmt>": [
        (
            "CREATE TABLE <new-table-name> <view-or-table>",
            opts(
                order=[1, 2],
            ),
        ),
        (
            "CREATE TEMP TABLE <new-table-name> <view-or-table>",
            opts(
                order=[1, 2],
            ),
        ),
        (
            "CREATE TEMPORARY TABLE <new-table-name> <view-or-table>",
            opts(
                order=[1, 2],
            ),
        ),
        # (
        #     "CREATE TABLE main.<new-table-name> <view-or-table>",
        #     opts(
        #         order=[1, 2],
        #     ),
        # ),
        # (
        #     "CREATE TEMP TABLE temp.<new-table-name> <view-or-table>",
        #     opts(
        #         order=[1, 2],
        #     ),
        # ),
        # (
        #     "CREATE TEMPORARY TABLE temp.<new-table-name> <view-or-table>",
        #     opts(
        #         order=[1, 2],
        #     ),
        # ),
        (
            "CREATE TABLE IF NOT EXISTS <new-table-name> <view-or-table>",
            opts(
                order=[1, 2],
            ),
        ),
        (
            "CREATE TEMP TABLE IF NOT EXISTS <new-table-name> <view-or-table>",
            opts(
                order=[1, 2],
            ),
        ),
        (
            "CREATE TEMPORARY TABLE IF NOT EXISTS <new-table-name> <view-or-table>",
            opts(
                order=[1, 2],
            ),
        ),
        # (
        #     "CREATE TABLE IF NOT EXISTS main.<new-table-name> <view-or-table>",
        #     opts(
        #         order=[1, 2],
        #     ),
        # ),
        # (
        #     "CREATE TEMP TABLE IF NOT EXISTS temp.<new-table-name> <view-or-table>",
        #     opts(
        #         order=[1, 2],
        #     ),
        # ),
        # (
        #     "CREATE TEMPORARY TABLE IF NOT EXISTS temp.<new-table-name> <view-or-table>",
        #     opts(
        #         order=[1, 2],
        #     ),
        # ),
    ],
    "<view-or-table>": [
        # "AS <select-stmt>",
        (
            "( <column-defs> <table-constraints-0> ) <table-options-0>",
            opts(order=[1, 2, 3]),
        ),
    ],
    "<column-defs>": ["<column-def>, <column-defs>", "<column-def>"],
    "<table-constraints-0>": [", <table-constraint> <table-constraints-0>", ""],
    "<table-options-0>": ["<table-options>", ""],
}

column_def = {
    "<column-def>": [
        "<new-column-name>",
        "<new-column-name> <type-name>",
        "<new-column-name> <column-constraints>",
        "<new-column-name> <type-name> <column-constraints>",
    ],
    "<column-constraints>": [
        "<column-constraint> <column-constraints>",
        "<column-constraint>",
    ],
}

type_name = {
    "<type-name>": [
        "<data-types>",
        "<data-types> ( <signed-number> )",
        "<data-types> ( <signed-number>, <signed-number> )",
    ],
    "<data-types>": ["<data-type> <data-types>", "<data-type>"],
    "<data-type>": [
        "TEXT",
        "NUMERIC",
        "INTEGER",
        "REAL",
        "BLOB",
    ],
}

column_constraint = {
    "<column-constraint>": [
        "CONSTRAINT <column-name> <column-constraint-base>",
        "<column-constraint-base>",
    ],
    "<column-constraint-base>": [
        "PRIMARY KEY <conflict-clause>",
        "PRIMARY KEY ASC <conflict-clause>",
        "PRIMARY KEY DESC <conflict-clause>",
        "PRIMARY KEY <conflict-clause> AUTOINCREMENT",
        "PRIMARY KEY ASC <conflict-clause> AUTOINCREMENT",
        "PRIMARY KEY DESC <conflict-clause> AUTOINCREMENT",
        "NOT NULL <conflict-clause>",
        "UNIQUE <conflict-clause>",
        "CHECK ( <expr> )",
        "DEFAULT ( <expr> )",
        "DEFAULT <literal-value>",
        "DEFAULT <signed-number>",
        "COLLATE <collation-name>",
        # "<foreign-key-clause>",
        "GENERATED ALWAYS AS ( <expr> )",
        "GENERATED ALWAYS AS ( <expr> ) STORED",
        "GENERATED ALWAYS AS ( <expr> ) VIRTUAL",
        "AS ( <expr> )",
        "AS ( <expr> ) STORED",
        "AS ( <expr> ) VIRTUAL",
    ],
}

conflict_clause = {
    "<conflict-clause>": [
        "",
        "ON CONFLICT ROLLBACK",
        "ON CONFLICT ABORT",
        "ON CONFLICT FAIL",
        "ON CONFLICT IGNORE",
        "ON CONFLICT REPLACE",
    ],
}

literal_value = {
    "<literal-value>": [
        "<numeric-literal>",
        "<string-literal>",
        "<blob-literal>",
        "NULL",
        "TRUE",
        "FALSE",
        "CURRENT_TIME",
        "CURRENT_DATE",
        "CURRENT_TIMESTAMP",
    ],
}

signed_number = {
    "<signed-number>": [
        "<numeric-literal>",
        "+ <numeric-literal>",
        "- <numeric-literal>",
    ],
}

foreign_key_clause = {
    "<foreign-key-clause>": [
        "REFERENCES <table-name> ( <column-names> ) <foreign-key-clause-base>",
        "REFERENCES <table-name> <foreign-key-clause-base>",
        "REFERENCES <table-name>",
    ],
    "<column-names>": ["<column-name>, <column-names>", "<column-name>"],
    "<foreign-key-clause-base>": [
        "<on-or-matchs-0>",
        "<on-or-matchs-0> DEFERABLE INITIALLY DEFERRED",
        "<on-or-matchs-0> DEFERABLE INITIALLY IMMEDIATE",
        "<on-or-matchs-0> DEFERABLE",
        "<on-or-matchs-0> NOT DEFERABLE INITIALLY DEFERRED",
        "<on-or-matchs-0> NOT DEFERABLE INITIALLY IMMEDIATE",
        "<on-or-matchs-0> NOT DEFERABLE",
    ],
    "<on-or-matchs-0>": ["", "<on-or-match>", "<on-or-match> <on-or-matchs-0>"],
    "<on-or-match>": [
        "ON DELETE SET NULL",
        "ON DELETE SET DEFAULT",
        "ON DELETE CASCADE",
        "ON DELETE RESTRICT",
        "ON DELETE NO ACTION",
        "ON UPDATE SET NULL",
        "ON UPDATE SET DEFAULT",
        "ON UPDATE CASCADE",
        "ON UPDATE RESTRICT",
        "ON UPDATE NO ACTION",
        "MATCH <name>",  # TODO: What name?
    ],
}

table_constraint = {
    "<table-constraint>": [
        "CONSTRAINT <table-name> <table-constraint-base>",
        "<table-constraint-base>",
    ],
    "<table-constraint-base>": [
        "PRIMARY KEY ( <indexed-columns> ) <conflict-clause>",
        "UNIQUE ( <indexed-columns> ) <conflict-clause>",
        "CHECK ( <expr> )",
        # "FOREIGN KEY ( <column-names> ) <foreign-key-clause>",
    ],
    "<indexed-columns>": ["<indexed-column>, <indexed-columns>", "<indexed-column>"],
    "<column-names>": ["<column-name>, <column-names>", "<column-name>"],
}

table_options = {
    "<table-options>": [
        "WIHTOUT ROWID",
        "STRICT",
        "WIHTOUT ROWID, <table-options>",
        "STRICT, <table-options>",
    ]
}

indexed_column = {
    "<indexed-column>": [
        "<column-name>",
        "<expr>",
        "<column-name> COLLATE <collation-name>",
        "<expr> COLLATE <collation-name>",
        "<column-name> ASC",
        "<expr> ASC",
        "<column-name> COLLATE <collation-name> ASC",
        "<expr> COLLATE <collation-name> ASC",
        "<column-name> DESC",
        "<expr> DESC",
        "<column-name> COLLATE <collation-name> DESC",
        "<expr> COLLATE <collation-name> DESC",
    ]
}

expr = {
    "<expr>": [
        "<literal-value>",
        "<bind-parameter>",  # TODO: what bind-parameter
        # "<schema-name>.<table-name>.<column-name>",
        "<table-name>.<column-name>",
        "<column-name>",
        "<unary-operator> <expr>",
        "<expr> <binary-operator> <expr>",
        "<function-name> ( <function-arguments> )"
        "<function-name> ( <function-arguments> ) <filter-clause>"
        "<function-name> ( <function-arguments> ) <over-clause>"
        "<function-name> ( <function-arguments> ) <filter-clause> <over-clause>"
        "( <exprs> )",
        "CAST ( <expr> AS <type-name>)",
        "<expr> COLLATE <collation-name>",
        "<expr> LIKE <expr>"
        "<expr> NOT LIKE <expr>"
        "<expr> LIKE <expr> ESCAPE <expr>"
        "<expr> NOT LIKE <expr> ESCAPE <expr>"
        "<expr> GLOB <expr>",
        "<expr> REGEXP <expr>",
        "<expr> MATCH <expr>",
        "<expr> NOT GLOB <expr>",
        "<expr> NOT REGEXP <expr>",
        "<expr> NOT MATCH <expr>",
        "<expr> ISNULL",
        "<expr> NOTNULL",
        "<expr> NOT NULL",
        "<expr> IS <expr>",
        "<expr> IS NOT <expr>",
        "<expr> IS DISTINCT FROM <expr>",
        "<expr> IS NOT DISTINCT FROM <expr>",
        "<expr> BETWEEN <expr> and <expr>",
        "<expr> NOT BETWEEN <expr> and <expr>",
        "<expr> IN ()",
        "<expr> NOT IN ()",
        "<expr> IN ( <select-stmt>)",
        "<expr> NOT IN ( <select-stmt> )",
        "<expr> IN ( <exprs> )",
        "<expr> NOT IN ( <exprs> )",
        # "<expr> IN <schema-name>.<table-name>",
        # "<expr> NOT IN <schema-name>.<table-name>",
        "<expr> IN <table-name>",
        "<expr> NOT IN <table-name>",
        # "<expr> IN <schema-name>.<table-function-name> ( <exprs> )",
        # "<expr> NOT IN <schema-name>.<table-function-name> ( <exprs> )",
        "<expr> IN <table-function-name> ( <exprs> )",
        "<expr> NOT IN <table-function-name> ( <exprs> )",
        "( <select-stmt> )",
        "EXISTS ( <select-stmt> )",
        "NOT EXISTS ( <select-stmt> )",
        "CASE <when-thens> END",
        "CASE <expr> <when-thens> END",
        "CASE <when-thens> ELSE <expr> END",
        "CASE <expr> <when-thens> ELSE <expr> END",
        "<raise-function>",
    ],
    "<exprs>": ["<expr>, <exprs>", "<expr>"],
    "<when-thens>": [
        "WHEN <expr> THEN <expr>",
        "WHEN <expr> THEN <expr> <when-thens>",
    ],
}

filter_clause = {"<filter-clause>": ["FILTER ( WHERE <expr> )"]}

function_arguments = {
    "<function-arguments>": [
        "",
        "*",
        "DISTINCT <exprs>",
        "<exprs>",
        "DISTINCT <exprs> ORDER BY <ordering-terms>",
        "<exprs> ORDER BY <ordering-terms>",
    ],
    "<ordering-terms>": [
        "<ordering-term>",
        "<ordering-term>, <ordering-terms>",
    ],
}

over_clause = {
    "<over-clause>": [
        "OVER <window-name>",
        "OVER ( )",
        "OVER ( <base-window-name> )",
        "OVER ( PARTITION BY <exprs> )",
        "OVER ( <base-window-name> PARTITION BY <exprs> )",
        "OVER ( ORDER BY <ordering-terms> )",
        "OVER ( <base-window-name> ORDER BY <ordering-terms> )",
        "OVER ( PARTITION BY <exprs> ORDER BY <ordering-terms> )",
        "OVER ( <base-window-name> PARTITION BY <exprs> ORDER BY <ordering-terms> )",
        "OVER ( <frame-spec> )",
        "OVER ( <base-window-name> <frame-spec> )",
        "OVER ( PARTITION BY <exprs> <frame-spec> )",
        "OVER ( <base-window-name> PARTITION BY <exprs> <frame-spec> )",
        "OVER ( ORDER BY <ordering-terms> <frame-spec> )",
        "OVER ( <base-window-name> ORDER BY <ordering-terms> <frame-spec> )",
        "OVER ( PARTITION BY <exprs> ORDER BY <ordering-terms> <frame-spec> )",
        "OVER ( <base-window-name> PARTITION BY <exprs> ORDER BY <ordering-terms> <frame-spec> )",
    ]
}

frame_spec = {
    "<frame-spec>": [
        "<range-row-group> BETWEEN <frame-spec-1> AND <frame-spec-2> <excludes>",
        "<range-row-group> UNBOUNDED PRECEDING <excludes>",
        "<range-row-group> <expr> PRECEDING <excludes>",
        "<range-row-group> CURRENT ROW <excludes>",
    ],
    "<frame-spec-1>": [
        "UNBOUNDED PRECEDING",
        "<expr> PRECEDING",
        "CURRENT ROW",
        "<expr> FOLLOWING",
    ],
    "<frame-spec-2>": [
        "<expr> PRECEDING",
        "CURRENT ROW",
        "<expr> FOLLOWING",
        "UNBOUNDED FOLLOWING",
    ],
    "<range-row-group>": [
        "RANGE",
        "ROWS",
        "GROUPS",
    ],
    "<excludes>": [
        "",
        "EXCLUDE NO OTHERS",
        "EXCLUDE CURRENT ROW",
        "EXCLUDE GROUP",
        "EXCLUDE TIES",
    ],
}

ordering_term = {
    "<ordering-term>": [
        "<expr>",
        "<expr> COLLATE <collation-name>",
        "<expr> NULLS FIRST",
        "<expr> COLLATE <collation-name> NULLS FIRST",
        "<expr> NULLS LAST",
        "<expr> COLLATE <collation-name> NULLS LAST",
        "<expr> ASC",
        "<expr> COLLATE <collation-name> ASC",
        "<expr> ASC NULLS FIRST",
        "<expr> COLLATE <collation-name> ASC NULLS FIRST",
        "<expr> ASC NULLS LAST",
        "<expr> COLLATE <collation-name> ASC NULLS LAST",
        "<expr> DESC",
        "<expr> COLLATE <collation-name> DESC",
        "<expr> DESC NULLS FIRST",
        "<expr> COLLATE <collation-name> DESC NULLS FIRST",
        "<expr> DESC NULLS LAST",
        "<expr> COLLATE <collation-name> DESC NULLS LAST",
    ]
}

raise_function = {
    "<raise-function>": [
        "RAISE ( IGNORE )",
        "RAISE ( ROLLBACK, <error-message> )",
        "RAISE ( ABORT, <error-message> )",
        "RAISE ( FAIL, <error-message> )",
    ]
}

select_stmt = {
    "<select-stmt>": [("<select-0> <select-cores> <select-1>", opts(order=[1, 2, 3]))],
    "<select-0>": [
        ("", opts(prob=1.0)),
        # "WITH",
        # "WITH RECURSIVE",
        # "WITH <common-table-expressions>",
        # "WITH RECURSIVE <common-table-expressions>",
    ],
    "<common-table-expressions>": [
        "<common-table-expression>, <common-table-expressions>",
        "<common-table-expression>",
    ],
    "<select-cores>": [
        ("<select-core>", opts(prob=1.0)),
        "<select-core> <compound-operator> <select-cores>",
    ],
    "<select-core>": [
        # "VALUES <values>",
        (
            "SELECT <result-columns> <from-0> <where-0> <groupby-0> <having-0> <window-0>",
            opts(order=[5, 1, 2, 3, 4, 6]),
        ),
        (
            "SELECT DISTINCT <result-columns> <from-0> <where-0> <groupby-0> <having-0> <window-0>",
            opts(order=[5, 1, 2, 3, 4, 6]),
        ),
        (
            "SELECT ALL <result-columns> <from-0> <where-0> <groupby-0> <having-0> <window-0>",
            opts(order=[5, 1, 2, 3, 4, 6]),
        ),
    ],
    "<from-0>": [
        # "",
        # "FROM <join-clause>",
        "FROM <table-or-subquerys>",
    ],
    "<where-0>": ["", "WHERE <expr>"],
    "<groupby-0>": [
        "",
        # "GROUP BY <exprs>"
    ],
    "<having-0>": [
        "",
        # "HAVING <expr>"
    ],
    "<window-0>": [
        "",
        # "WINDOW <window-defs>"
    ],
    "<window-defs>": [
        "<window-name> AS <window-defn>",
        "<window-name> AS <window-defn>, <window-defs>",
    ],
    "<table-or-subquerys>": [
        "<table-or-subquery>",
        # "<table-or-subquery>, <table-or-subquerys>",
    ],
    "<result-columns>": ["<result-column>, <result-columns>", "<result-column>"],
    "<values>": ["VALUES ( <exprs> ), <values>", "VALUES ( <exprs> )"],
    "<select-1>": [
        "",
        "ORDER BY <ordering-terms>",
        "LIMIT <expr>",
        "ORDER BY <ordering-terms> LIMIT <expr>",
        "LIMIT <expr> OFFSET <expr>",
        "ORDER BY <ordering-terms> LIMIT <expr> OFFSET <expr>",
        "LIMIT <expr> , <expr>",
        "ORDER BY <ordering-terms> LIMIT <expr> , <expr>",
    ],
    "<ordering-terms>": ["<ordering-term>", "<ordering-term>, <ordering-terms>"],
}

common_table_expression = {
    "<common-table-expression>": [
        "<table-name> AS ( <select-stmt> )",
        "<table-name> ( <column-names> ) AS ( <select-stmt> )",
        "<table-name> AS MATERIALIZED ( <select-stmt> )",
        "<table-name> ( <column-names> ) AS MATERIALIZED ( <select-stmt> )",
        "<table-name> AS NOT MATERIALIZED ( <select-stmt> )",
        "<table-name> ( <column-names> ) AS NOT MATERIALIZED ( <select-stmt> )",
    ]
}

compound_operator = {
    "<compound-operator>": ["UNION", "UNION ALL", "INTERSECT", "EXCEPT"]
}

join_clause = {
    "<join-clause>": [
        "<table-or-subquery> <join-clause-0>",
    ],
    "<join-clause-0>": [
        "",
        (
            "<join-operator> <table-or-subquery> <join-constraint> <join-clause-0>",
            opts(order=[1, 2, 3, 4]),
        ),
    ],
}

join_constraint = {"<join-constraint>": ["", "ON <expr>", "USING ( <column-names> )"]}

join_operator = {
    "<join-operator>": [
        " , ",
        "CROSS JOIN",
        "JOIN",
        "NATURAL JOIN",
        "LEFT JOIN",
        "NATURAL LEFT JOIN",
        "RIGHT JOIN",
        "NATURAL RIGHT JOIN",
        "FULL JOIN",
        "NATURAL FULL JOIN",
        "LEFT OUTER JOIN",
        "NATURAL LEFT OUTER JOIN",
        "RIGHT OUTER JOIN",
        "NATURAL RIGHT OUTER JOIN",
        "FULL OUTER JOIN",
        "NATURAL FULL OUTER JOIN",
        "INNER JOIN",
        "NATURAL INNER JOIN",
    ]
}

table_or_subquery = {
    "<table-or-subquery>": [
        "<table-name>",
        "<table-name> <table-alias>",
        "<table-name> AS <table-alias>",
        "<table-name> INDEXED BY <index-name>",
        "<table-name> <table-alias> INDEXED BY <index-name>",
        "<table-name> AS <table-alias> INDEXED BY <index-name>",
        "<table-name> NOT INDEXED",
        "<table-name> <table-alias> NOT INDEXED",
        "<table-name> AS <table-alias> NOT INDEXED",
        # "<schema-name>.<table-name>",
        # "<schema-name>.<table-name> <table-alias>",
        # "<schema-name>.<table-name> AS <table-alias>",
        # "<schema-name>.<table-name> INDEXED BY <index-name>",
        # "<schema-name>.<table-name> <table-alias> INDEXED BY <index-name>",
        # "<schema-name>.<table-name> AS <table-alias> INDEXED BY <index-name>",
        # "<schema-name>.<table-name> NOT INDEXED",
        # "<schema-name>.<table-name> <table-alias> NOT INDEXED",
        # "<schema-name>.<table-name> AS <table-alias> NOT INDEXED",
        # "<table-function-name> ( <exprs> )",
        # "<table-function-name> ( <exprs> ) <table-alias>",
        # "<table-function-name> ( <exprs> ) AS <table-alias>",
        # "<schema-name>.<table-function-name> ( <exprs> )",
        # "<schema-name>.<table-function-name> ( <exprs> ) <table-alias>",
        # "<schema-name>.<table-function-name> ( <exprs> ) AS <table-alias>",
        # "( <select-stmt> )",
        # "( <select-stmt> ) <table-alias>",
        # "( <select-stmt> ) AS <table-alias>",
        # "( <table-or-subquerys> )",
        # ("( <join-clause> )", opts(prob=0.0)),
    ]
}

result_column = {
    "<result-column>": [
        "*",
        "<table-name>.*",
        "<expr>",
        "<expr> <column-alias>",
        "<expr> AS <column-alias>",
    ],
}

window_defn = {
    "<window-defn>": [
        "()",
        "( <base-window-name> )",
        "( PARTITION BY <exprs>)",
        "( <base-window-name> PARTITION BY <exprs>)",
        "( ORDER BY <ordering-terms>)",
        "( <base-window-name> ORDER BY <ordering-terms>)",
        "( PARTITION BY <exprs> ORDERING BY <ordering-terms>)",
        "( <base-window-name> PARTITION BY <exprs> ORDERING BY <ordering-terms>)",
        "(<frame-spec>)",
        "( <base-window-name> <frame-spec>)",
        "( PARTITION BY <exprs> <frame-spec>)",
        "( <base-window-name> PARTITION BY <exprs> <frame-spec>)",
        "( ORDER BY <ordering-terms> <frame-spec>)",
        "( <base-window-name> ORDER BY <ordering-terms> <frame-spec>)",
        "( PARTITION BY <exprs> ORDERING BY <ordering-terms> <frame-spec>)",
        "( <base-window-name> PARTITION BY <exprs> ORDERING BY <ordering-terms> <frame-spec>)",
    ]
}

alter_table_stmt = {
    "<alter-table-stmt>": [
        (
            "ALTER TABLE <table-name> COLUMN <column-name> TO <new-column-name>",
            opts(
                order=[1, 2, 3],
                post=lambda table_name, column_name, new_column_name: store.get_query_processor().update_column_name(
                    column_name, new_column_name
                ),
            ),
        ),
        (
            "ALTER TABLE <table-name> RENAME TO <new-table-name>",
            opts(
                order=[1, 2],
                post=lambda table_name, new_table_name: store.get_query_processor().update_table_name(
                    new_table_name
                ),
            ),
        ),
        (
            "ALTER TABLE <table-name> <column-name> TO <new-column-name>",
            opts(
                order=[1, 2, 3],
                post=lambda _, column_name, new_column_name: store.get_query_processor().update_column_name(
                    column_name, new_column_name
                ),
            ),
        ),
        ("ALTER TABLE <table-name> ADD COLUMN <column-def>", opts(order=[1, 2])),
        ("ALTER TABLE <table-name> ADD <column-def>", opts(order=[1, 2])),
        (
            "ALTER TABLE <table-name> DROP COLUMN <column-name>",
            opts(
                order=[1, 2],
                prob=0.05,
                post=lambda table_name, column_name: store.get_query_processor().delete_column_name(
                    table_name, column_name
                ),
            ),
        ),
        (
            "ALTER TABLE <table-name> DROP <column-name>",
            opts(
                order=[1, 2],
                prob=0.05,
                post=lambda table_name, column_name: store.get_query_processor().delete_column_name(
                    table_name, column_name
                ),
            ),
        ),
        # "ALTER TABLE <schema-name>.<table-name> RENAME TO <new-table-name>",
        # "ALTER TABLE <schema-name>.<table-name> COLUMN <column-name> TO <new-column-name>",
        # "ALTER TABLE <schema-name>.<table-name> <column-name> TO <new-column-name>",
        # "ALTER TABLE <schema-name>.<table-name> ADD COLUMN <column-def>",
        # "ALTER TABLE <schema-name>.<table-name> ADD <column-def>",
        # "ALTER TABLE <schema-name>.<table-name> DROP COLUMN <column-name>",
        # "ALTER TABLE <schema-name>.<table-name> DROP <column-name>",
    ]
}


string_literal = {
    "<string-literal>": ["'<characters>'"],
    "<characters>": ["<character><characters>", "<character>"],
    "<character>": list(string.ascii_letters),
}


blob_literal = {
    "<blob-literal>": [
        "x'<hexdigits>'",
        "X'<hexdigits>'",
    ]
}

numeric_literal = {
    "<numeric-literal>": [
        "0x<hexdigits>",
        "0X<hexdigits>",
        ".<digits><exponent-0>",
        "<digits><exponent-0>",
        "<digits>.<digits><exponent-0>",
    ],
    "<digits>": ["<digit><digits>", "<digit>"],
    "<hexdigits>": ["<hexdigit><hexdigits>", "<hexdigit>"],
    "<exponent-0>": [
        "",
        "E<digits>",
        "E+<digits>",
        "E-<digits>",
        "e<digits>",
        "e+<digits>",
        "e-<digits>",
    ],
}


binary_operator = {
    "<binary-operator>": [
        "||",
        "->",
        "->>",
        "*",
        "/",
        "%",
        "+",
        "-",
        "&",
        "|",
        "<<",
        ">>",
        "<",
        ">",
        "<=",
        ">=",
        "=",
        "==",
        "!=",
    ],
}

unary_operator = {
    "<unary-operator>": ["~", "+", "-"],
}

digit = {"<digit>": list("0123456789")}

hexdigit = {"<hexdigit>": list("01234567890ABCDEF")}

misc = {
    "<table-name>": [
        ("<characters>", opts(pre=lambda: store.get_query_processor().get_table_name()))
    ],
    "<column-name>": [
        (
            "<characters>",
            opts(
                pre=lambda: store.get_query_processor().get_column_name(),
            ),
        )
    ],
    "<base-window-name>": ["<characters>"],
    "<new-table-name>": [
        (
            "<characters>",
            opts(pre=lambda: store.get_query_processor().get_new_table_name()),
        )
    ],
    # "<schema-name>": ["<characters>"],
    "<column-alias>": ["<characters>"],
    "<table-function-name>": ["<characters>"],
    "<window-name>": ["<characters>"],
    "<function-name>": ["<characters>"],
    "<index-name>": ["<characters>"],
    "<table-alias>": ["<characters>"],
    "<new-column-name>": [
        (
            "<characters>",
            opts(pre=lambda: store.get_query_processor().get_new_column_name()),
        )
    ],
    "<name>": ["<characters>"],
    "<error-message>": ["<characters>"],
    "<bind-parameter>": ["<characters>"],
    "<collation-name>": ["<characters>"],
    "<view-name>": ["<characters>"],
    "<index-name>": ["<characters>"],
}

create_view_stmt = {
    "<create-view-stmt>": [
        "CREATE VIEW <view-name> AS <select-stmt>",
        "CREATE VIEW IF NOT EXISTS <view-name> AS <select-stmt>",
        # "CREATE VIEW <view-name> ( <column-names> ) AS <select-stmt>",
        # "CREATE VIEW IF NOT EXISTS <view-name> ( <column-names> ) AS <select-stmt>",
    ]
}

create_index_stmt = {
    "<create-index-stmt>": [
        "CREATE INDEX <index-name> ON <table-name> ( <indexed-column> )",
        "CREATE UNIQUE INDEX <index-name> ON <table-name> ( <indexed-column> )",
        "CREATE INDEX IF NOT EXISTS <index-name> ON <table-name> ( <indexed-column> )",
        "CREATE UNIQUE INDEX IF NOT EXISTS <index-name> ON <table-name> ( <indexed-column> )",
        # "CREATE INDEX <index-name> ON <table-name> ( <indexed-column> ) WHERE <expr>",
        # "CREATE UNIQUE INDEX <index-name> ON <table-name> ( <indexed-column> ) WHERE <expr>",
        # "CREATE INDEX IF NOT EXISTS <index-name> ON <table-name> ( <indexed-column> ) WHERE <expr>",
        # "CREATE UNIQUE INDEX IF NOT EXISTS <index-name> ON <table-name> ( <indexed-column> ) WHERE <expr>",
    ]
}

begin_stmt = {
    "<begin-stmt>": [
        "BEGIN",
        "BEGIN DEFERRED",
        "BEGIN IMMEDIATE",
        "BEGIN EXCLUSIVE",
        "BEGIN TRANSACTION",
        "BEGIN DEFERRED TRANSACTION",
        "BEGIN IMMEDIATE TRANSACTION",
        "BEGIN EXCLUSIVE TRANSACTION",
    ]
}

commit_stmt = {
    "<commit-stmt>": [
        "COMMIT",
        "END",
        "COMMIT TRANSACTION",
        "END TRANSACTION",
    ]
}

rollback_stmt = {
    "<rollback-stmt>": [
        "ROLLBACK",
        "ROLLBACK TRANSACTION",
        "ROLLBACK TO <savepoint-name>",
        "ROLLBACK TRANSACTION TO <savepoint-name>",
        "ROLLBACK TO SAVEPOINT <savepoint-name>",
        "ROLLBACK TRANSACTION TO SAVEPOINT <savepoint-name>",
    ]
}


grammar = {
    "<start>": [("<phase-1>", opts(prob=1.0)), "<phase-2>"],
    "<phase-1>": [
        (
            "<create-table-stmt>",
            opts(
                pre=lambda: store.append_query_processor(CreateTableProcessor),
                post=lambda _: store.pop_query_processor(),
            ),
            "<create-view-stmt>",
            opts(
                pre=lambda: store.append_query_processor(
                    CreateTableProcessor
                ),  # TODO: CreateViewProcessor
                post=lambda _: store.pop_query_processor(),
            ),
            "<create-index-stmt>",
            opts(
                pre=lambda: store.append_query_processor(
                    CreateTableProcessor
                ),  # TODO: CreateIndexProcessor
                post=lambda _: store.pop_query_processor(),
            ),
        ),
    ],
    "<phase-2>": [
        (
            "<select-stmt>",
            opts(
                pre=lambda: store.append_query_processor(SelectProcessor),
                post=lambda _: store.pop_query_processor(),
            ),
        ),
        (
            "<alter-table-stmt>",
            opts(
                pre=lambda: store.append_query_processor(AlterTableProcessor),
                post=lambda _: store.pop_query_processor(),
                prob=1.0,
            ),
        ),
        "<begin-stmt>",
        "<commit-stmt>",
        "<rollback-stmt>",
    ],
    **alter_table_stmt,
    **begin_stmt,
    **binary_operator,
    **blob_literal,
    **column_constraint,
    **column_def,
    **commit_stmt,
    **common_table_expression,
    **compound_operator,
    **conflict_clause,
    **create_index_stmt,
    **create_table_stmt,
    **create_view_stmt,
    **digit,
    **expr,
    **filter_clause,
    **foreign_key_clause,
    **frame_spec,
    **function_arguments,
    **hexdigit,
    **indexed_column,
    **join_clause,
    **join_constraint,
    **join_operator,
    **literal_value,
    **misc,
    **numeric_literal,
    **ordering_term,
    **over_clause,
    **raise_function,
    **result_column,
    **rollback_stmt,
    **select_stmt,
    **signed_number,
    **string_literal,
    **table_constraint,
    **table_options,
    **table_or_subquery,
    **type_name,
    **unary_operator,
    **window_defn,
}
