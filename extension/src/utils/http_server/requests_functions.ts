import { printToExtentionChannel } from "../runtime/extention_utils";

import { DocumentFunction } from "./requests_structures";

export async function documentFunctionRequest(
    request: DocumentFunction.Request
): Promise<DocumentFunction.Response | undefined> {
    printToExtentionChannel(
        `documentFunctionRequest, function content:\n${request.FunctionContent}`
    );
    for (const reference of request.ReferencesContent) {
        printToExtentionChannel(`Reference content:\n${reference}`);
    }
    printToExtentionChannel(`Request end.`);

    return {
        FunctionDocumention: "Test function documentation",
    };
}
