# Implement your grammar here in the `grammar` variable.
# You may define additional functions, e.g. for generators.
# You may not import any other modules written by yourself.
# That is, your entire implementation must be in `grammar.py`
# and `fuzzer.py`.

import string
import random
from typing import Any, Dict
from fuzzingbook.Grammars import opts
from pprint import pprint


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
    name_length = random.randint(10, 15)
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
        self.schema = set()
        self.query_processors = []

    def add_schema(self, schema_name):
        self.schema.add(schema_name)

    def remove_schema(self, schema_name):
        self.schema.remove(schema_name)

    def get_schema_name(self):
        res = random.choice(list(self.schema))
        return res

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
        # print(f"appending_query_processor: {query_processor}")
        self.query_processors.append(query_processor(self))
        return True

    def pop_query_processor(self):
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
            "has_primary_key": True,
            "columns": set(["id"]),
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
        return random.choice(list(current_table["columns"] - {"id"}))

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
        # print(f"delete_column_name: {column_name}")
        assert self.table_name is not None
        current_table = self.store.get_table(self.table_name)
        # print("before:")
        # pprint(current_table)
        current_table["columns"].remove(column_name)
        self.store.set_table(self.table_name, current_table)
        # print("after:")
        # pprint(self.store.get_table(self.table_name))
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

    def add_schema(self, schema_name):
        self.store.add_schema(schema_name)
        return True

    def remove_schema(self, schema_name):
        self.store.remove_schema(schema_name)
        return True

    def get_schema_name(self):
        return self.store.get_schema_name()


class InsertProcessor:
    def __init__(self, store: Store) -> None:
        self.qp = QueryProcessor(store)

    def get_table_name(self):
        return self.qp.get_table_name()


class AttachProcessor:
    def __init__(self, store: Store) -> None:
        self.qp = QueryProcessor(store)

    def add_schema(self, schema_name):
        return self.qp.add_schema(schema_name)

    def remove_schema(self, schema_name):
        return self.qp.remove_schema(schema_name)

    def get_schema_name(self):
        return self.qp.get_schema_name()


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


class AnalyzeProcessor:
    def __init__(self, store: Store) -> None:
        self.qp = QueryProcessor(store)

    def get_table_name(self):
        # print(f"select_processor get_table_name...")
        return self.qp.get_table_name()


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
                order=(1, 2),
            ),
        ),
        (
            "CREATE TABLE main.<new-table-name> <view-or-table>",
            opts(
                order=(1, 2),
            ),
        ),
        (
            "CREATE TABLE IF NOT EXISTS <new-table-name> <view-or-table>",
            opts(
                order=(1, 2),
            ),
        ),
        (
            "CREATE TABLE IF NOT EXISTS main.<new-table-name> <view-or-table>",
            opts(
                order=(1, 2),
            ),
        ),
    ],
    "<view-or-table>": [
        (
            "(id INTEGER PRIMARY KEY AUTOINCREMENT, <column-defs>, <table-constraint> ) <table-options>",
            opts(order=(1, 2, 3)),
        ),
    ],
    "<column-defs>": [
        "<column-def>, <column-defs>",
        "<column-def>, <column-def>, <column-def>",
    ],
}

column_def = {
    "<column-def>": [
        (
            "<new-column-name> TEXT <column-constraint-base> DEFAULT ( <string-expr> )",
            opts(order=(1, 2, 3)),
        ),
        (
            "<new-column-name> INTEGER <column-constraint-base> DEFAULT ( <integer-expr> )",
            opts(order=(1, 2, 3)),
        ),
        (
            "<new-column-name> REAL <column-constraint-base> DEFAULT ( <real-expr> )",
            opts(order=(1, 2, 3)),
        ),
    ],
}


