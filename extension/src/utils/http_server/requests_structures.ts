export namespace DocumentFunction {
    export interface Request {
        FunctionContent: String;
        ReferencesContent: String[];
    }

    export interface Response {
        FunctionDocumention: String;
    }
}
