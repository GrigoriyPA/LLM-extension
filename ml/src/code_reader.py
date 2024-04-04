import ast
import typing as tp


def get_functions_sources(
        source_code: str
) -> tp.List[tp.Tuple[str, str, str]]:
    tree = ast.parse(source_code)
    code_by_lines = source_code.splitlines(True)
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

            function_sources.append(
                (node.name, func_source, docstring)
            )

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
