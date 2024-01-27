import net from 'node:net';

import * as vscode from 'vscode';
import {
    LanguageClient,
    LanguageClientOptions,
    StreamInfo
} from 'vscode-languageclient/node';

export async function activate(context: vscode.ExtensionContext) {
    const outputChannel = vscode.window.createOutputChannel("LLM python extension");
    outputChannel.appendLine(`Initialization of LLM Python extension`);

    const serverConnectionInfo = { port: 8089, host: "127.0.0.1" };

    const serverOptions = () => {
        const socket = net.connect(serverConnectionInfo);
        const result: StreamInfo = {
            writer: socket,
            reader: socket
        };
        return Promise.resolve(result);
    };

    const clientOptions: LanguageClientOptions = {
        documentSelector: [{ scheme: 'file', language: 'python' }],
        synchronize: {
            fileEvents: vscode.workspace.createFileSystemWatcher('**/.py')
        }
    };

    try {
        const client = new LanguageClient(
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

export function deactivate() {}
