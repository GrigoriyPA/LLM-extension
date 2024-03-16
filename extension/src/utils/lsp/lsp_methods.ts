import * as vscode from "vscode";

import * as vscodelc from "vscode-languageclient/node";

import { FromVscode } from "./lsp_helpers";

import { languageClient } from "../runtime/client_utils";

export async function getSymbolsInformation(
    document: vscode.TextDocument
): Promise<vscodelc.DocumentSymbol[] | undefined> {
    let params: vscodelc.DocumentSymbolParams = {
        textDocument: FromVscode.getTextDocumentIdentifier(document),
    };

    const response = await languageClient.sendRequest(
        vscodelc.DocumentSymbolRequest.method,
        params
    );

    if (!response) {
        return undefined;
    }

    return response as vscodelc.DocumentSymbol[];
}

export async function getReferences(
    document: vscode.TextDocument,
    position: vscode.Position,
    includeDeclaration: boolean
): Promise<vscodelc.Location[] | undefined> {
    let params: vscodelc.ReferenceParams = {
        textDocument: FromVscode.getTextDocumentIdentifier(document),
        position: FromVscode.getPosition(position),
        context: {
            includeDeclaration: includeDeclaration,
        },
    };

    const response = await languageClient.sendRequest(
        vscodelc.ReferencesRequest.method,
        params
    );

    if (!response) {
        return undefined;
    }

    return response as vscodelc.Location[];
}
