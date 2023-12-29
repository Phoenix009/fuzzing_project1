# Implement your grammar here in the `grammar` variable.
# You may define additional functions, e.g. for generators.
# You may not import any other modules written by yourself.
# That is, your entire implementation must be in `grammar.py`
# and `fuzzer.py`.

import string
import random
from fuzzingbook.Grammars import opts


KEYWORDS = [
    "ABORT",
    "ACTION",
    "ADD",
    "AFTER",
    "ALL",
    "ALTER",
    "ALWAYS",
    "ANALYZE",
    "AND",
    "AS",
    "ASC",
    "ATTACH",
    "AUTOINCREMENT",
    "BEFORE",
    "BEGIN",
    "BETWEEN",
    "BY",
    "CASCADE",
    "CASE",
    "CAST",
    "CHECK",
    "COLLATE",
    "COLUMN",
    "COMMIT",
    "CONFLICT",
    "CONSTRAINT",
    "CREATE",
    "CROSS",
    "CURRENT",
    "CURRENT_DATE",
    "CURRENT_TIME",
    "CURRENT_TIMESTAMP",
    "DATABASE",
    "DEFAULT",
    "DEFERRABLE",
    "DEFERRED",
    "DELETE",
    "DESC",
    "DETACH",
    "DISTINCT",
    "DO",
    "DROP",
    "EACH",
    "ELSE",
    "END",
    "ESCAPE",
    "EXCEPT",
    "EXCLUDE",
    "EXCLUSIVE",
    "EXISTS",
    "EXPLAIN",
    "FAIL",
    "FILTER",
    "FIRST",
    "FOLLOWING",
    "FOR",
    "FOREIGN",
    "FROM",
    "FULL",
    "GENERATED",
    "GLOB",
    "GROUP",
    "GROUPS",
    "HAVING",
    "IF",
    "IGNORE",
    "IMMEDIATE",
    "IN",
    "INDEX",
    "INDEXED",
    "INITIALLY",
    "INNER",
    "INSERT",
    "INSTEAD",
    "INTERSECT",
    "INTO",
    "IS",
    "ISNULL",
    "JOIN",
    "KEY",
    "LAST",
    "LEFT",
    "LIKE",
    "LIMIT",
    "MATCH",
    "MATERIALIZED",
    "NATURAL",
    "NO",
    "NOT",
    "NOTHING",
    "NOTNULL",
    "NULL",
    "NULLS",
    "OF",
    "OFFSET",
    "ON",
    "OR",
    "ORDER",
    "OTHERS",
    "OUTER",
    "OVER",
    "PARTITION",
    "PLAN",
    "PRAGMA",
    "PRECEDING",
    "PRIMARY",
    "QUERY",
    "RAISE",
    "RANGE",
    "RECURSIVE",
    "REFERENCES",
    "REGEXP",
    "REINDEX",
    "RELEASE",
    "RENAME",
    "REPLACE",
    "RESTRICT",
    "RETURNING",
    "RIGHT",
    "ROLLBACK",
    "ROW",
    "ROWS",
    "SAVEPOINT",
    "SELECT",
    "SET",
    "TABLE",
    "TEMP",
    "TEMPORARY",
    "THEN",
    "TIES",
    "TO",
    "TRANSACTION",
    "TRIGGER",
    "UNBOUNDED",
    "UNION",
    "UNIQUE",
    "UPDATE",
    "USING",
    "VACUUM",
    "VALUES",
    "VIEW",
    "VIRTUAL",
    "WHEN",
    "WHERE",
    "WINDOW",
    "WITH",
    "WITHOUT",
]


def get_random_string():
    alpha = list(string.ascii_letters)
    name_length = random.randint(5, 10)
    result = "".join(
        [alpha[random.randint(0, len(alpha) - 1)] for _ in range(name_length)]
    )
    return result


def get_random_name():
    new_name = get_random_string()
    while new_name.upper() in KEYWORDS:
        new_name = get_random_string()
    return new_name


