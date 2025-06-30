"""
Provides Swift specific instantiation of the LanguageServer class using SourceKit-LSP.
Contains various configurations and settings specific to Swift.
"""

import logging
import os
import pathlib
import subprocess
import threading

from overrides import override

from solidlsp.ls import SolidLanguageServer
from solidlsp.ls_config import LanguageServerConfig
from solidlsp.ls_logger import LanguageServerLogger
from solidlsp.lsp_protocol_handler.lsp_types import InitializeParams
from solidlsp.lsp_protocol_handler.server import ProcessLaunchInfo


class SourceKitLSP(SolidLanguageServer):
    """
    Provides Swift specific instantiation of the LanguageServer class using SourceKit-LSP.
    Contains various configurations and settings specific to Swift.
    """

    def __init__(self, config: LanguageServerConfig, logger: LanguageServerLogger, repository_root_path: str):
        """
        Creates a SourceKitLSP instance. This class is not meant to be instantiated directly.
        Use LanguageServer.create() instead.
        """
        # Find SourceKit-LSP executable path
        sourcekit_lsp_path = self._find_sourcekit_lsp_path(logger)

        super().__init__(
            config,
            logger,
            repository_root_path,
            ProcessLaunchInfo(cmd=sourcekit_lsp_path, cwd=repository_root_path),
            "swift",
        )

        # Event to signal when server is ready
        self.server_ready = threading.Event()

    def _find_sourcekit_lsp_path(self, logger: LanguageServerLogger) -> str:
        """
        Find the SourceKit-LSP executable path using xcode-select.
        """
        try:
            # Use xcode-select to find the active Xcode installation
            result = subprocess.run(["xcode-select", "--print-path"], capture_output=True, text=True, check=True)
            xcode_developer_path = result.stdout.strip()

            # Construct the path to sourcekit-lsp
            sourcekit_lsp_path = os.path.join(xcode_developer_path, "Toolchains/XcodeDefault.xctoolchain/usr/bin/sourcekit-lsp")

            if os.path.exists(sourcekit_lsp_path):
                logger.log(f"Found SourceKit-LSP at: {sourcekit_lsp_path}", logging.INFO)
                return sourcekit_lsp_path
            else:
                logger.log(f"SourceKit-LSP not found at expected path: {sourcekit_lsp_path}", logging.WARNING)
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            logger.log(f"Failed to run xcode-select: {e}", logging.WARNING)

        # Fallback paths
        fallback_paths = [
            "/usr/bin/sourcekit-lsp",
            "/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/sourcekit-lsp",
        ]

        for path in fallback_paths:
            if os.path.exists(path):
                logger.log(f"Using fallback SourceKit-LSP at: {path}", logging.INFO)
                return path

        # If no path found, raise an error
        raise FileNotFoundError("SourceKit-LSP not found. Please ensure Xcode or Swift toolchain is installed.")

    @override
    def is_ignored_dirname(self, dirname: str) -> bool:
        """Ignore common Swift build directories"""
        return super().is_ignored_dirname(dirname) or dirname in [".build", "DerivedData", ".swiftpm"]

    def _get_initialize_params(self, repository_absolute_path: str) -> InitializeParams:
        """
        Returns the initialize params for the SourceKit-LSP Language Server.
        """
        initialize_params: InitializeParams = {  # type: ignore
            "processId": os.getpid(),
            "rootPath": repository_absolute_path,
            "rootUri": pathlib.Path(repository_absolute_path).as_uri(),
            "initializationOptions": {},
            "capabilities": {
                "workspace": {
                    "applyEdit": True,
                    "workspaceEdit": {"documentChanges": True},
                    "didChangeConfiguration": {"dynamicRegistration": True},
                    "didChangeWatchedFiles": {"dynamicRegistration": True},
                    "symbol": {
                        "dynamicRegistration": True,
                        "symbolKind": {
                            "valueSet": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26]
                        },
                    },
                    "executeCommand": {"dynamicRegistration": True},
                },
                "textDocument": {
                    "synchronization": {"dynamicRegistration": True, "willSave": True, "willSaveWaitUntil": True, "didSave": True},
                    "completion": {
                        "dynamicRegistration": True,
                        "contextSupport": True,
                        "completionItem": {
                            "snippetSupport": True,
                            "commitCharactersSupport": True,
                            "documentationFormat": ["markdown", "plaintext"],
                            "deprecatedSupport": True,
                            "preselectSupport": True,
                        },
                        "completionItemKind": {
                            "valueSet": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]
                        },
                    },
                    "hover": {"dynamicRegistration": True, "contentFormat": ["markdown", "plaintext"]},
                    "signatureHelp": {
                        "dynamicRegistration": True,
                        "signatureInformation": {
                            "documentationFormat": ["markdown", "plaintext"],
                            "parameterInformation": {"labelOffsetSupport": True},
                        },
                    },
                    "definition": {"dynamicRegistration": True},
                    "references": {"dynamicRegistration": True},
                    "documentHighlight": {"dynamicRegistration": True},
                    "documentSymbol": {
                        "dynamicRegistration": True,
                        "symbolKind": {
                            "valueSet": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26]
                        },
                        "hierarchicalDocumentSymbolSupport": True,
                    },
                    "codeAction": {
                        "dynamicRegistration": True,
                        "codeActionLiteralSupport": {
                            "codeActionKind": {
                                "valueSet": [
                                    "",
                                    "quickfix",
                                    "refactor",
                                    "refactor.extract",
                                    "refactor.inline",
                                    "refactor.rewrite",
                                    "source",
                                    "source.organizeImports",
                                ]
                            }
                        },
                    },
                    "codeLens": {"dynamicRegistration": True},
                    "formatting": {"dynamicRegistration": True},
                    "rangeFormatting": {"dynamicRegistration": True},
                    "onTypeFormatting": {"dynamicRegistration": True},
                    "rename": {"dynamicRegistration": True},
                    "publishDiagnostics": {"relatedInformation": True},
                },
            },
            "workspaceFolders": [
                {"uri": pathlib.Path(repository_absolute_path).as_uri(), "name": os.path.basename(repository_absolute_path)}
            ],
        }

        return initialize_params

    def _start_server(self):
        """
        Starts the SourceKit-LSP Language Server and waits for it to be ready.
        """

        def do_nothing(params):
            return

        def window_log_message(msg):
            """Monitor SourceKit-LSP log messages"""
            message_text = msg.get("message", "")
            self.logger.log(f"LSP: window/logMessage: {message_text}", logging.INFO)

        def check_server_status(params):
            """Check if server is ready"""
            self.server_ready.set()
            self.completions_available.set()

        # Set up notification handlers
        self.server.on_notification("window/logMessage", window_log_message)
        self.server.on_notification("$/progress", do_nothing)
        self.server.on_notification("textDocument/publishDiagnostics", do_nothing)
        self.server.on_notification("experimental/serverStatus", check_server_status)

        self.logger.log("Starting SourceKit-LSP server process", logging.INFO)
        self.server.start()

        # Send initialization request
        initialize_params = self._get_initialize_params(self.repository_root_path)

        self.logger.log(
            "Sending initialize request from LSP client to SourceKit-LSP server and awaiting response",
            logging.INFO,
        )
        init_response = self.server.send.initialize(initialize_params)
        self.logger.log(f"Received initialize response from SourceKit-LSP server: {init_response}", logging.INFO)

        # Verify that the server supports our required features
        assert "textDocumentSync" in init_response["capabilities"]
        # SourceKit-LSP doesn't explicitly advertise completionProvider in capabilities
        # but it does support completions through other mechanisms
        assert "definitionProvider" in init_response["capabilities"]

        # Complete the initialization handshake
        self.server.notify.initialized({})

        # Mark server as ready
        self.server_ready.set()
        self.completions_available.set()

        self.logger.log("SourceKit-LSP server ready", logging.INFO)
