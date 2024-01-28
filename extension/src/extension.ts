import * as vscode from 'vscode';

import {
    HoverRequest,
    Hover,
    Position,
    TextDocumentIdentifier,
    LanguageClient,
    LanguageClientOptions,
    HoverParams,
    MarkupContent
} from 'vscode-languageclient/node';

import {
    printToExtentionChannel,
    initializeExtention
} from './utils/extention_utils';

import {
    initializeServer,
    serverProcess
} from './utils/server_utils';


let client: LanguageClient;


export async function activate(context: vscode.ExtensionContext) {
    initializeExtention();
    await initializeServer();

    const clientOptions: LanguageClientOptions = {
        documentSelector: [{ scheme: 'file', language: 'python' }],
        synchronize: {
            fileEvents: vscode.workspace.createFileSystemWatcher('**/.py')
        }
    };

    try {
        client = new LanguageClient(
            'llmLanguageServer',
            'LLM language server',
            serverProcess.options,
            clientOptions
        );

        await client.start();
        printToExtentionChannel(`Connected to Jedi LS`);
    } catch (e) {
        printToExtentionChannel(`Failed to connect language client to Jedi LS:\n${e}`);
    }

    let disposable = vscode.commands.registerTextEditorCommand('llm-extension.documentFunction', async (textEditor: vscode.TextEditor, edit: vscode.TextEditorEdit) => {
        const position: vscode.Position = textEditor.selection.active;
        const range = textEditor.document.getWordRangeAtPosition(position);
        const world = textEditor.document.getText(range);
        
        let params: HoverParams = {
            textDocument: TextDocumentIdentifier.create(textEditor.document.uri.toString()),
            position: Position.create(position.line, position.character)
        };

        const response: Hover = await client.sendRequest(HoverRequest.method, params);
        if (response !== null) {
            const content = response.contents as MarkupContent;
            printToExtentionChannel(`Hover content:\n${content.value}`);
        }

        textEditor.edit((edit: vscode.TextEditorEdit) => {
            edit.insert(position, "Test insert content");
        });

        vscode.window.showInformationMessage(`Hello World from LLM-extension! Current world: ${world}`);
    });

    context.subscriptions.push(disposable);
}

export function deactivate() {
    if (serverProcess) {
        serverProcess.stop();
    }
    if (!client) {
        return undefined;
    }
    return client.stop();
}
