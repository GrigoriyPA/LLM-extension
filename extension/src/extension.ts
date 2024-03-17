import * as vscode from "vscode";

import { documentFunction } from "./functions/document_function";
import { generateTests } from "./functions/generate_tests";
import { nameSuggestion } from "./functions/name_suggestion";
import { semanticAnalysisOfSymbol } from "./functions/semantic_analysis_of_symbol";

import { initializeHttpGateway } from "./utils/http_server/http_gateway";

import {
    initializeLanguageClient,
    languageClient,
} from "./utils/runtime/client_utils";

import { initializeExtention } from "./utils/runtime/extention_utils";

import { LogLevel } from "./utils/logger";

export async function activate(context: vscode.ExtensionContext) {
    initializeExtention(LogLevel.TRACE);
    await initializeLanguageClient();
    await initializeHttpGateway();

    context.subscriptions.push(
        vscode.commands.registerTextEditorCommand(
            "llm-extension.documentFunction",
            documentFunction
        )
    );
    context.subscriptions.push(
        vscode.commands.registerTextEditorCommand(
            "llm-extension.generateTests",
            generateTests
        )
    );
    context.subscriptions.push(
        vscode.commands.registerTextEditorCommand(
            "llm-extension.nameSuggestion",
            nameSuggestion
        )
    );
    context.subscriptions.push(
        vscode.commands.registerTextEditorCommand(
            "llm-extension.semanticAnalysisOfSymbol",
            semanticAnalysisOfSymbol
        )
    );
}

export function deactivate() {
    if (!languageClient) {
        return undefined;
    }
    return languageClient.stop();
}
