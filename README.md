# Course project "LLM for IDE Plugins"

The main purpose of that work was to create a plugin for [Visual Studio Code](https://code.visualstudio.com/).

The plugin was created to automate the writing of certain parts of code. 
Specifically, we highlighted the following challenges:

* Function docstring generation.
* UnitTest generation
* Semantic analysis of variables based on certain code snippets.
* AI code autocomplete 

# LLM part

Our main goal was a creation and fine-tuning a model for the IDE plugin.

## Dataset:

We created a dataset with 10000 function examples based on data from open GitHub 
repos. Also, we used CodeLLama 3 70b Instruct for the generation synthetic data(docstrings, UnitTests, semantic senses)
that we used for fine-tune and scoring results.

## Baselines:

As a baseline, we choose two models: CodeLlama2 7B Instruct and Microsoft Phi-3 mini with 
general prompts.


## Scoring methods:

We used CodeLLama 3 70b Instruct for scoring responses in our models - we asked model to 
score response by criterion with few shot examples.


## Results:


| Model                          | Docstring | Test generation | Semantic sense |
|--------------------------------|-----------|-----------------|----------------|
| Average Human                  | 0.46      | -               | -              |
| CodeLlama3 Instruct 70b        | 0.995     | 0.82            | 0.992          |
| microsoft/phi-3-mini finetuned | 0.87      | 0.69            | 0.91           |
| microsoft/phi-3-mini           | 0.75      | 0.55            | 0.77           |
| microsoft/phi-2                | 0.55      | 0.42            | 0.63           |
| CodeLlama-Python-7B            | 0.56      | 0.47            | 0.67           |
| Stable Code 3b                 | 0.34      | 0.52            | 0.41           |


# Demo:

![](https://github.com/GrigoriyPA/LLM-extension/demo.gif)