class Store:
    def __init__(self):
        self.store = {}
        self.query_processors = []

    def get_table_names(self):
        return set(self.store.keys())

    def set_table(self, table_name, table_info):
        # print(f"setting table: {table_name}")
        self.store[table_name] = table_info

    def remove_table(self, table_name):
        # print(f"removing table: {table_name}")
        assert table_name in self.store
        self.store.pop(table_name)

    def get_table(self, table_name):
        # print(f"getting table_info for: {table_name}")
        return self.store[table_name]

    def append_query_processor(self, query_processor):
        # print(f"append_query_processor: {query_processor}")
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
        self.store: Store = store
        self.table_name = None

    def is_keyword(name: str):
        return name.upper() in KEYWORDS

    def get_new_table_name(self):
        init_empty_table = lambda: {
            "has_primary_key": False,
            "columns": set(),
            "indices": set(),
        }

        table_names = self.store.get_table_names()
        new_name = get_random_string()
        while new_name in table_names:
            new_name = get_random_string()

        self.store.set_table(new_name, init_empty_table())
        self.table_name = new_name

        return new_name

    def get_new_column_name(self):
        assert self.table_name is not None
        current_table = self.store.get_table(self.table_name)

        new_name = get_random_string()

        while new_name in current_table["columns"]:
            new_name = get_random_string()

        current_table["columns"].add(new_name)
        self.store.set_table(self.table_name, current_table)

        return new_name

    def get_table_name(self):
        result = random.choice(list(self.store.get_table_names()))
        self.table_name = result
        return self.table_name

    def get_column_name(self):
        assert self.table_name is not None
        current_table = self.store.get_table(self.table_name)
        return random.choice(list(current_table["columns"]))

    def update_table_name(self, table_name, new_table_name):
        # print(f"query_processor: update_table_name to {new_table_name}")
        table_info = self.store.get_table(table_name)
        self.store.set_table(new_table_name, table_info)
        self.store.remove_table(table_name)
        self.table_name = new_table_name
        return True

    def update_column_name(self, column_name, new_column_name):
        assert self.table_name is not None
        current_table = self.store.get_table(self.table_name)
        current_table["columns"].add(new_column_name)
        current_table["columns"].remove(column_name)
        self.store.set_table(self.table_name, current_table)
        return True

    def delete_column_name(self, table_name, column_name):
        assert self.table_name is not None
        current_table = self.store.get_table(self.table_name)
        current_table["columns"].remove(column_name)
        self.store.set_table(self.table_name, current_table)
        return True

    def set_primary_key(self, columns):
        # print(f"set_primary_key table: {self.table_name}: {columns}")
        current_table = self.store.get_table(self.table_name)
        if current_table["has_primary_key"]:
            # print(f"set_primary_key table: {self.table_name} already has one...")
            return "CHECK(1)"
        current_table["has_primary_key"] = True
        self.store.set_table(self.table_name, current_table)
        return True

    def mark_table_temporary(self, table_name):
        self.update_table_name(table_name, f"temp.{table_name}")
        return True

    def create_index(self, table_name, index_name):
        assert table_name == self.table_name
        # print(f"create_index: table_name: {table_name}, index_name: {index_name}")
        current_table = self.store.get_table(table_name)
        current_table["indices"].add(index_name)
        self.store.set_table(table_name, current_table)
        return True

    def get_index(self, table_name):
        table_with_indices = dict(
            filter(
                lambda item: item[1]["indices"],
                self.store.store.items(),
            )
        )
        table_name = random.choice(list(table_with_indices.keys()))
        # print(table_with_indices[table_name])
        self.table_name = table_name
        index_name = random.choice(list(table_with_indices[table_name]["indices"]))
        return f"{table_name} INDEXED BY {index_name}"


