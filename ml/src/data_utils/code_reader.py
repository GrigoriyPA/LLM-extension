import ast
import builtins
import collections
import typing as tp
import random

from src.constants import github_searcher as github_searcher_constants

FunctionData = collections.namedtuple(
    'FunctionData',
    ['name', 'source', 'docstring', 'variable']
)


class VariableCollector(ast.NodeVisitor):
    def __init__(self) -> None:
        self.variables = []

    def visit_Name(self, node) -> None:
        if (
                isinstance(
                    node.ctx, (ast.Store, ast.Load, ast.Del)
                )
                and not self.is_builtin(node.id)
        ):
            self.variables.append(node.id)
        self.generic_visit(node)

    def visit_Assign(self, node) -> None:
        for target in node.targets:
            self.visit(target)
        self.generic_visit(node)

    def visit_AugAssign(self, node) -> None:
        self.visit(node.target)
        self.generic_visit(node)

    def visit_For(self, node) -> None:
        self.visit(node.target)
        self.generic_visit(node)

    def visit_FunctionDef(self, node) -> None:
        for arg in node.args.args:
            self.variables.append(arg.arg)
        self.generic_visit(node)

    def visit_With(self, node) -> None:
        for item in node.items:
            self.visit(item.optional_vars)
        self.generic_visit(node)

    def is_builtin(self, name) -> bool:
        return name in dir(builtins)


def get_variable_name(function_code: str) -> tp.Optional[str]:
    function_tree = ast.parse(function_code)
    collector = VariableCollector()
    collector.visit(function_tree)
    variables = [
        var for var in collector.variables
        if (
                len(var) >= github_searcher_constants.VARIABLE_MIN_LENGTH
                and var[0] == var[0].lower()
        )

    ]
    if not variables:
        return None
    variable = collections.Counter(variables).most_common(
        random.randint(1, github_searcher_constants.GITHUB_API_TIMEOUT)
    )[-1][0]
    return variable


def get_functions_sources(
        source_code: str,
        ignore_comments: bool = False
) -> tp.List[FunctionData]:
    try:
        tree = ast.parse(source_code)
        code_by_lines = source_code.splitlines(True)
        if ignore_comments:
            code_by_lines = [
                code_line.split('#')[0]
                for code_line in code_by_lines
            ]
        function_sources = []

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                docstring = ast.get_docstring(node)
                start_lineno = node.lineno
                end_lineno = node.end_lineno

                if docstring:
                    doc_node = node.body[0].value
                    func_source = "".join(
                        code_by_lines[start_lineno - 1: doc_node.lineno - 1] +
                        code_by_lines[doc_node.end_lineno: end_lineno]
                    )
                else:
                    func_source = "".join(
                        code_by_lines[start_lineno - 1: end_lineno]
                    )

                variable = get_variable_name(func_source)

                function_sources.append(
                    (node.name, func_source, docstring, variable)
                )
    except Exception as ex:
        return []
    return function_sources


def get_functions_calls(
        source_code: str,
        context_wide: int = 4
) -> tp.List[tp.Tuple[str, str]]:
    tree = ast.parse(source_code)
    code_by_lines = source_code.splitlines(True)
    function_sources = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            left_border = node.lineno - context_wide
            right_border = node.end_lineno + context_wide
            context = "".join(code_by_lines[left_border:right_border + 1])
            name = node.func.id
            function_sources.append((name, context))
    return function_sources


def get_function_name_by_test_name(
        test_name: str
) -> str:
    return test_name[:5]


def is_test(function_name: str) -> bool:
    return 'test_' == function_name[:5]
