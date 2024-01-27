import net from 'node:net';

import * as vscode from 'vscode';
import {
    LanguageClient,
    LanguageClientOptions,
    StreamInfo
} from 'vscode-languageclient/node';

let client: LanguageClient;

export async function activate(context: vscode.ExtensionContext) {
    let outputChannel = vscode.window.createOutputChannel("LLM python extension");
    outputChannel.appendLine(`Initialization of LLM Python extension`);

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
                    outputChannel.appendLine(`${entry[0]}: ${entry[1]}`);
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
        outputChannel.appendLine(`Connected to Jedi LS`);
    } catch (e) {
        outputChannel.appendLine(`Failed to connect language client to Jedi LS:\n${e}`);
    }

    let disposable = vscode.commands.registerCommand('llm-extension.helloWorld', () => {
        vscode.window.showInformationMessage('Hello World from LLM-extension!');
    });

    context.subscriptions.push(disposable);
}

export function deactivate() {
    if (!client) {
        return undefined;
    }
    return client.stop();
}
