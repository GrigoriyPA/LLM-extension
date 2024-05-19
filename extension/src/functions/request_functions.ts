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
    const symbolContentRange = findSymbolContentRange(
        document,
        position,
        targetSymbol
    );
    const symbolReferencesContent = findSymbolReferencesContent(
        document,
        position
    );

    return Promise.all([symbolContentRange, symbolReferencesContent]).then(
        (result) => {
            if (
                result[0] === undefined ||
                result[1] === undefined ||
                result[1].length === 0
            ) {
                return undefined;
            }

            return new RequestsBase.RequestWithSymbolContextBase(
                document.getText(result[0]),
                result[1]
            );
        }
    );
}
