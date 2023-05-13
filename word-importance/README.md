# Word Correlation and Feature Importance

&rarr; (1) [[Word Correlation Analysis](#word-correlation-analysis)] | (2) [[Word Importance Analysis](#word-importance-analysis)], [[Word frequency analysis](#word-frequency-analysis)] | (3) [[Cross-Validation and Hyper-Parameter Search](#cross-validation-and-hyper-parameter-search)]

## Run analysis and experiments

* Requires data from https://osf.io/dwnxt/?view_only=e75faa4f54244361aa198e257b4fecf9. Download and extract in current folder.
* Code requires Python 3.8.
* Requirements can be found in [`requirements.txt`](requirements.txt).
  * We use `spaCy` for POS (part-of-speech) tagging and filtering/cleaning (stopwords, non-words, etc.)
  * `numpy`, `pandas`, `scipy` for numerical computation
  * `scikit-learn` for model training
  * `matplotlib` for plotting figures
  * `jupyterlab` for Jupyter Notebooks with examples
* To run all: `python3 compute.py`
* [`compute.py`](compute.py) contains shared code used in all the notebooks to load and process data as well as some utility functions.

## Distribution of Scores and Quantiles

Notebook: [`WordFeature.ipynb`](WordFeature.ipynb)

The following figures show the distribution of scores for the documents for each category: _dominance_, _prestige_, _power_, and _workplace power_ (only study 2).
The vertical dashed lines represent the boundaries for the quantiles for low to mid and mid to high.

### Study 1

<details>
  <summary>Distribution of Scores and Quantiles</summary>

#### Dominance

Self vs. Judges

<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study1/distribution/quant-dominance.png?raw=true" title="Distribution and quantiles of scores (self-judged)" width="200">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study1/distribution/quant-dominance_f.png?raw=true" title="Distribution and quantiles of scores (judges)" width="200">

#### Power

Self vs. Judges

<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study1/distribution/quant-power.png?raw=true" title="Distribution and quantiles of scores (self-judged)" width="200">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study1/distribution/quant-power_f.png?raw=true" title="Distribution and quantiles of scores (judges)" width="200">

#### Prestige

Self vs. Judges

<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study1/distribution/quant-prestige.png?raw=true" title="Distribution and quantiles of scores (self-judged)" width="200">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study1/distribution/quant-prestige_f.png?raw=true" title="Distribution and quantiles of scores (judges)" width="200">

</details>

### Study 2

<details>
  <summary>Distribution of Scores and Quantiles</summary>

#### Dominance

Self vs. Judges

<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study2/distribution/quant-dominance.png?raw=true" title="Distribution and quantiles of scores (self-judged)" width="200">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study2/distribution/quant-dominance_f.png?raw=true" title="Distribution and quantiles of scores (judges)" width="200">

#### Power

Self vs. Judges

<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study2/distribution/quant-power.png?raw=true" title="Distribution and quantiles of scores (self-judged)" width="200">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study2/distribution/quant-power_f.png?raw=true" title="Distribution and quantiles of scores (judges)" width="200">

#### Prestige

Self vs. Judges

<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study2/distribution/quant-prestige.png?raw=true" title="Distribution and quantiles of scores (self-judged)" width="200">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study2/distribution/quant-prestige_f.png?raw=true" title="Distribution and quantiles of scores (judges)" width="200">

#### Workplace Power

Self vs. Judges

<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study2/distribution/quant-workplace_power.png?raw=true" title="Distribution and quantiles of scores (self-judged)" width="200">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study2/distribution/quant-workplace_power_f.png?raw=true" title="Distribution and quantiles of scores (judges)" width="200">

</details>


## Word frequency analysis

Notebook: [`WordFeature.ipynb`](WordFeature.ipynb)

Absolute word frequency values can be found in [`study1-output.xlsx`](study1-output.xlsx) and [`study2-output.xlsx`](study2-output.xlsx).

### Study 1

<details>
  <summary>Word frequency comparison between low / mid / high (quantile) scored descriptions</summary>

#### Domminance

<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study1/mid-low-high/words-dominance-by-pos-ADJ.png?raw=true" title="Word importance for Dominance for POS tag ADJ" width="400">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study1/mid-low-high/words-dominance-by-pos-ADV.png?raw=true" title="Word importance for Dominance for POS tag ADV" width="400">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study1/mid-low-high/words-dominance-by-pos-NOUN,PROPN.png?raw=true" title="Word importance for Dominance for POS tag NOUN and PROPN" width="400">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study1/mid-low-high/words-dominance-by-pos-VERB.png?raw=true" title="Word importance for Dominance for POS tag VERB" width="400">

#### Power

<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study1/mid-low-high/words-power-by-pos-ADJ.png?raw=true" title="Word importance for Power for POS tag ADJ" width="400">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study1/mid-low-high/words-power-by-pos-ADV.png?raw=true" title="Word importance for Power for POS tag ADV" width="400">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study1/mid-low-high/words-power-by-pos-NOUN,PROPN.png?raw=true" title="Word importance for Power for POS tag NOUN and PROPN" width="400">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study1/mid-low-high/words-power-by-pos-VERB.png?raw=true" title="Word importance for Power for POS tag VERB" width="400">

#### Prestige

<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study1/mid-low-high/words-prestige-by-pos-ADJ.png?raw=true" title="Word importance for Prestige for POS tag ADJ" width="400">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study1/mid-low-high/words-prestige-by-pos-ADV.png?raw=true" title="Word importance for Prestige for POS tag ADV" width="400">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study1/mid-low-high/words-prestige-by-pos-NOUN,PROPN.png?raw=true" title="Word importance for Prestige for POS tag NOUN and PROPN" width="400">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study1/mid-low-high/words-prestige-by-pos-VERB.png?raw=true" title="Word importance for Prestige for POS tag VERB" width="400">

</details>

<details>
  <summary>Word comparison between categories</summary>

<details>
  <summary>Low-Quantil Scores</summary>

##### Self-judged

<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study1/comparison/words-by-quant-0.0-0.3+pos-ADJ-for-power,dominance,prestige.png" width="24%">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study1/comparison/words-by-quant-0.0-0.3+pos-ADV-for-power,dominance,prestige.png" width="24%">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study1/comparison/words-by-quant-0.0-0.3+pos-NOUN,PROPN-for-power,dominance,prestige.png" width="24%">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study1/comparison/words-by-quant-0.0-0.3+pos-VERB-for-power,dominance,prestige.png" width="24%">

##### By judges

<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study1/comparison/words-by-quant-0.0-0.3+pos-ADJ-for-power_f,dominance_f,prestige_f.png" width="24%">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study1/comparison/words-by-quant-0.0-0.3+pos-ADV-for-power_f,dominance_f,prestige_f.png" width="24%">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study1/comparison/words-by-quant-0.0-0.3+pos-NOUN,PROPN-for-power_f,dominance_f,prestige_f.png" width="24%">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study1/comparison/words-by-quant-0.0-0.3+pos-VERB-for-power_f,dominance_f,prestige_f.png" width="24%">

</details>
<details>
  <summary>Mid-Quantil Scores</summary>

##### Self-judged

<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study1/comparison/words-by-quant-0.3-0.7+pos-ADJ-for-power,dominance,prestige.png" width="24%">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study1/comparison/words-by-quant-0.3-0.7+pos-ADV-for-power,dominance,prestige.png" width="24%">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study1/comparison/words-by-quant-0.3-0.7+pos-NOUN,PROPN-for-power,dominance,prestige.png" width="24%">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study1/comparison/words-by-quant-0.3-0.7+pos-VERB-for-power,dominance,prestige.png" width="24%">

##### By judges

<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study1/comparison/words-by-quant-0.3-0.7+pos-ADJ-for-power_f,dominance_f,prestige_f.png" width="24%">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study1/comparison/words-by-quant-0.3-0.7+pos-ADV-for-power_f,dominance_f,prestige_f.png" width="24%">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study1/comparison/words-by-quant-0.3-0.7+pos-NOUN,PROPN-for-power_f,dominance_f,prestige_f.png" width="24%">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study1/comparison/words-by-quant-0.3-0.7+pos-VERB-for-power_f,dominance_f,prestige_f.png" width="24%">

</details>
<details>
  <summary>High-Quantil Scores</summary>

##### Self-judged

<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study1/comparison/words-by-quant-0.7-1.0+pos-ADJ-for-power,dominance,prestige.png" width="24%">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study1/comparison/words-by-quant-0.7-1.0+pos-ADV-for-power,dominance,prestige.png" width="24%">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study1/comparison/words-by-quant-0.7-1.0+pos-NOUN,PROPN-for-power,dominance,prestige.png" width="24%">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study1/comparison/words-by-quant-0.7-1.0+pos-VERB-for-power,dominance,prestige.png" width="24%">

##### By judges

<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study1/comparison/words-by-quant-0.7-1.0+pos-ADJ-for-power_f,dominance_f,prestige_f.png" width="24%">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study1/comparison/words-by-quant-0.7-1.0+pos-ADV-for-power_f,dominance_f,prestige_f.png" width="24%">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study1/comparison/words-by-quant-0.7-1.0+pos-NOUN,PROPN-for-power_f,dominance_f,prestige_f.png" width="24%">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study1/comparison/words-by-quant-0.7-1.0+pos-VERB-for-power_f,dominance_f,prestige_f.png" width="24%">

</details>

</details>

<details>
  <summary>Word comparison between self-judged and judges</summary>

<details>
  <summary>Low-Quantil Scores</summary>

##### ADJ: adjective

<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study1/comparison/words-by-quant-0.0-0.3+pos-ADJ-for-dominance,dominance_f.png" width="400">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study1/comparison/words-by-quant-0.0-0.3+pos-ADJ-for-power,power_f.png" width="400">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study1/comparison/words-by-quant-0.0-0.3+pos-ADJ-for-prestige,prestige_f.png" width="400">

##### ADV: adverb

<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study1/comparison/words-by-quant-0.0-0.3+pos-ADV-for-dominance,dominance_f.png" width="400">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study1/comparison/words-by-quant-0.0-0.3+pos-ADV-for-power,power_f.png" width="400">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study1/comparison/words-by-quant-0.0-0.3+pos-ADV-for-prestige,prestige_f.png" width="400">

##### NOUN: noun / PROPN: proper noun

<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study1/comparison/words-by-quant-0.0-0.3+pos-NOUN,PROPN-for-dominance,dominance_f.png" width="400">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study1/comparison/words-by-quant-0.0-0.3+pos-NOUN,PROPN-for-power,power_f.png" width="400">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study1/comparison/words-by-quant-0.0-0.3+pos-NOUN,PROPN-for-prestige,prestige_f.png" width="400">

##### VERB: verb

<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study1/comparison/words-by-quant-0.0-0.3+pos-VERB-for-dominance,dominance_f.png" width="400">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study1/comparison/words-by-quant-0.0-0.3+pos-VERB-for-power,power_f.png" width="400">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study1/comparison/words-by-quant-0.0-0.3+pos-VERB-for-prestige,prestige_f.png" width="400">

</details>

<details>
  <summary>Mid-Quantil Scores</summary>

##### ADJ: adjective

<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study1/comparison/words-by-quant-0.3-0.7+pos-ADJ-for-dominance,dominance_f.png" width="400">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study1/comparison/words-by-quant-0.3-0.7+pos-ADJ-for-power,power_f.png" width="400">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study1/comparison/words-by-quant-0.3-0.7+pos-ADJ-for-prestige,prestige_f.png" width="400">

##### ADV: adverb

<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study1/comparison/words-by-quant-0.3-0.7+pos-ADV-for-dominance,dominance_f.png" width="400">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study1/comparison/words-by-quant-0.3-0.7+pos-ADV-for-power,power_f.png" width="400">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study1/comparison/words-by-quant-0.3-0.7+pos-ADV-for-prestige,prestige_f.png" width="400">

##### NOUN: noun / PROPN: proper noun

<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study1/comparison/words-by-quant-0.3-0.7+pos-NOUN,PROPN-for-dominance,dominance_f.png" width="400">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study1/comparison/words-by-quant-0.3-0.7+pos-NOUN,PROPN-for-power,power_f.png" width="400">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study1/comparison/words-by-quant-0.3-0.7+pos-NOUN,PROPN-for-prestige,prestige_f.png" width="400">

##### VERB: verb

<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study1/comparison/words-by-quant-0.3-0.7+pos-VERB-for-dominance,dominance_f.png" width="400">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study1/comparison/words-by-quant-0.3-0.7+pos-VERB-for-power,power_f.png" width="400">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study1/comparison/words-by-quant-0.3-0.7+pos-VERB-for-prestige,prestige_f.png" width="400">

</details>

<details>
  <summary>High-Quantil Scores</summary>

##### ADJ: adjective

<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study1/comparison/words-by-quant-0.7-1.0+pos-ADJ-for-dominance,dominance_f.png" width="400">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study1/comparison/words-by-quant-0.7-1.0+pos-ADJ-for-power,power_f.png" width="400">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study1/comparison/words-by-quant-0.7-1.0+pos-ADJ-for-prestige,prestige_f.png" width="400">

##### ADV: adverb

<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study1/comparison/words-by-quant-0.7-1.0+pos-ADV-for-dominance,dominance_f.png" width="400">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study1/comparison/words-by-quant-0.7-1.0+pos-ADV-for-power,power_f.png" width="400">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study1/comparison/words-by-quant-0.7-1.0+pos-ADV-for-prestige,prestige_f.png" width="400">

##### NOUN: noun / PROPN: proper noun

<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study1/comparison/words-by-quant-0.7-1.0+pos-NOUN,PROPN-for-dominance,dominance_f.png" width="400">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study1/comparison/words-by-quant-0.7-1.0+pos-NOUN,PROPN-for-power,power_f.png" width="400">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study1/comparison/words-by-quant-0.7-1.0+pos-NOUN,PROPN-for-prestige,prestige_f.png" width="400">

##### VERB: verb

<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study1/comparison/words-by-quant-0.7-1.0+pos-VERB-for-dominance,dominance_f.png" width="400">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study1/comparison/words-by-quant-0.7-1.0+pos-VERB-for-power,power_f.png" width="400">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study1/comparison/words-by-quant-0.7-1.0+pos-VERB-for-prestige,prestige_f.png" width="400">

</details>

</details>

### Study 2

<details>
  <summary>Word frequency comparison between low / mid / high (quantile) scored descriptions</summary>

#### Domminance

<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study2/mid-low-high/words-dominance-by-pos-ADJ.png?raw=true" title="Word importance for Dominance for POS tag ADJ" width="400">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study2/mid-low-high/words-dominance-by-pos-ADV.png?raw=true" title="Word importance for Dominance for POS tag ADV" width="400">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study2/mid-low-high/words-dominance-by-pos-NOUN,PROPN.png?raw=true" title="Word importance for Dominance for POS tag NOUN and PROPN" width="400">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study2/mid-low-high/words-dominance-by-pos-VERB.png?raw=true" title="Word importance for Dominance for POS tag VERB" width="400">

#### Power

<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study2/mid-low-high/words-power-by-pos-ADJ.png?raw=true" title="Word importance for Power for POS tag ADJ" width="400">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study2/mid-low-high/words-power-by-pos-ADV.png?raw=true" title="Word importance for Power for POS tag ADV" width="400">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study2/mid-low-high/words-power-by-pos-NOUN,PROPN.png?raw=true" title="Word importance for Power for POS tag NOUN and PROPN" width="400">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study2/mid-low-high/words-power-by-pos-VERB.png?raw=true" title="Word importance for Power for POS tag VERB" width="400">

#### Prestige

<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study2/mid-low-high/words-prestige-by-pos-ADJ.png?raw=true" title="Word importance for Prestige for POS tag ADJ" width="400">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study2/mid-low-high/words-prestige-by-pos-ADV.png?raw=true" title="Word importance for Prestige for POS tag ADV" width="400">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study2/mid-low-high/words-prestige-by-pos-NOUN,PROPN.png?raw=true" title="Word importance for Prestige for POS tag NOUN and PROPN" width="400">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study2/mid-low-high/words-prestige-by-pos-VERB.png?raw=true" title="Word importance for Prestige for POS tag VERB" width="400">

#### Workplace Power

<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study2/mid-low-high/words-workplace_power-by-pos-ADJ.png?raw=true" title="Word importance for Workplace Power for POS tag ADJ" width="400">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study2/mid-low-high/words-workplace_power-by-pos-ADV.png?raw=true" title="Word importance for Workplace Power for POS tag ADV" width="400">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study2/mid-low-high/words-workplace_power-by-pos-NOUN,PROPN.png?raw=true" title="Word importance for Workplace Power for POS tag NOUN and PROPN" width="400">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study2/mid-low-high/words-workplace_power-by-pos-VERB.png?raw=true" title="Word importance for Workplace Power for POS tag VERB" width="400">

</details>

<details>
  <summary>Word comparison between categories</summary>

<details>
  <summary>Low-Quantil Scores</summary>

##### Self-judged

<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study2/comparison/words-by-quant-0.0-0.3+pos-ADJ-for-power,dominance,prestige,workplace_power.png" width="24%">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study2/comparison/words-by-quant-0.0-0.3+pos-ADV-for-power,dominance,prestige,workplace_power.png" width="24%">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study2/comparison/words-by-quant-0.0-0.3+pos-NOUN,PROPN-for-power,dominance,prestige,workplace_power.png" width="24%">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study2/comparison/words-by-quant-0.0-0.3+pos-VERB-for-power,dominance,prestige,workplace_power.png" width="24%">

##### By judges

<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study2/comparison/words-by-quant-0.0-0.3+pos-ADJ-for-power_f,dominance_f,prestige_f,workplace_power_f.png" width="24%">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study2/comparison/words-by-quant-0.0-0.3+pos-ADV-for-power_f,dominance_f,prestige_f,workplace_power_f.png" width="24%">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study2/comparison/words-by-quant-0.0-0.3+pos-NOUN,PROPN-for-power_f,dominance_f,prestige_f,workplace_power_f.png" width="24%">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study2/comparison/words-by-quant-0.0-0.3+pos-VERB-for-power_f,dominance_f,prestige_f,workplace_power_f.png" width="24%">

</details>
<details>
  <summary>Mid-Quantil Scores</summary>

##### Self-judged

<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study2/comparison/words-by-quant-0.3-0.7+pos-ADJ-for-power,dominance,prestige,workplace_power.png" width="24%">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study2/comparison/words-by-quant-0.3-0.7+pos-ADV-for-power,dominance,prestige,workplace_power.png" width="24%">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study2/comparison/words-by-quant-0.3-0.7+pos-NOUN,PROPN-for-power,dominance,prestige,workplace_power.png" width="24%">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study2/comparison/words-by-quant-0.3-0.7+pos-VERB-for-power,dominance,prestige,workplace_power.png" width="24%">

##### By judges

<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study2/comparison/words-by-quant-0.3-0.7+pos-ADJ-for-power_f,dominance_f,prestige_f,workplace_power_f.png" width="24%">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study2/comparison/words-by-quant-0.3-0.7+pos-ADV-for-power_f,dominance_f,prestige_f,workplace_power_f.png" width="24%">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study2/comparison/words-by-quant-0.3-0.7+pos-NOUN,PROPN-for-power_f,dominance_f,prestige_f,workplace_power_f.png" width="24%">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study2/comparison/words-by-quant-0.3-0.7+pos-VERB-for-power_f,dominance_f,prestige_f,workplace_power_f.png" width="24%">

</details>
<details>
  <summary>High-Quantil Scores</summary>

##### Self-judged

<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study2/comparison/words-by-quant-0.7-1.0+pos-ADJ-for-power,dominance,prestige,workplace_power.png" width="24%">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study2/comparison/words-by-quant-0.7-1.0+pos-ADV-for-power,dominance,prestige,workplace_power.png" width="24%">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study2/comparison/words-by-quant-0.7-1.0+pos-NOUN,PROPN-for-power,dominance,prestige,workplace_power.png" width="24%">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study2/comparison/words-by-quant-0.7-1.0+pos-VERB-for-power,dominance,prestige,workplace_power.png" width="24%">

##### By judges

<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study2/comparison/words-by-quant-0.7-1.0+pos-ADJ-for-power_f,dominance_f,prestige_f,workplace_power_f.png" width="24%">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study2/comparison/words-by-quant-0.7-1.0+pos-ADV-for-power_f,dominance_f,prestige_f,workplace_power_f.png" width="24%">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study2/comparison/words-by-quant-0.7-1.0+pos-NOUN,PROPN-for-power_f,dominance_f,prestige_f,workplace_power_f.png" width="24%">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study2/comparison/words-by-quant-0.7-1.0+pos-VERB-for-power_f,dominance_f,prestige_f,workplace_power_f.png" width="24%">

</details>

</details>

<details>
  <summary>Word comparison between self-judged and judges</summary>

<details>
  <summary>Low-Quantil Scores</summary>

##### ADJ: adjective

<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study2/comparison/words-by-quant-0.0-0.3+pos-ADJ-for-dominance,dominance_f.png" width="400">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study2/comparison/words-by-quant-0.0-0.3+pos-ADJ-for-power,power_f.png" width="400">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study2/comparison/words-by-quant-0.0-0.3+pos-ADJ-for-prestige,prestige_f.png" width="400">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study2/comparison/words-by-quant-0.0-0.3+pos-ADJ-for-workplace_power,workplace_power_f.png" width="400">

##### ADV: adverb

<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study2/comparison/words-by-quant-0.0-0.3+pos-ADV-for-dominance,dominance_f.png" width="400">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study2/comparison/words-by-quant-0.0-0.3+pos-ADV-for-power,power_f.png" width="400">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study2/comparison/words-by-quant-0.0-0.3+pos-ADV-for-prestige,prestige_f.png" width="400">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study2/comparison/words-by-quant-0.0-0.3+pos-ADV-for-workplace_power,workplace_power_f.png" width="400">

##### NOUN: noun / PROPN: proper noun

<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study2/comparison/words-by-quant-0.0-0.3+pos-NOUN,PROPN-for-dominance,dominance_f.png" width="400">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study2/comparison/words-by-quant-0.0-0.3+pos-NOUN,PROPN-for-power,power_f.png" width="400">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study2/comparison/words-by-quant-0.0-0.3+pos-NOUN,PROPN-for-prestige,prestige_f.png" width="400">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study2/comparison/words-by-quant-0.0-0.3+pos-NOUN,PROPN-for-workplace_power,workplace_power_f.png" width="400">

##### VERB: verb

<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study2/comparison/words-by-quant-0.0-0.3+pos-VERB-for-dominance,dominance_f.png" width="400">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study2/comparison/words-by-quant-0.0-0.3+pos-VERB-for-power,power_f.png" width="400">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study2/comparison/words-by-quant-0.0-0.3+pos-VERB-for-prestige,prestige_f.png" width="400">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study2/comparison/words-by-quant-0.0-0.3+pos-VERB-for-workplace_power,workplace_power_f.png" width="400">

</details>

<details>
  <summary>Mid-Quantil Scores</summary>

##### ADJ: adjective

<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study2/comparison/words-by-quant-0.3-0.7+pos-ADJ-for-dominance,dominance_f.png" width="400">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study2/comparison/words-by-quant-0.3-0.7+pos-ADJ-for-power,power_f.png" width="400">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study2/comparison/words-by-quant-0.3-0.7+pos-ADJ-for-prestige,prestige_f.png" width="400">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study2/comparison/words-by-quant-0.3-0.7+pos-ADJ-for-workplace_power,workplace_power_f.png" width="400">

##### ADV: adverb

<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study2/comparison/words-by-quant-0.3-0.7+pos-ADV-for-dominance,dominance_f.png" width="400">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study2/comparison/words-by-quant-0.3-0.7+pos-ADV-for-power,power_f.png" width="400">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study2/comparison/words-by-quant-0.3-0.7+pos-ADV-for-prestige,prestige_f.png" width="400">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study2/comparison/words-by-quant-0.3-0.7+pos-ADV-for-workplace_power,workplace_power_f.png" width="400">

##### NOUN: noun / PROPN: proper noun

<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study2/comparison/words-by-quant-0.3-0.7+pos-NOUN,PROPN-for-dominance,dominance_f.png" width="400">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study2/comparison/words-by-quant-0.3-0.7+pos-NOUN,PROPN-for-power,power_f.png" width="400">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study2/comparison/words-by-quant-0.3-0.7+pos-NOUN,PROPN-for-prestige,prestige_f.png" width="400">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study2/comparison/words-by-quant-0.3-0.7+pos-NOUN,PROPN-for-workplace_power,workplace_power_f.png" width="400">

##### VERB: verb

<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study2/comparison/words-by-quant-0.3-0.7+pos-VERB-for-dominance,dominance_f.png" width="400">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study2/comparison/words-by-quant-0.3-0.7+pos-VERB-for-power,power_f.png" width="400">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study2/comparison/words-by-quant-0.3-0.7+pos-VERB-for-prestige,prestige_f.png" width="400">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study2/comparison/words-by-quant-0.3-0.7+pos-VERB-for-workplace_power,workplace_power_f.png" width="400">

</details>

<details>
  <summary>High-Quantil Scores</summary>

##### ADJ: adjective

<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study2/comparison/words-by-quant-0.7-1.0+pos-ADJ-for-dominance,dominance_f.png" width="400">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study2/comparison/words-by-quant-0.7-1.0+pos-ADJ-for-power,power_f.png" width="400">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study2/comparison/words-by-quant-0.7-1.0+pos-ADJ-for-prestige,prestige_f.png" width="400">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study2/comparison/words-by-quant-0.7-1.0+pos-ADJ-for-workplace_power,workplace_power_f.png" width="400">

##### ADV: adverb

<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study2/comparison/words-by-quant-0.7-1.0+pos-ADV-for-dominance,dominance_f.png" width="400">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study2/comparison/words-by-quant-0.7-1.0+pos-ADV-for-power,power_f.png" width="400">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study2/comparison/words-by-quant-0.7-1.0+pos-ADV-for-prestige,prestige_f.png" width="400">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study2/comparison/words-by-quant-0.7-1.0+pos-ADV-for-workplace_power,workplace_power_f.png" width="400">

##### NOUN: noun / PROPN: proper noun

<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study2/comparison/words-by-quant-0.7-1.0+pos-NOUN,PROPN-for-dominance,dominance_f.png" width="400">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study2/comparison/words-by-quant-0.7-1.0+pos-NOUN,PROPN-for-power,power_f.png" width="400">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study2/comparison/words-by-quant-0.7-1.0+pos-NOUN,PROPN-for-prestige,prestige_f.png" width="400">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study2/comparison/words-by-quant-0.7-1.0+pos-NOUN,PROPN-for-workplace_power,workplace_power_f.png" width="400">

##### VERB: verb

<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study2/comparison/words-by-quant-0.7-1.0+pos-VERB-for-dominance,dominance_f.png" width="400">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study2/comparison/words-by-quant-0.7-1.0+pos-VERB-for-power,power_f.png" width="400">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study2/comparison/words-by-quant-0.7-1.0+pos-VERB-for-prestige,prestige_f.png" width="400">
<img src="https://github.com/Querela/Language-of-Power/blob/main/word-importance/figures_study2/comparison/words-by-quant-0.7-1.0+pos-VERB-for-workplace_power,workplace_power_f.png" width="400">

</details>

</details>


## Word Correlation Analysis

Notebook: [`WordCorrelation.ipynb`](WordCorrelation.ipynb)

We correlate each word (of each description,) with each hierarchy variable _dominance_, _power_, _prestige_, and _workplace_power_ (only study 2) based on the document scores and the relative word frequencies.

The final correlation scores are in the Excel documents [`study1-corrs.xlsx`](study1-corrs.xlsx) and [`study2-corrs.xlsx`](study2-corrs.xlsx). We truncated to the top-20 words (10 each for highest positive and negative values).
Besides relative word frequencies (TF), we also included a variant using TF-IDF which lowers the importance of words appearing across all documents.

## Word Importance Analysis

Notebook: [`WordFeature.ipynb`](WordFeature.ipynb)

We compute **word importance scores** by training a [_logistic regression_ model](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html#sklearn.linear_model.LogisticRegression) and extracting the model coefficients as scores.

As input features, we compute the [TF-IDF word-document matrix](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfTransformer.html). E.g., we compute word frequencies per document and performing some averaging. _Optional: filtering by part-of-speech word category is also possible but we included all words besides stop words._
The document scores (by judges or self-judged) for _dominance_, _power_, _prestige_, and _workplace_power_ (only study 2) are the target values for our model. The scores are being transformed to classes (1, 2, ..., 7) by rounding, and the model has to predict those classes from the input features.
We train a model for each of the three (four) categories (_dominance_, ...).

From the trained model, we extract the coefficients for each input feature (word) for each score class. We aggregate the coefficients over all the classes by summing the scaled coefficients, i.e. coefficients for low document scores (e.g. 1, 2, ...) are weighted more negatively in the calculation, while high scores (..., 6, 7) are weighted more positively. This results in strong coefficients for low document scores being overall negativ while strong coefficients for high document scores are overall positiv.
We finally scale the coefficients to the interval of `[-1, 1]` to obtain our word scores.

The final word scores are in the Excel documents [`study1-coefs.xlsx`](study1-coefs.xlsx) and [`study2-coefs.xlsx`](study2-coefs.xlsx) as well as results for lemmatized words. _We performed some filtering to limit the results using a minimum threshold for the importance score and a restriction of `30` features per category. We ranked them by importance. Both positive and negative features are included. (It is possible to have no strong positive or negative features, so only one of both would be shown but we added the condition to include both._

## Cross-Validation and Hyper-Parameter Search

Notebook: [`CrossValidation.ipynb`](CrossValidation.ipynb)

Performing nested cross-validation and hyper-parameter search over study data to find best model to predict target hierarchy variables.

Various runs were performed:
- using data from either _Study 1_, _Study 2_ or both
- with features from _DTM_ (document-term-matrix using TF-IDF), _LIWC_ or both (as well as scaled variants)
- with target variables being either continuous (regression models) or categorical (classes 1..7 or low/mid/high by quantiles; classification models).

Results are stored in [`results-crossvalidation.xlsx`](results-crossvalidation.xlsx).
