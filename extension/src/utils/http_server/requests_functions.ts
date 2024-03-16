import { RequestInterface, HttpResponse } from "./requests_structures";

import { LogLevel, Components, logEntry } from "../logger";

function logMessage(logLevel: LogLevel, functionName: string, message: string) {
    logEntry(logLevel, Components.HTTP_GATEWAY, `[${functionName}] ${message}`);
}

export async function sendRequest(
    request: RequestInterface
): Promise<HttpResponse> {
    logMessage(LogLevel.DEBUG, "SendRequest", `${request.name}`);
    logMessage(
        LogLevel.TRACE,
        "SendRequest",
        `Request description:\n${request.getDescription()}`
    );

    // TODO: @dffTu implement request sending
    const response = new HttpResponse("Test function documentation");
    response.setSuccess();

    logMessage(LogLevel.TRACE, "SendRequest", `Request successfully finished`);

    return response;
}
