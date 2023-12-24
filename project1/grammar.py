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

    def get_table_names(self):
        return set(self.store.keys())

    def add_table(self, table_name):
        self.store[table_name] = {}


class CreateTableProcessor:
    def __init__(self, store: Store) -> None:
        self.store = store

    def get_new_table_name(self):
        table_names = self.store.get_table_names()
        new_name = get_random_string()
        while new_name in table_names:
            new_name = self.get_random_string()

        self.store.add_table(new_name)

        return new_name

    def get_new_column_name(self):
        new_name = self.get_random_string()
        # print(f"current_table_name: {self.current_table_name}")
        current_table = self.table_store[self.current_table_name]

        while new_name in current_table:
            new_name = self.get_random_string()

        current_table[new_name] = ""
        self.table_store[self.current_table_name] = current_table

        return new_name


def get_table_name(self):
    result = random.choice(list(self.table_store.keys()))
    self.current_table_name = result
    # print(f"current_table_name: {self.current_table_name}, result: {result}")
    return self.current_table_name


def update_table_name(self, new_table_name):
    self.table_store[new_table_name] = self.table_store[self.current_table_name]
    self.table_store.pop(self.current_table_name)
    self.current_table_name = new_table_name


def get_column_name(self):
    # print(f"current_table_name: {self.current_table_name}")
    return random.choice(list(self.table_store[self.current_table_name].keys()))


def update_column_name(self, column_name, new_column_name):
    self.table_store[self.current_table_name][new_column_name] = self.table_store[
        self.current_table_name
    ][column_name]
    self.table_store[self.current_table_name].pop(column_name)


def delete_column_name(self, column_name):
    self.table_store[self.current_table_name].pop(column_name)


name_store = Store()

create_table_stmt = {
    "<create-table-stmt>": [
        "CREATE TABLE <new-table-name> <view-or-table>",
        # ("CREATE TEMP TABLE <new-table-name> <view-or-table>", ,
        # ("CREATE TEMPORARY TABLE <new-table-name> <view-or-table>", ,
        # ("CREATE TABLE main.<table-name> <view-or-table>", ,
        # ("CREATE TEMP TABLE temp.<table-name> <view-or-table>", ,
        # (
        #     "CREATE TEMPORARY TABLE temp.<table-name> <view-or-table>",
        #     ,
        # ),
        "CREATE TABLE IF NOT EXISTS <new-table-name> <view-or-table>",
        # (
        #     "CREATE TEMP TABLE IF NOT EXISTS <new-table-name> <view-or-table>",
        #     ,
        # ),
        # (
        #     "CREATE TEMPORARY TABLE IF NOT EXISTS <new-table-name> <view-or-table>",
        #     ,
        # ),
        # (
        #     "CREATE TABLE IF NOT EXISTS main.<table-name> <view-or-table>",
        #     ,
        # ),
        # (
        #     "CREATE TEMP TABLE IF NOT EXISTS temp.<table-name> <view-or-table>",
        #     ,
        # ),
        # (
        #     "CREATE TEMPORARY TABLE IF NOT EXISTS temp.<table-name> <view-or-table>",
        #     ,
        # ),
    ],
    "<view-or-table>": [
        "AS <select-stmt>",
        "( <column-defs> )",
    ],
    "<column-defs>": ["<column-def>, <column-defs>", "<column-def>"],
}

column_def = {
    "<column-def>": [
        "<new-column-name>",
        "<new-column-name> <type-name>",
    ],
}

type_name = {
    "<type-name>": [
        "<data-type>",
    ],
    "<data-type>": [
        "TEXT",
    ],
}

# column_constraint = {
#     "<column-constraint>": [
#         "CONSTRAINT <column-name> <column-constraint-base>",
#         "<column-constraint-base>",
#     ],
#     "<column-constraint-base>": [
#         "PRIMARY KEY <conflict-clause>",
#         "PRIMARY KEY ASC <conflict-clause>",
#         "PRIMARY KEY DESC <conflict-clause>",
#         "PRIMARY KEY <conflict-clause> AUTOINCREMENT",
#         "PRIMARY KEY ASC <conflict-clause> AUTOINCREMENT",
#         "PRIMARY KEY DESC <conflict-clause> AUTOINCREMENT",
#         "NOT NULL <conflict-clause>",
#         "UNIQUE <conflict-clause>",
#         "CHECK ( <expr> )",
#         "DEFAULT ( <expr> )",
#         "DEFAULT <literal-value>",
#         "DEFAULT <signed-number>",
#         "COLLATE <collation-name>",
#         "<foreign-key-clause>",
#         "GENERATED ALWAYS AS ( <expr> )",
#         "GENERATED ALWAYS AS ( <expr> ) STORED",
#         "GENERATED ALWAYS AS ( <expr> ) VIRTUAL",
#         "AS ( <expr> )",
#         "AS ( <expr> ) STORED",
#         "AS ( <expr> ) VIRTUAL",
#     ],
# }

