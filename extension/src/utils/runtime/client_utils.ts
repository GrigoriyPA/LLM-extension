import * as vscode from "vscode";

import * as vscodelc from "vscode-languageclient/node";

import { completionSuggestion } from "../../functions/completion_suggestion";

import { LogLevel, Components, logEntry } from "../logger";

import { serverOptions } from "./server_utils";

export let languageClient: vscodelc.LanguageClient;

function createOptions(): vscodelc.LanguageClientOptions {
    return {
        documentSelector: [{ scheme: "file", language: "python" }],
        synchronize: {
            fileEvents: vscode.workspace.createFileSystemWatcher("**/.py"),
        },
        middleware: {
            provideCompletionItem: completionSuggestion,
        },
    };
}

export async function initializeLanguageClient() {
    logEntry(
        LogLevel.INFO,
        Components.EXTENSION,
        "Initialization of language client"
    );

    try {
        languageClient = new vscodelc.LanguageClient(
            "llmExtentionLanguageClient",
            "LLM extention language client",
            serverOptions,
            createOptions()
        );

        await languageClient.start();
        logEntry(
            LogLevel.INFO,
            Components.EXTENSION,
            "Language client connected to Jedi LS"
        );
    } catch (exception) {
        logEntry(
            LogLevel.ALERT,
            Components.EXTENSION,
            `Failed to connect language client to Jedi LS: ${exception}`
        );
    }
}
