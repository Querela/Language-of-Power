# Language of Power - Experiments

## Word Frequency, Word Importance Analysis and Word--Hierarchy Variable Correlation

See folder [`word-importance`](word-importance).
* A lot of figures.
* Document score distribution per category and quantils for low/mid/high score ranges.
* Word frequency comparisons between categories, part-of-speech tags, etc.
* Word importance calculation. E.g., which word contributes how much for high-power descriptions.
* Word rank analysis and split-half correlation for reliability estimation of data.
* Correlation between words and hierarchy variables (_power_, _dominance_, _prestige_).

## Other experiments

See notebooks in folder [`notebooks`](notebooks).
* Topic modelling with LDA and HDP. Visualization using `pyLDAvis`. Some word clouds.
* Assign LWIC-unknown words to existing [LWIC](https://www.liwc.app/) categories based on semantic similarity using [FastText](https://fasttext.cc/) word embedding.
* Using SentenceTransformer and [SetFit](https://github.com/huggingface/setfit) for few-shot learning. E.g., predict category scores with scarce training data.
* Regression modelling to predict category scores.