# conflict_clause = {
#     "<conflict-clause>": [
#         "",
#         "ON CONFLICT ROLLBACK",
#         "ON CONFLICT ABORT",
#         "ON CONFLICT FAIL",
#         "ON CONFLICT IGNORE",
#         "ON CONFLICT REPLACE",
#     ],
# }

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

# table_constraint = {
#     "<table-constraint>": [
#         "CONSTRAINT <table-name> <table-constraint-base>",
#         "<table-constraint-base>",
#     ],
#     "<table-constraint-base>": [
#         "PRIMARY KEY ( <indexed-columns> ) <conflict-clause>",
#         "UNIQUE ( <indexed-columns> ) <conflict-clause>",
#         "CHECK ( <expr> )",
#         "FOREIGN KEY ( <column-names> ) <foreign-key-clause>",
#     ],
#     "<indexed-columns>": ["<indexed-column>, <indexed-columns>", "<indexed-column>"],
#     "<column-names>": ["<column-name>, <column-names>", "<column-name>"],
# }

# table_options = {
#     "<table-options>": [
#         "WIHTOUT ROWID",
#         "STRICT",
#         "WIHTOUT ROWID, <table-options>",
#         "STRICT, <table-options>",
#     ]
# }

# indexed_column = {
#     "<indexed-column>": [
#         "<column-name>",
#         "<expr>",
#         "<column-name> COLLATE <collation-name>",
#         "<expr> COLLATE <collation-name>",
#         "<column-name> ASC",
#         "<expr> ASC",
#         "<column-name> COLLATE <collation-name> ASC",
#         "<expr> COLLATE <collation-name> ASC",
#         "<column-name> DESC",
#         "<expr> DESC",
#         "<column-name> COLLATE <collation-name> DESC",
#         "<expr> COLLATE <collation-name> DESC",
#     ]
# }

