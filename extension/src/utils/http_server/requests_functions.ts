import { RequestsBase, ResponseBase } from "./requests_structures";

import { LogLevel, Components, logEntry } from "../logger";

function logMessage(logLevel: LogLevel, functionName: string, message: string) {
    logEntry(logLevel, Components.HTTP_GATEWAY, `[${functionName}] ${message}`);
}

export async function sendRequest(
    request: RequestsBase.RequestInterface
): Promise<ResponseBase.HttpResponse> {
    logMessage(LogLevel.DEBUG, "SendRequest", `${request.getName()}`);
    logMessage(
        LogLevel.TRACE,
        "SendRequest",
        `Request description:\n${request.getDescription()}`
    );

    // TODO: @dffTu implement request sending and error message passing
    // TODO: @ganvas show status bar when we wait for http response
    const response = new ResponseBase.HttpResponse(
        `Test response for request ${request.getName()}`
    );
    response.setSuccess();

    logMessage(LogLevel.TRACE, "SendRequest", `Request successfully finished`);

    return response;
}
