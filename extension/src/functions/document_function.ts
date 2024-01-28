import * as vscode from 'vscode';

import {
    Position,
    TextDocumentIdentifier,

    MarkupContent,

    HoverParams,
    HoverRequest,
    Hover
} from 'vscode-languageclient/node';

import { printToExtentionChannel } from '../utils/extention_utils';

import { languageClient } from '../utils/client_utils';


export const documentFunction = async (textEditor: vscode.TextEditor, edit: vscode.TextEditorEdit) => {
    const position: vscode.Position = textEditor.selection.active;
    const range = textEditor.document.getWordRangeAtPosition(position);
    const world = textEditor.document.getText(range);

    let params: HoverParams = {
        textDocument: TextDocumentIdentifier.create(textEditor.document.uri.toString()),
        position: Position.create(position.line, position.character)
    };

    const response: Hover = await languageClient.sendRequest(HoverRequest.method, params);
    if (response !== null) {
        const content = response.contents as MarkupContent;
        printToExtentionChannel(`Hover content:\n${content.value}`);
    }

    textEditor.edit((edit: vscode.TextEditorEdit) => {
        edit.insert(position, "Test insert content");
    });

    vscode.window.showInformationMessage(`Hello World from LLM-extension! Current world: ${world}`);
};