class CreateIndexProcessor:
    def __init__(self, store: Store) -> None:
        self.qp = QueryProcessor(store)

    def get_table_name(self):
        return self.qp.get_table_name()

    def get_column_name(self):
        return self.qp.get_column_name()

    def create_index(self, table_name, index_name):
        return self.qp.create_index(table_name, index_name)


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

    def set_primary_key(self, indexed_columns):
        return self.qp.set_primary_key(indexed_columns)

    def mark_table_temporary(self, table_name):
        return self.qp.mark_table_temporary(table_name)


class SelectProcessor:
    def __init__(self, store: Store) -> None:
        self.qp = QueryProcessor(store)

    def get_table_name(self):
        # print(f"select_processor get_table_name...")
        return self.qp.get_table_name()

    def get_column_name(self):
        return self.qp.get_column_name()

    def get_index(self, table_name):
        return self.qp.get_index(table_name)


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

    def update_table_name(self, table_name, new_table_name):
        # print(f"alter_table_stmt: update_table_name to {new_table_name}")
        return self.qp.update_table_name(table_name, new_table_name)

    def update_column_name(self, column_name, new_column_name):
        return self.qp.update_column_name(column_name, new_column_name)

    def delete_column_name(self, table_name, column_name):
        return self.qp.delete_column_name(table_name, column_name)

    def set_primary_key(self, indexed_columns):
        return self.qp.set_primary_key(indexed_columns)


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
            "CREATE TABLE main.<new-table-name> <view-or-table>",
            opts(
                order=[1, 2],
            ),
        ),
        (
            "CREATE TABLE IF NOT EXISTS <new-table-name> <view-or-table>",
            opts(
                order=[1, 2],
            ),
        ),
        (
            "CREATE TABLE IF NOT EXISTS main.<new-table-name> <view-or-table>",
            opts(
                order=[1, 2],
            ),
        ),
    ],
    "<view-or-table>": [
        (
            "( <column-defs>, <table-constraint> ) <table-options>",
            opts(order=[1, 2, 3]),
        ),
    ],
    "<column-defs>": ["<column-def>, <column-defs>", "<column-def>"],
}

column_def = {
    "<column-def>": [
        ("<new-column-name> <type-name>", opts(order=[1, 2])),
        ("<new-column-name> <type-name> <column-constraint>", opts(order=[1, 2, 3])),
    ],
}

type_name = {
    "<type-name>": [
        "TEXT",
        "INTEGER",
        "REAL",
    ],
}

column_constraint = {
    "<column-constraint>": [
        "<column-constraint-base> DEFAULT ( <constant-expr> )",
        "<column-constraint-base> DEFAULT <literal-value>",
        "<column-constraint-base> DEFAULT <signed-number>",
    ],
    "<column-constraint-base>": [
        "NOT NULL",
        "CHECK ( <expr> )",
        "COLLATE <collation-name>",
        # "<foreign-key-clause>",
        # "GENERATED ALWAYS AS ( <expr> )",
        # "GENERATED ALWAYS AS ( <expr> ) STORED",
        # "GENERATED ALWAYS AS ( <expr> ) VIRTUAL",
        # "AS ( <expr> )",
        # "AS ( <expr> ) STORED",
        # "AS ( <expr> ) VIRTUAL",
    ],
    "<dummy>": [""],
    "<constant-expr>": [
        "<numeric-literal>",
        "<string-literal>",
        "CURRENT_TIME",
        "CURRENT_DATE",
        "CURRENT_TIMESTAMP",
        "<signed-number>",
        "<unary-operator> <constant-expr>",
        "<constant-expr> <binary-operator> <constant-expr>",  # TODO: Can be problematic `string + number`
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
        "NULL",
        "TRUE",
        "FALSE",
        "<numeric-literal>",
        "<string-literal>",
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
        "<table-constraint-base>",
    ],
    "<table-constraint-base>": [
        (
            "PRIMARY KEY ( <indexed-column> ) <conflict-clause>",
            opts(
                post=lambda indexed_columns, _: store.get_query_processor().set_primary_key(
                    indexed_columns
                )
            ),
        ),
        "UNIQUE ( <indexed-column> )",
        "CHECK ( <expr> )",
        # "FOREIGN KEY ( <column-names> ) <foreign-key-clause>",
    ],
    "<indexed-columns>": ["<indexed-column>, <indexed-columns>", "<indexed-column>"],
    "<column-names>": ["<column-name>, <column-names>", "<column-name>"],
}