column_constraint = {
    "<column-constraint-base>": [
        "NOT NULL",
        "CHECK ( <expr> )",
        "COLLATE <collation-name>",
        # "<foreign-key-clause>",
    ],
    "<dummy>": [""],
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


# foreign_key_clause = {
#     "<foreign-key-clause>": [
#         "REFERENCES <table-name> ( <column-names> ) <foreign-key-clause-base>",
#         "REFERENCES <table-name> <foreign-key-clause-base>",
#         "REFERENCES <table-name>",
#     ],
#     "<column-names>": ["<column-name>, <column-names>", "<column-name>"],
#     "<foreign-key-clause-base>": [
#         "<on-or-matchs-0>",
#         "<on-or-matchs-0> DEFERABLE INITIALLY DEFERRED",
#         "<on-or-matchs-0> DEFERABLE INITIALLY IMMEDIATE",
#         "<on-or-matchs-0> DEFERABLE",
#         "<on-or-matchs-0> NOT DEFERABLE INITIALLY DEFERRED",
#         "<on-or-matchs-0> NOT DEFERABLE INITIALLY IMMEDIATE",
#         "<on-or-matchs-0> NOT DEFERABLE",
#     ],
#     "<on-or-matchs-0>": ["", "<on-or-match>", "<on-or-match> <on-or-matchs-0>"],
#     "<on-or-match>": [
#         "ON DELETE SET NULL",
#         "ON DELETE SET DEFAULT",
#         "ON DELETE CASCADE",
#         "ON DELETE RESTRICT",
#         "ON DELETE NO ACTION",
#         "ON UPDATE SET NULL",
#         "ON UPDATE SET DEFAULT",
#         "ON UPDATE CASCADE",
#         "ON UPDATE RESTRICT",
#         "ON UPDATE NO ACTION",
#         "MATCH <name>",  # TODO: What name?
#     ],
# }

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
    "<column-names>": ["<column-name>, <column-names>", "<column-name>"],
}

