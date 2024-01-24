import { exec } from 'child_process';
import { text } from 'stream/consumers';

import * as vscode from 'vscode';

export async function activate(context: vscode.ExtensionContext) {
    vscode.languages.registerCompletionItemProvider('python', {
        provideCompletionItems(document: vscode.TextDocument, position: vscode.Position, token: vscode.CancellationToken, context: vscode.CompletionContext) {
            const complitionItem = new vscode.CompletionItem(
                'MyCompletionItem',
                vscode.CompletionItemKind.User
            );
            return [complitionItem];
        }
    });

    vscode.languages.registerHoverProvider('python', {
        async provideHover(document: vscode.TextDocument, position: vscode.Position, token: vscode.CancellationToken) {
            const range = document.getWordRangeAtPosition(position);
            const word = document.getText(range);
            const { stdout } = exec(`python -c "print(${word}.__doc__)"`);

            if (stdout === null) {
                throw new Error('Could not fetch hover data');
            }

            return {
                contents: [await text(stdout)]
            };
        }
    });

    let disposable = vscode.commands.registerCommand('llm-extension.helloWorld', () => {
        vscode.window.showInformationMessage('Hello World from LLM-extension!');
    });

    context.subscriptions.push(disposable);
}

export function deactivate() {}
