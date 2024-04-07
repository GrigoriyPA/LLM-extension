import * as vscode from "vscode";

import { initializeHttpGateway } from "./utils/http_server/requests_functions";

import {
    initializeLanguageClient,
    languageClient,
} from "./utils/runtime/client_utils";

import { initializeExtention } from "./utils/runtime/extention_utils";

export async function activate(context: vscode.ExtensionContext) {
    initializeExtention(context);

    return Promise.all([initializeLanguageClient(), initializeHttpGateway()]);
}

export async function deactivate() {
    if (!languageClient) {
        return undefined;
    }
    return languageClient.stop();
}
