import * as vscode from "vscode";

import { initializeExtention } from "./utils/extention_utils";

import { initializeLanguageClient, languageClient } from "./utils/client_utils";

import { documentFunction } from "./functions/document_function";

export async function activate(context: vscode.ExtensionContext) {
    initializeExtention();
    await initializeLanguageClient();

    context.subscriptions.push(
        vscode.commands.registerTextEditorCommand(
            "llm-extension.documentFunction",
            documentFunction
        )
    );
}

export function deactivate() {
    if (!languageClient) {
        return undefined;
    }
    return languageClient.stop();
}
