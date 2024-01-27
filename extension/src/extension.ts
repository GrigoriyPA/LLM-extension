import { exec } from 'child_process';
import net from 'node:net';

import * as vscode from 'vscode';

import {
    HoverRequest,
    Hover,
    Position,
    TextDocumentIdentifier,
    LanguageClient,
    LanguageClientOptions,
    StreamInfo,
    HoverParams,
    MarkupContent
} from 'vscode-languageclient/node';

import {
    printToExtentionChannel,
    initializeExtention
} from './utils/extention_utils';


let client: LanguageClient;


export async function activate(context: vscode.ExtensionContext) {
    initializeExtention();

    const serverConnectionInfo = { port: 8089, host: "127.0.0.1" };

    const serverOptions = () => {
        let socket = net.connect(serverConnectionInfo);
        let result: StreamInfo = {
            writer: socket,
            reader: socket
        };
        return Promise.resolve(result);
    };

    const clientOptions: LanguageClientOptions = {
        documentSelector: [{ scheme: 'file', language: 'python' }],
        synchronize: {
            fileEvents: vscode.workspace.createFileSystemWatcher('**/.py')
        },
        middleware: {
            provideCompletionItem: async (document, position, context, token, next) => {
                const result = await next(document, position, context, token);
                const completionList = result as vscode.CompletionList;
                const stats: Map<string, number> = new Map();
                completionList.items.forEach(item => {
                    if (!item.kind) {
                        return;
                    }

                    let current_value = stats.get(vscode.CompletionItemKind[item.kind]) || 0;
                    stats.set(
                        vscode.CompletionItemKind[item.kind],
                        ++current_value
                    );
                });

                for (let entry of stats.entries()) {
                    printToExtentionChannel(`${entry[0]}: ${entry[1]}`);
                }
                
                return result;
            },
        }
    };

    try {
        client = new LanguageClient(
            'llmLanguageServer',
            'LLM language server',
            serverOptions,
            clientOptions
        );

        client.start();
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
    if (!client) {
        return undefined;
    }
    return client.stop();
}