expr = {
    "<expr>": [
        "<literal-value>",
        # "<bind-parameter>",  # TODO: what bind-parameter
        # "<schema-name>.<table-name>.<column-name>",
        # "<table-name>.<column-name>",
        "<column-name>",
        "<unary-operator> <expr>",
        "<expr> <binary-operator> <expr>",
        # "<function-name> ( <function-arguments> )"
        # "<function-name> ( <function-arguments> ) <filter-clause>"
        # "<function-name> ( <function-arguments> ) <over-clause>"
        # "<function-name> ( <function-arguments> ) <filter-clause> <over-clause>"
        "( <exprs> )",
        # "CAST ( <expr> AS <type-name>)",
        # "<expr> COLLATE <collation-name>",
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
        "<expr> IN ( <select-stmt >)",
        "<expr> NOT IN ( <select-stmt> )",
        "<expr> IN ( <exprs> )",
        "<expr> NOT IN ( <exprs> )",
        # "<expr> IN <schema-name>.<table-name>",
        # "<expr> NOT IN <schema-name>.<table-name>",
        "<expr> IN <table-name>",
        "<expr> NOT IN <table-name>",
        # "<expr> IN <schema-name>.<table-function-name> ( <exprs> )",
        # "<expr> NOT IN <schema-name>.<table-function-name> ( <exprs> )",
        # "<expr> IN <table-function-name> ( <exprs> )",
        # "<expr> NOT IN <table-function-name> ( <exprs> )",
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

# filter_clause = {"<filter-clause>": ["FILTER ( WHERE <expr> )"]}

# function_arguments = {
#     "<function-arguments>": [
#         "",
#         "*",
#         "DISTINCT <exprs>",
#         "<exprs>",
#         "DISTINCT <exprs> ORDER BY <ordering-terms>",
#         "<exprs> ORDER BY <ordering-terms>",
#     ],
#     "<ordering-terms>": [
#         "<ordering-term>",
#         "<ordering-term>, <ordering-terms>",
#     ],
# }

# over_clause = {
#     "<over-clause>": [
#         "OVER <window-name>",
#         "OVER ( )",
#         "OVER ( <base-window-name> )",
#         "OVER ( PARTITION BY <exprs> )",
#         "OVER ( <base-window-name> PARTITION BY <exprs> )",
#         "OVER ( ORDER BY <ordering-terms> )",
#         "OVER ( <base-window-name> ORDER BY <ordering-terms> )",
#         "OVER ( PARTITION BY <exprs> ORDER BY <ordering-terms> )",
#         "OVER ( <base-window-name> PARTITION BY <exprs> ORDER BY <ordering-terms> )",
#         "OVER ( <frame-spec> )",
#         "OVER ( <base-window-name> <frame-spec> )",
#         "OVER ( PARTITION BY <exprs> <frame-spec> )",
#         "OVER ( <base-window-name> PARTITION BY <exprs> <frame-spec> )",
#         "OVER ( ORDER BY <ordering-terms> <frame-spec> )",
#         "OVER ( <base-window-name> ORDER BY <ordering-terms> <frame-spec> )",
#         "OVER ( PARTITION BY <exprs> ORDER BY <ordering-terms> <frame-spec> )",
#         "OVER ( <base-window-name> PARTITION BY <exprs> ORDER BY <ordering-terms> <frame-spec> )",
#     ]
# }

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
    "<select-stmt>": ["<select-0> <select-cores> <select-1>"],
    "<select-0>": [
        "",
        # "WITH",
        # "WITH RECURSIVE",
        # "WITH <common-table-expressions>",
        # "WITH RECURSIVE <common-table-expressions>",
    ],
    # "<common-table-expressions>": [
    #     "<common-table-expression>, <common-table-expressions>",
    #     "<common-table-expression>",
    # ],
    "<select-cores>": [
        "<select-core>",
        # "<select-core> <compound-operator> <select-cores>",
    ],
    "<select-core>": [
        "VALUES <values>",
        "SELECT <result-columns> <from-0> <where-0> <groupby-0> <having-0> <window-0>",
        "SELECT DISTINCT <result-columns> <from-0> <where-0> <groupby-0> <having-0> <window-0>",
        "SELECT ALL <result-columns> <from-0> <where-0> <groupby-0> <having-0> <window-0>",
    ],
    "<from-0>": [
        "",
        # "FROM <join-clause>",
        "FROM <table-or-subquerys>",
    ],
    "<where-0>": [
        "",
        # "WHERE <expr>"
    ],
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
    # "<window-defs>": [
    #     "<window-name> AS <window-defn>",
    #     "<window-name> AS <window-defn>, <window-defs>",
    # ],
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

# common_table_expression = {
#     "<common-table-expression>": [
#         "<table-name> AS ( <select-stmt> )",
#         "<table-name> ( <column-names> ) AS ( <select-stmt> )",
#         "<table-name> AS MATERIALIZED ( <select-stmt> )",
#         "<table-name> ( <column-names> ) AS MATERIALIZED ( <select-stmt> )",
#         "<table-name> AS NOT MATERIALIZED ( <select-stmt> )",
#         "<table-name> ( <column-names> ) AS NOT MATERIALIZED ( <select-stmt> )",
#     ]
# }

# compound_operator = {
#     "<compound-operator>": ["UNION", "UNION ALL", "INTERSECT", "EXCEPT"]
# }

# join_clause = {
#     "<join-clause>": [
#         "<table-or-subquery> <join-clause-0>",
#     ],
#     "<join-clause-0>": [
#         "",
#         "<join-operator> <table-or-subquery> <join-constraint> <join-clause-0>",
#     ],
# }

# join_constraint = {"<join-constraint>": ["", "ON <expr>", "USING ( <column-names> )"]}

# join_operator = {
#     "<join-operator>": [
#         " , ",
#         "CROSS JOIN" "JOIN",
#         "NATURAL JOIN",
#         "LEFT JOIN",
#         "NATURAL LEFT JOIN",
#         "RIGHT JOIN",
#         "NATURAL RIGHT JOIN" "FULL JOIN",
#         "NATURAL FULL JOIN",
#         "LEFT OUTER JOIN",
#         "NATURAL LEFT OUTER JOIN",
#         "RIGHT OUTER JOIN",
#         "NATURAL RIGHT OUTER JOIN" "FULL OUTER JOIN",
#         "NATURAL FULL OUTER JOIN",
#         "INNER JOIN",
#         "NATURAL INNER JOIN",
#     ]
# }

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
        "( <select-stmt> )",
        "( <select-stmt> ) <table-alias>",
        "( <select-stmt> ) AS <table-alias>",
        "( <table-or-subquerys> )",
        # "( <join-clause> )",
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

# window_defn = {
#     "<window-defn>": [
#         "()",
#         "( <base-window-name> )",
#         "( PARTITION BY <exprs>)",
#         "( <base-window-name> PARTITION BY <exprs>)",
#         "( ORDER BY <ordering-terms>)",
#         "( <base-window-name> ORDER BY <ordering-terms>)",
#         "( PARTITION BY <exprs> ORDERING BY <ordering-terms>)",
#         "( <base-window-name> PARTITION BY <exprs> ORDERING BY <ordering-terms>)",
#         "(<frame-spec>)",
#         "( <base-window-name> <frame-spec>)",
#         "( PARTITION BY <exprs> <frame-spec>)",
#         "( <base-window-name> PARTITION BY <exprs> <frame-spec>)",
#         "( ORDER BY <ordering-terms> <frame-spec>)",
#         "( <base-window-name> ORDER BY <ordering-terms> <frame-spec>)",
#         "( PARTITION BY <exprs> ORDERING BY <ordering-terms> <frame-spec>)",
#         "( <base-window-name> PARTITION BY <exprs> ORDERING BY <ordering-terms> <frame-spec>)",
#     ]
# }

alter_table_stmt = {
    "<alter-table-stmt>": [
        "ALTER TABLE <table-name> COLUMN <column-name> TO <new-column-name>",
        "ALTER TABLE <table-name> RENAME TO <new-table-name>",
        "ALTER TABLE <table-name> <column-name> TO <new-column-name>",
        "ALTER TABLE <table-name> ADD COLUMN <column-def>",
        "ALTER TABLE <table-name> ADD <column-def>",
        "ALTER TABLE <table-name> DROP COLUMN <column-name>",
        "ALTER TABLE <table-name> DROP <column-name>",
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
        "<characters>",
    ],
    "<column-name>": [
        "<characters>",
    ],
    "<base-window-name>": ["<characters>"],
    "<new-table-name>": [
        "<characters>",
    ],
    # "<schema-name>": ["<characters>"],
    "<column-alias>": ["<characters>"],
    "<table-function-name>": ["<characters>"],
    "<window-name>": ["<characters>"],
    "<function-name>": ["<characters>"],
    "<index-name>": ["<characters>"],
    "<table-alias>": ["<characters>"],
    "<new-column-name>": ["<characters>"],
    # "<name>": ["<characters>"],
    "<error-message>": ["<characters>"],
    "<bind-parameter>": ["<characters>"],
    "<collation-name>": ["<characters>"],
}

grammar = {
    "<start>": ["<sql-stmt-list>"],
    "<sql-stmt-list>": [
        # "",
        "<sql-stmt>",
        # "<sql-stmt> ; <sql-stmt-list>",
    ],
    "<sql-stmt>": [
        "<create-table-stmt>",
        "<select-stmt>",
        "<alter-table-stmt>",
    ],
    **create_table_stmt,
    **column_def,
    **type_name,
    # **column_constraint,
    # **conflict_clause,
    **literal_value,
    **signed_number,
    # **foreign_key_clause,
    # **table_constraint,
    # **table_options,
    # **indexed_column,
    # **filter_clause,
    # **function_arguments,
    **expr,
    # **over_clause,
    **frame_spec,
    **ordering_term,
    **raise_function,
    **numeric_literal,
    **string_literal,
    **blob_literal,
    **select_stmt,
    # **common_table_expression,
    # **compound_operator,
    # **join_clause,
    # **join_constraint,
    # **join_operator,
    **table_or_subquery,
    **result_column,
    # **window_defn,
    **alter_table_stmt,
    **digit,
    **hexdigit,
    **unary_operator,
    **binary_operator,
    **misc,
}


if __name__ == "__main__":
    from fuzzingbook.GeneratorGrammarFuzzer import ProbabilisticGeneratorGrammarFuzzer
    from fuzzingbook.Grammars import trim_grammar
    from pprint import pprint

    fuzzer = ProbabilisticGeneratorGrammarFuzzer(trim_grammar(grammar))

    for i in range(3):
        print(fuzzer.fuzz())
        print()

    grammar["<sql-stmt>"].pop()

    for i in range(5):
        print(fuzzer.fuzz())
        print()