table_options = {
    "<table-options>": [
        "STRICT",
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


frame_spec = {
    "<frame-spec>": [
        "<range-row-group> BETWEEN <frame-spec-1> AND <frame-spec-2> <excludes>",
        "<range-row-group> UNBOUNDED PRECEDING <excludes>",
        "<range-row-group> <expr> PRECEDING <excludes>",
        "<range-row-group> CURRENT ROW <excludes>",
    ],
    "<frame-spec-1>": [
        "UNBOUNDED PRECEDING",
        "<integer-expr> PRECEDING",
        "CURRENT ROW",
        "<expr> FOLLOWING",
    ],
    "<frame-spec-2>": [
        "<integer-expr> PRECEDING",
        "CURRENT ROW",
        "<integer-expr> FOLLOWING",
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


select_stmt = {
    "<select-stmt>": [("<select-core> <select-1>", opts(order=(1, 2)))],
    # "<select-0>": [
    #     "",
    #     # "WITH",
    #     # "WITH RECURSIVE",
    #     # "WITH <common-table-expressions>",
    #     # "WITH RECURSIVE <common-table-expressions>",
    # ],
    "<select-core>": [
        "SELECT <core-functions>",
        (
            "SELECT <result-columns> <from-0> <where-0> <groupby-0> <window-0>",
            opts(order=(4, 1, 2, 3, 5)),
        ),
        (
            "SELECT DISTINCT <result-columns> <from-0> <where-0> <groupby-0> <window-0>",
            opts(order=(4, 1, 2, 3, 5)),
        ),
        (
            "SELECT ALL <result-columns> <from-0> <where-0> <groupby-0> <window-0>",
            opts(order=(4, 1, 2, 3, 5)),
        ),
    ],
    "<from-0>": [
        # "",
        "FROM <join-clause>",
        # "FROM <table-or-subquery>",
    ],
    "<where-0>": ["WHERE <expr>"],
    "<groupby-0>": ["GROUP BY <expr>"],
    # "<having-0>": [
    #     "",
    #     # "HAVING <expr>"
    # ],
    "<window-0>": [
        # "",
        "WINDOW <window-name> AS <window-defn>"
    ],
    "<result-columns>": ["<result-column>, <result-columns>", "<result-column>"],
    "<select-1>": [
        # "",
        "ORDER BY <ordering-term>",
        "LIMIT <integer>",
        "ORDER BY <ordering-term> LIMIT <integer>",
        "LIMIT <integer> OFFSET <integer>",
        "LIMIT <integer> , <integer>",
        "ORDER BY <ordering-term> LIMIT <integer> OFFSET <integer>",
        "ORDER BY <ordering-term> LIMIT <integer> , <integer>",
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


join_clause = {
    "<join-clause>": [
        "<table-or-subquery> <join-clause-0>",
    ],
    "<join-clause-0>": [
        "",
        (
            "<join-operator> <table-or-subquery> <join-constraint> <join-clause-0>",
            opts(order=(1, 2, 3, 4)),
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
        "( <select-stmt> )",
        "( <select-stmt> ) <table-alias>",
        "( <select-stmt> ) AS <table-alias>",
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
        "( PARTITION BY <expr> ORDER BY <ordering-term>)",
        "( <base-window-name> PARTITION BY <expr> ORDER BY <ordering-term>)",
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
                order=(1, 2, 3),
                post=lambda table_name, column_name, new_column_name: store.get_query_processor().update_column_name(
                    column_name, new_column_name
                ),
            ),
        ),
        (
            "ALTER TABLE <table-name> RENAME TO <new-table-name>",
            opts(
                order=(1, 2),
                post=lambda table_name, new_table_name: store.get_query_processor().update_table_name(
                    table_name, new_table_name
                ),
            ),
        ),
        (
            "ALTER TABLE <table-name> RENAME <column-name> TO <new-column-name>",
            opts(
                order=(1, 2, 3),
                post=lambda _, column_name, new_column_name: store.get_query_processor().update_column_name(
                    column_name, new_column_name
                ),
            ),
        ),
        (
            "ALTER TABLE <table-name> DROP COLUMN <column-name>",
            opts(
                order=(1, 2),
                prob=0.001,
                post=lambda table_name, column_name: store.get_query_processor().delete_column_name(
                    table_name, column_name
                ),
            ),
        ),
        (
            "ALTER TABLE <table-name> DROP <column-name>",
            opts(
                order=(1, 2),
                prob=0.001,
                post=lambda table_name, column_name: store.get_query_processor().delete_column_name(
                    table_name, column_name
                ),
            ),
        ),
    ]
}


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
    "<column-alias>": ["<characters>"],
    "<window-name>": ["<characters>"],
    "<index-name>": ["<characters>"],
    "<table-alias>": ["<characters>"],
    "<new-column-name>": [
        (
            "<characters>",
            opts(pre=lambda: store.get_query_processor().get_new_column_name()),
        )
    ],
    "<name>": ["<characters>"],
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
                order=(1, 2, 3),
                post=lambda index_name, table_name, _: store.get_query_processor().create_index(
                    table_name, index_name
                ),
            ),
        ),
        # (
        #     "CREATE UNIQUE INDEX <new-index-name> ON <table-name> ( <indexed-column> )",
        #     opts(
        #         order=(1, 2, 3),
        #         post=lambda index_name, table_name, _: store.get_query_processor().create_index(
        #             table_name, index_name
        #         ),
        #     ),
        # ),
        (
            "CREATE INDEX IF NOT EXISTS <new-index-name> ON <table-name> ( <indexed-column> )",
            opts(
                order=(1, 2, 3),
                post=lambda index_name, table_name, _: store.get_query_processor().create_index(
                    table_name, index_name
                ),
            ),
        ),
        # (
        #     "CREATE UNIQUE INDEX IF NOT EXISTS <new-index-name> ON <table-name> ( <indexed-column> )",
        #     opts(
        #         order=(1, 2, 3),
        #         post=lambda index_name, table_name, _: store.get_query_processor().create_index(
        #             table_name, index_name
        #         ),
        #     ),
        # ),
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
        "PRAGMA <pragma-name> = <integer>",
        "PRAGMA <pragma-name>",
    ],
    "<pragma-name>": [
        "analysis_limit",
        "application_id",
        "auto_vacuum",
        "automatic_index",
        "busy_timeout",
        "cache_size",
        "cache_spill",
        "cell_size_check",
        "checkpoint_fullfsync",
        "collation_list",
        "compile_options",
        "data_version",
        "database_list",
        "defer_foreign_keys",
        "encoding",
        "foreign_key_check",
        "foreign_key_list",
        "foreign_keys",
        "freelist_count",
        "fullfsync",
        "function_list",
        "hard_heap_limit",
        "ignore_check_constraints",
        "incremental_vacuum",
        "index_info",
        "index_list",
        "index_xinfo",
        "integrity_check",
        "journal_mode",
        "journal_size_limit",
        "legacy_alter_table",
        "legacy_file_format",
        "locking_mode",
        "max_page_count",
        "mmap_size",
        "module_list",
        "optimize",
        "page_count",
        "page_size",
        "pragma_list",
        "query_only",
        "quick_check",
        "read_uncommitted",
        "recursive_triggers",
        "reverse_unordered_selects",
        "secure_delete",
        "shrink_memory",
        "soft_heap_limit",
        "stats³",
        "synchronous",
        "table_info",
        "table_list",
        "table_xinfo",
        "temp_store",
        "threads",
        "trusted_schema",
        "user_version",
        "wal_autocheckpoint",
        "wal_checkpoint",
    ],
}

analyze_stmt = {
    "<analyze-stmt>": [
        "ANALYZE main",
        # "ANALYZE <index-name>",
        "ANALYZE <table-name>",
    ]
}

vacuum_stmt = {
    "<vacuum-stmt>": [
        "VACUUM main",
    ]
}

drop_index_stmt = {
    "<drop-index-stmt>": [
        "DROP INDEX IF EXISTS <name>",
    ]
}

drop_table_stmt = {
    "<drop-table-stmt>": [
        "DROP TABLE IF EXISTS <name>",
    ]
}

drop_view_stmt = {
    "<drop-view-stmt>": [
        "DROP VIEW IF EXISTS <name>",
    ]
}

attach_stmt = {
    "<attach-stmt>": [
        "ATTACH DATABASE <name> AS <name>",
        "ATTACH <name> as <name>",
    ]
}

detach_stmt = {
    "<detach-stmt>": [
        "DETACH <name>",
        "DETACH DATABASE <name>",
    ],
}

insert_stmt = {
    "<insert-stmt>": [
        "INSERT INTO <table-name> DEFAULT VALUES",
        "REPLACE INTO <table-name> DEFAULT VALUES",
    ]
}


expr = {
    "<expr>": [
        "<integer-expr>",
        "<string-expr>",
        "<real-expr>",
        "<bool-expr>",
        "<datetime-expr>",
        "NULL",
        "coalesce(<expr-csv>)",
        "ifnull(<expr>, <expr>)",
        "iif(<bool-expr>, <expr>, <expr>)",
        "nullif(<expr>, <expr>)",
    ],
    "<expr-csv>": [
        "<expr>, <expr>",
    ],
}

core_functions = {
    "<core-functions>": [
        "changes()",
        "last_insert_rowid()",
        "total_changes()",
    ]
}

datetime_expr = {
    "<datetime-expr>": [
        "CURRENT_TIME",
        "CURRENT_DATE",
        "CURRENT_TIMESTAMP",
    ]
}

bool_expr = {
    "<bool-expr>": [
        "TRUE",
        "FALSE",
        "like(<string-literal>, <string-literal>)",
        "like(<string-literal>, <string-literal>, '<character>')",
    ]
}

real = {
    "<real>": [
        ".<integer><exponent>",
        "<integer><exponent>",
        "<integer>.<integer><exponent>",
    ],
    "<exponent>": [
        "E<integer>",
        "E+<integer>",
        "E-<integer>",
        "e<integer>",
        "e+<integer>",
        "e-<integer>",
    ],
}

string_literal = {
    "<string-literal>": ["'<characters>'"],
    "<characters>": [("<dummy>", opts(pre=get_random_string))],
    "<character>": [
        ("<dummy>", opts(pre=lambda: random.choice(list(string.ascii_letters))))
    ],
}

string_expr = {
    "<string-expr>": [
        "<string-literal>",
        "char(<integer-csv>)",
        "concat(<string-literal-csv>)",
        "concat('<character>', <string-literal-csv>)",
        "hex(<integer>)",
        "hex(<real>)",
        "lower(<string-literal>)",
        "ltrim(<string-literal>)",
        "max(<string-literal-csv>)",
        "min(<string-literal-csv>)",
        "replace(<string-literal>, <string-literal>, <string-literal>)",
        "rtrim(<string-literal>)",
        "substring(<string-literal>, '<character>')",
        "substring(<string-literal>, '<character>', <integer>)",
        "trim(<string-literal>)",
        "upper(<string-literal>)",
    ],
    "<string-literal-csv>": [
        "<string-literal>, <string-literal>",
    ],
}

real_expr = {
    "<real-expr>": [
        "<real>",
        "<unary-operator> <real>",
        "<real> <binary-operator> <real>",
        "abs(<real>)",
        "max(<real-csv>)",
        "min(<real-csv>)",
        # "acos(<real>)",
        # "acosh(<real>)",
        # "asin(<real>)",
        # "asinh(<real>)",
        # "atan(<real>)",
        # "atan2(<real>,<real>)",
        # "atanh(<real>)",
        # "cos(<real>)",
        # "cosh(<real>)",
        # "degrees(<real>)",
        # "exp(<real>)",
        # "ln(<real>)",
        # "log(<real>)",
        # "log(<integer>, <real>)",
        # "log10(<real>)",
        # "log2(<real>)",
        # "mod(<real>)",
        # "pi()",
        # "radians(<real>)",
        # "sin(<real>)",
        # "sinh(<real>)",
        # "sqrt(<real>)",
        # "tan(<real>)",
        # "tanh(<real>)",
    ],
    "<real-csv>": [
        "<real>, <real>",
    ],
}

integer_expr = {
    "<integer-expr>": [
        "<integer>",
        "<unary-operator> <integer>",
        "<integer> <binary-operator> <integer>",
        "abs(<integer>)",
        "instr(<string-literal>, <string-literal>)",
        "length(<string-literal>)",
        "max(<integer-csv>)",
        "min(<integer-csv>)",
        "octet_length(<string-literal>)",
        "random()",
        "round(<real>)",
        "sign(<integer>)",
        "unicode(<string-literal>)",
        # "ceil(<integer>)",
        # "ceiling(<integer>)",
        # "floor(<integer>)",
        # "mod(<integer>, <integer>)",
        # "pow(<integer>, <integer>)",
        # "power(<integer>, <integer>)",
        # "trunc(<integer>)",
    ],
    "<integer>": [("<dummy>", opts(pre=lambda: random.randint(1, 10_000)))],
    "<integer-csv>": [
        "<integer>, <integer>",
    ],
}

digit = {"<digit>": [("<dummy>", opts(pre=lambda: random.choice(list("0123456789"))))]}

unary_operator = {
    "<unary-operator>": ["+", "-"],
}

binary_operator = {
    "<binary-operator>": [
        (
            "<dummy>",
            opts(
                pre=lambda: random.choice(
                    [
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
                    ]
                )
            ),
        )
    ],
}

explain_stmt = {
    "<explain-stmt>": [
        "EXPLAIN <stmt>",
        "EXPLAIN QUERY PLAN <stmt>",
    ]
}

stmt = {
    "<stmt>": [
        "<create-table-stmt>",
        "<create-index-stmt>",
        "<create-view-stmt>",
        "<insert-stmt>",
        "<select-stmt>",
        "<alter-table-stmt>",
        "<analyze-stmt>",
        "<pragma-stmt>",
        "<vacuum-stmt>",
        "<drop-table-stmt>",
        "<drop-index-stmt>",
        "<drop-view-stmt>",
        "<begin-stmt>",
        "<commit-stmt>",
        "<rollback-stmt>",
        "<attach-stmt>",
        "<detach-stmt>",
    ]
}

grammar = {
    "<start>": ["<phase-1>", "<phase-2>", "<phase-3>"],
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
            "<insert-stmt>",
            opts(
                pre=lambda: store.append_query_processor(InsertProcessor),
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
        (
            "<analyze-stmt>",
            opts(
                pre=lambda: store.append_query_processor(AnalyzeProcessor),
                post=lambda _: store.pop_query_processor(),
            ),
        ),
        "<pragma-stmt>",
        ("<drop-table-stmt>", opts(prob=0.01)),
        ("<drop-index-stmt>", opts(prob=0.01)),
        ("<drop-view-stmt>", opts(prob=0.01)),
        ("<vacuum-stmt>", opts(prob=0.001)),
        ("<begin-stmt>", opts(prob=0.001)),
        ("<commit-stmt>", opts(prob=0.001)),
        ("<rollback-stmt>", opts(prob=0.001)),
        ("<attach-stmt>", opts(prob=0.001)),
        ("<detach-stmt>", opts(prob=0.001)),
        (
            "<select-stmt>",
            opts(
                pre=lambda: store.append_query_processor(SelectProcessor),
                post=lambda _: store.pop_query_processor(),
            ),
        ),
    ],
    **alter_table_stmt,
    **analyze_stmt,
    **attach_stmt,
    **begin_stmt,
    **binary_operator,
    **bool_expr,
    **column_constraint,
    **column_def,
    **commit_stmt,
    **conflict_clause,
    **core_functions,
    **create_index_stmt,
    **create_table_stmt,
    **create_view_stmt,
    **datetime_expr,
    **detach_stmt,
    **digit,
    **drop_index_stmt,
    **drop_table_stmt,
    **drop_view_stmt,
    **expr,
    **integer_expr,
    **real_expr,
    **real,
    **string_expr,
    # **foreign_key_clause,
    **frame_spec,
    **indexed_column,
    **join_clause,
    **join_constraint,
    **join_operator,
    **misc,
    **pragma_stmt,
    **result_column,
    **rollback_stmt,
    **select_stmt,
    **string_literal,
    **table_constraint,
    **table_options,
    **table_or_subquery,
    **unary_operator,
    **vacuum_stmt,
    **window_defn,
    **insert_stmt,
    **ordering_term,
    **explain_stmt,
    **stmt,
}


if __name__ == "__main__":
    from fuzzingbook.Grammars import is_valid_grammar, trim_grammar
    from pprint import pprint

    is_valid_grammar(grammar)
