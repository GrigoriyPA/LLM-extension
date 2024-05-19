export enum LogLevel {
    CRIT, // Extention level fatal errors
    ERROR, // Request level fatal errors
    WARNING, // Exceptional situations that are guaranteed not to lead to an error
    INFO, // Information about the progress of request computing, only a few messages during the processing of a single request
    DEBUG, // Information about the progress of function execution, only a few messages during the processing of a single function
    TRACE, // Detail information about the progress of function execution, regular messages during the processing of a single function
}

export enum Components {
    REQUESTS_PROCESSOR,
    HTTP_GATEWAY,
    EXTENSION,
}

class ExtensionConfig {
    defaultLogLevel = LogLevel.TRACE;
    componentsLogLevel = new Map<Components, LogLevel>();

    llmServerUrl: string = "http://51.250.77.98";

    symbolContentRangeSize: number = 5;
}

export const extensionConfig = new ExtensionConfig();