table_options = {
    "<table-options>": [
        "STRICT",
        "STRICT, <table-options>",
    ]
}

indexed_column = {
    "<indexed-column>": [
        "<column-name>",
        "<column-name> COLLATE <collation-name>",
        "<column-name> ASC",
        "<column-name> COLLATE <collation-name> ASC",
        "<column-name> DESC",
        "<column-name> COLLATE <collation-name> DESC",
    ]
}


expr = {
    "<expr>": [
        "<literal-value>",
        # "<bind-parameter>",  # TODO: what bind-parameter
        # "<schema-name>.<table-name>.<column-name>",
        # "<table-name>.<column-name>",
        "<unary-operator> <expr>",
        # "<column-name>",
        "<expr> <binary-operator> <expr>",
        # "<function-name> ( <function-arguments> )"
        # "<function-name> ( <function-arguments> ) <filter-clause>"
        # "<function-name> ( <function-arguments> ) <over-clause>"
        # "<function-name> ( <function-arguments> ) <filter-clause> <over-clause>"
        # "( <exprs> )",
        "CAST ( <expr> AS <type-name>)",
        "<expr> COLLATE <collation-name>",
        "<expr> LIKE <expr>",
        "<expr> NOT LIKE <expr>",
        # "<expr> LIKE <expr> ESCAPE <expr>",
        # "<expr> NOT LIKE <expr> ESCAPE <expr>",
        # "<expr> GLOB <expr>",
        # "<expr> REGEXP <expr>",
        "<expr> MATCH <expr>",
        # "<expr> NOT GLOB <expr>",
        # "<expr> NOT REGEXP <expr>",
        "<expr> NOT MATCH <expr>",
        "<expr> ISNULL",
        "<expr> NOTNULL",
        "<expr> NOT NULL",
        "<expr> IS <expr>",
        "<expr> IS NOT <expr>",
        # "<expr> IS DISTINCT FROM <expr>",
        # "<expr> IS NOT DISTINCT FROM <expr>",
        "<expr> BETWEEN <expr> and <expr>",
        "<expr> NOT BETWEEN <expr> and <expr>",
        "<expr> IN ()",
        "<expr> NOT IN ()",
        # "<expr> IN ( <select-stmt>)",
        # "<expr> NOT IN ( <select-stmt> )",
        # "<expr> IN ( <exprs> )",
        # "<expr> NOT IN ( <exprs> )",
        # "<expr> IN <schema-name>.<table-name>",
        # "<expr> NOT IN <schema-name>.<table-name>",
        # "<expr> IN <table-name>",
        # "<expr> NOT IN <table-name>",
        # "<expr> IN <schema-name>.<table-function-name> ( <exprs> )",
        # "<expr> NOT IN <schema-name>.<table-function-name> ( <exprs> )",
        # "<expr> IN <table-function-name> ( <exprs> )",
        # "<expr> NOT IN <table-function-name> ( <exprs> )",
        # "( <select-stmt> )",
        # "EXISTS ( <select-stmt> )",
        # "NOT EXISTS ( <select-stmt> )",
        "CASE <when-thens> END",
        "CASE <expr> <when-thens> END",
        "CASE <when-thens> ELSE <expr> END",
        "CASE <expr> <when-thens> ELSE <expr> END",
        # "<raise-function>",
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
        # "",
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
    "<select-stmt>": [("<select-core> <select-1>", opts(order=[1, 2]))],
    # "<select-0>": [
    #     "",
    #     # "WITH",
    #     # "WITH RECURSIVE",
    #     # "WITH <common-table-expressions>",
    #     # "WITH RECURSIVE <common-table-expressions>",
    # ],
    "<common-table-expressions>": [
        "<common-table-expression>, <common-table-expressions>",
        "<common-table-expression>",
    ],
    "<select-core>": [
        (
            "SELECT <result-columns> <from-0> <where-0> <groupby-0> <window-0>",
            opts(order=[4, 1, 2, 3, 5]),
        ),
        (
            "SELECT DISTINCT <result-columns> <from-0> <where-0> <groupby-0> <window-0>",
            opts(order=[4, 1, 2, 3, 5]),
        ),
        (
            "SELECT ALL <result-columns> <from-0> <where-0> <groupby-0> <window-0>",
            opts(order=[4, 1, 2, 3, 5]),
        ),
    ],
    "<from-0>": [
        # "",
        "FROM <join-clause>",
        "FROM <table-or-subquery>",
    ],
    "<where-0>": ["", "WHERE <expr>"],
    "<groupby-0>": ["", "GROUP BY <exprs>"],
    # "<having-0>": [
    #     "",
    #     # "HAVING <expr>"
    # ],
    "<window-0>": [
        # "",
        "WINDOW <window-name> AS <window-defn>"
    ],
    "<result-columns>": ["<result-column>, <result-columns>", "<result-column>"],
    "<values>": ["VALUES ( <exprs> ), <values>", "VALUES ( <exprs> )"],
    "<select-1>": [
        # "",
        "ORDER BY <ordering-term>",
        "LIMIT <limit-number>",
        "ORDER BY <ordering-term> LIMIT <limit-number>",
        "LIMIT <limit-number> OFFSET <limit-number>",
        "LIMIT <limit-number> , <limit-number>",
        "ORDER BY <ordering-term> LIMIT <limit-number> OFFSET <limit-number>",
        "ORDER BY <ordering-term> LIMIT <limit-number> , <limit-number>",
    ],
    "<ordering-terms>": ["<ordering-term>", "<ordering-term>, <ordering-terms>"],
    "<limit-number>": [
        "0x<hexdigits>",
        "0X<hexdigits>",
        "<digits>",
    ],
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
        "<table-name> NOT INDEXED",
        "<table-name> <table-alias> NOT INDEXED",
        "<table-name> AS <table-alias> NOT INDEXED",
        (
            "<table-name> INDEXED BY <index-name>",
            opts(
                post=lambda table_name, _: store.get_query_processor().get_index(
                    table_name
                ),
            ),
        ),
        # (
        #     "<table-name> <table-alias> INDEXED BY <index-name>",
        #     opts(
        #         post=lambda table_name, *_: store.get_query_processor().get_index(
        #             table_name
        #         )
        #     ),
        # ),
        # (
        #     "<table-name> AS <table-alias> INDEXED BY <index-name>",
        #     opts(
        #         post=lambda table_name, *_: store.get_query_processor().get_index(
        #             table_name
        #         )
        #     ),
        # ),
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
        "( <select-stmt> )",
        "( <select-stmt> ) <table-alias>",
        "( <select-stmt> ) AS <table-alias>",
        # "( <table-or-subquerys> )",
        # ("( <join-clause> )", opts(prob=0.0)),
    ]
}

