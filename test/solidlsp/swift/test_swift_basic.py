import os

import pytest

from solidlsp import SolidLanguageServer
from solidlsp.ls_config import Language
from solidlsp.ls_utils import SymbolUtils


@pytest.mark.swift
class TestSwiftLanguageServer:
    @pytest.mark.parametrize("language_server", [Language.SWIFT], indirect=True)
    @pytest.mark.skip(reason="SourceKit-LSP reference finding needs investigation")
    def test_find_references_raw(self, language_server: SolidLanguageServer) -> None:
        # Test finding references to the Calculator class
        file_path = os.path.join("Sources", "test_repo", "Calculator.swift")
        symbols = language_server.request_document_symbols(file_path)
        calculator_symbol = None
        for sym in symbols[0]:
            if sym.get("name") == "Calculator":
                calculator_symbol = sym
                break
        assert calculator_symbol is not None, "Could not find 'Calculator' class symbol"
        sel_start = calculator_symbol["selectionRange"]["start"]
        refs = language_server.request_references(file_path, sel_start["line"], sel_start["character"])
        assert any(
            "main.swift" in ref.get("relativePath", "") for ref in refs
        ), "main.swift should reference Calculator class"

    @pytest.mark.parametrize("language_server", [Language.SWIFT], indirect=True)
    def test_find_symbol(self, language_server: SolidLanguageServer) -> None:
        symbols = language_server.request_full_symbol_tree()
        assert SymbolUtils.symbol_tree_contains_name(symbols, "Calculator"), "Calculator class not found in symbol tree"
        assert SymbolUtils.symbol_tree_contains_name(symbols, "add(_:_:)"), "add method not found in symbol tree"
        assert SymbolUtils.symbol_tree_contains_name(symbols, "User"), "User struct not found in symbol tree"
        assert SymbolUtils.symbol_tree_contains_name(symbols, "UserManager"), "UserManager class not found in symbol tree"

    @pytest.mark.parametrize("language_server", [Language.SWIFT], indirect=True)
    @pytest.mark.skip(reason="SourceKit-LSP reference finding needs investigation")
    def test_find_referencing_symbols(self, language_server: SolidLanguageServer) -> None:
        # Find references to 'add' method defined in Calculator.swift
        file_path = os.path.join("Sources", "test_repo", "Calculator.swift")
        symbols = language_server.request_document_symbols(file_path)
        add_symbol = None
        for sym in symbols[0]:
            if sym.get("name") == "add(_:_:)":
                add_symbol = sym
                break
        assert add_symbol is not None, "Could not find 'add' method symbol in Calculator.swift"
        sel_start = add_symbol["selectionRange"]["start"]
        refs = language_server.request_references(file_path, sel_start["line"], sel_start["character"])
        assert any(
            "main.swift" in ref.get("relativePath", "") for ref in refs
        ), "main.swift should reference add method"

    @pytest.mark.parametrize("language_server", [Language.SWIFT], indirect=True)
    def test_overview_methods(self, language_server: SolidLanguageServer) -> None:
        symbols = language_server.request_full_symbol_tree()
        assert SymbolUtils.symbol_tree_contains_name(symbols, "Calculator"), "Calculator missing from overview"
        assert SymbolUtils.symbol_tree_contains_name(symbols, "User"), "User missing from overview"
        assert SymbolUtils.symbol_tree_contains_name(symbols, "UserManager"), "UserManager missing from overview"
        assert SymbolUtils.symbol_tree_contains_name(symbols, "CalculatorError"), "CalculatorError missing from overview"
