export function sleep(ms: number) {
    return new Promise((resolve) => setTimeout(resolve, ms));
}

export function applyIndent(indent: number, text: string): string {
    const textIndent = " ".repeat(indent);

    let resultText = "";
    for (const textLine of text.split("\n")) {
        resultText += textIndent + textLine + "\n";
    }

    return resultText;
}
