import * as vscode from "vscode";

import * as vscodelc from "vscode-languageclient/node";

import { serverOptions } from "./server_utils";

import { logEntry } from "../logger";

import { LogLevel, Components } from "../../config";

export let languageClient: vscodelc.LanguageClient;

function createOptions(): vscodelc.LanguageClientOptions {
    return {
        documentSelector: [{ scheme: "file", language: "python" }],
        synchronize: {
            fileEvents: vscode.workspace.createFileSystemWatcher("**/.py"),
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
    } catch (exception) {
        logEntry(
            LogLevel.ALERT,
            Components.EXTENSION,
            `Failed to create language client: ${exception}`
        );
    }

    return languageClient
        .start()
        .then(() => {
            logEntry(
                LogLevel.INFO,
                Components.EXTENSION,
                "Language client connected to Jedi LS"
            );
        })
        .catch((error) => {
            logEntry(
                LogLevel.ALERT,
                Components.EXTENSION,
                `Failed to connect language client to Jedi LS: ${error}`
            );
        });
}
