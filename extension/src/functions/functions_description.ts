import { documentFunction } from "./handlers/document_function";
import { generateTests } from "./handlers/generate_tests";
import { nameSuggestion } from "./handlers/name_suggestion";
import { semanticAnalysisOfSymbol } from "./handlers/semantic_analysis_of_symbol";

export const supportedFunctions = new Map([
    ["documentFunction", documentFunction],
    ["generateTests", generateTests],
    ["nameSuggestion", nameSuggestion],
    ["semanticAnalysisOfSymbol", semanticAnalysisOfSymbol],
]);
