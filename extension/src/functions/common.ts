import * as vscode from "vscode";

import * as vscodelc from "vscode-languageclient/node";

import { FromVscodelc } from "../utils/lsp/lsp_helpers";

export function findSymbolDescription(
    documentSymbols: vscodelc.DocumentSymbol[] | undefined,
    wordRange: vscode.Range
): vscodelc.DocumentSymbol | undefined {
    if (documentSymbols === undefined) {
        return undefined;
    }

    for (const documentSymbol of documentSymbols) {
        const isFinction =
            documentSymbol.kind === vscodelc.SymbolKind.Function ||
            documentSymbol.kind === vscodelc.SymbolKind.Method;

        const isTargetRange = wordRange.isEqual(
            FromVscodelc.getRange(documentSymbol.selectionRange)
        );

        if (isFinction && isTargetRange) {
            return documentSymbol;
        }

        const result = findSymbolDescription(
            documentSymbol.children,
            wordRange
        );
        if (result !== undefined) {
            return result;
        }
    }

    return undefined;
}
