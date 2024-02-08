import * as vscode from "vscode";

import * as vscodelc from "vscode-languageclient/node";

import { printToExtentionChannel } from "../utils/extention_utils";

import { languageClient } from "../utils/client_utils";

export const documentFunction = async (
    textEditor: vscode.TextEditor,
    edit: vscode.TextEditorEdit
) => {
    const position: vscode.Position = textEditor.selection.active;
    const range = textEditor.document.getWordRangeAtPosition(position);
    const world = textEditor.document.getText(range);

    let params: vscodelc.HoverParams = {
        textDocument: vscodelc.TextDocumentIdentifier.create(
            textEditor.document.uri.toString()
        ),
        position: vscodelc.Position.create(position.line, position.character),
    };

    const response: vscodelc.Hover = await languageClient.sendRequest(
        vscodelc.HoverRequest.method,
        params
    );
    if (response !== null) {
        const content = response.contents as vscodelc.MarkupContent;
        printToExtentionChannel(`Hover content:\n${content.value}`);
    }

    textEditor.edit((edit: vscode.TextEditorEdit) => {
        edit.insert(position, "Test insert content");
    });

    vscode.window.showInformationMessage(
        `Hello World from LLM-extension! Current world: ${world}`
    );
};
