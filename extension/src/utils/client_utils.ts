import * as vscode from 'vscode';

import {
    LanguageClient,
    LanguageClientOptions
} from 'vscode-languageclient/node';

import { printToExtentionChannel } from './extention_utils';

import { serverProcess } from './server_utils';


export let languageClient: LanguageClient;


function createOptions(): LanguageClientOptions {
    return {
        documentSelector: [{ scheme: 'file', language: 'python' }],
        synchronize: {
            fileEvents: vscode.workspace.createFileSystemWatcher('**/.py')
        }
    };
}

export async function initializeLanguageClient() {
    printToExtentionChannel(`Initialization of language client`);

    try {
        languageClient = new LanguageClient(
            'llmExtentionLanguageClient',
            'LLM extention language client',
            serverProcess.options,
            createOptions()
        );

        await languageClient.start();
        printToExtentionChannel(`Language client connected to Jedi LS`);
    } catch (exception) {
        printToExtentionChannel(`Failed to connect language client to Jedi LS: ${exception}`);
    }
}