result_column = {
    "<result-column>": [
        "*",
        "<expr>",
        "<expr> <column-alias>",
        "<expr> AS <column-alias>",
    ],
}

window_defn = {
    "<window-defn>": [
        "()",
        "( <base-window-name> )",
        "( PARTITION BY <expr>)",
        "( <base-window-name> PARTITION BY <expr>)",
        "( ORDER BY <ordering-term>)",
        "( <base-window-name> ORDER BY <ordering-term>)",
        "( PARTITION BY <exprs> ORDER BY <ordering-term>)",
        "( <base-window-name> PARTITION BY <exprs> ORDER BY <ordering-term>)",
        "(<frame-spec>)",
        "( <base-window-name> <frame-spec>)",
        "( PARTITION BY <expr> <frame-spec>)",
        "( <base-window-name> PARTITION BY <expr> <frame-spec>)",
        "( ORDER BY <ordering-term> <frame-spec>)",
        "( <base-window-name> ORDER BY <ordering-term> <frame-spec>)",
        "( PARTITION BY <expr> ORDER BY <ordering-term> <frame-spec>)",
        "( <base-window-name> PARTITION BY <expr> ORDER BY <ordering-term> <frame-spec>)",
    ]
}

alter_table_stmt = {
    "<alter-table-stmt>": [
        (
            "ALTER TABLE <table-name> RENAME COLUMN <column-name> TO <new-column-name>",
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
                    table_name, new_table_name
                ),
            ),
        ),
        (
            "ALTER TABLE <table-name> RENAME <column-name> TO <new-column-name>",
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
                prob=0.01,
                post=lambda table_name, column_name: store.get_query_processor().delete_column_name(
                    table_name, column_name
                ),
            ),
        ),
        (
            "ALTER TABLE <table-name> DROP <column-name>",
            opts(
                order=[1, 2],
                prob=0.01,
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
    "<characters>": ["<character><characters>", "<character><character><character>"],
    "<character>": list(string.ascii_letters),
}


blob_literal = {
    # # "<blob-literal>": [
    #     "x'<hexdigits>'",
    #     # "X'<hexdigits>'",
    # ]
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
    "<collation-name>": ["RTRIM", "NOCASE", "BINARY"],
    "<view-name>": ["<characters>"],
    "<savepoint-name>": ["<characters>"],
    "<index-name>": ["<characters>"],
    "<new-index-name>": ["<characters>"],
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
        (
            "CREATE INDEX <new-index-name> ON <table-name> ( <indexed-column> )",
            opts(
                order=[1, 2, 3],
                post=lambda index_name, table_name, _: store.get_query_processor().create_index(
                    table_name, index_name
                ),
            ),
        ),
        (
            "CREATE UNIQUE INDEX <new-index-name> ON <table-name> ( <indexed-column> )",
            opts(
                order=[1, 2, 3],
                post=lambda index_name, table_name, _: store.get_query_processor().create_index(
                    table_name, index_name
                ),
            ),
        ),
        (
            "CREATE INDEX IF NOT EXISTS <new-index-name> ON <table-name> ( <indexed-column> )",
            opts(
                order=[1, 2, 3],
                post=lambda index_name, table_name, _: store.get_query_processor().create_index(
                    table_name, index_name
                ),
            ),
        ),
        (
            "CREATE UNIQUE INDEX IF NOT EXISTS <new-index-name> ON <table-name> ( <indexed-column> )",
            opts(
                order=[1, 2, 3],
                post=lambda index_name, table_name, _: store.get_query_processor().create_index(
                    table_name, index_name
                ),
            ),
        ),
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

pragma_stmt = {
    "<pragma-stmt>": [
        "PRAGMA <pragma-name> = <pragma-value>",
        "PRAGMA <pragma-name> ( <pragma-value> )",
    ],
    "<pragma-value>": [
        "<signed-number>",
        "<string-literal>",
    ],
    "<pragma-name>": ["<characters>"],
}

attach_stmt = {"<attach-stmt>": ["`"]}

grammar = {
    "<start>": [("<phase-1>", opts(prob=1.0)), "<phase-2>"],
    "<phase-1>": [
        (
            "<create-table-stmt>",
            opts(
                pre=lambda: store.append_query_processor(CreateTableProcessor),
                post=lambda _: store.pop_query_processor(),
            ),
        ),
    ],
    "<phase-2>": [
        (
            "<create-index-stmt>",
            opts(
                pre=lambda: store.append_query_processor(CreateIndexProcessor),
                post=lambda _: store.pop_query_processor(),
            ),
        ),
        (
            "<create-view-stmt>",
            opts(
                pre=lambda: store.append_query_processor(SelectProcessor),
                post=lambda _: store.pop_query_processor(),
            ),
        ),
    ],
    "<phase-3>": [
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
            ),
        ),
        # "<begin-stmt>",
        # "<commit-stmt>",
        # "<rollback-stmt>",
        "<pragma-stmt>",
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
    **pragma_stmt,
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
