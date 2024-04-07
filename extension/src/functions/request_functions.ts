import * as vscode from "vscode";

import {
    findSymbolContentRange,
    findSymbolReferencesContent,
} from "./find_functions";

import { RequestsBase } from "../utils/http_server/requests_structures";

import { SymbolKind } from "../utils/lsp/lsp_helpers";

export async function buildRequestWithSymbolContex(
    document: vscode.TextDocument,
    position: vscode.Position,
    targetSymbol: SymbolKind
): Promise<RequestsBase.RequestWithSymbolContextBase | undefined> {
    const symbolContentRange = await findSymbolContentRange(
        document,
        position,
        targetSymbol
    );
    if (symbolContentRange === undefined) {
        return undefined;
    }

    const symbolReferencesContent = await findSymbolReferencesContent(
        document,
        position
    );

    return new RequestsBase.RequestWithSymbolContextBase(
        document.getText(symbolContentRange),
        symbolReferencesContent
    );
}
