import * as vscode from "vscode";

import { initializeHttpGateway } from "./utils/http_server/http_gateway";

import {
    initializeLanguageClient,
    languageClient,
} from "./utils/runtime/client_utils";

import { initializeExtention } from "./utils/runtime/extention_utils";

import { LogLevel } from "./utils/logger";

export async function activate(context: vscode.ExtensionContext) {
    initializeExtention(context, LogLevel.TRACE);

    return Promise.all([initializeLanguageClient(), initializeHttpGateway()]);
}

export async function deactivate() {
    if (!languageClient) {
        return undefined;
    }
    return languageClient.stop();
}
