# Unit 11—Risky Business

## Background
<br>
Auto loans, mortgages, student loans, debt consolidation ... these are just a few examples of credit and loans that people are seeking online. Peer-to-peer lending services such as LendingClub or Prosper allow investors to loan other people money without the use of a bank. However, investors always want to mitigate risk, so you have been asked by a client to help them use machine learning techniques to predict credit risk.

In this assignment, you will build and evaluate several machine-learning models to predict credit risk using free data from LendingClub. Credit risk is an inherently imbalanced classification problem (the number of good loans is much larger than the number of at-risk loans), so you will need to employ different techniques for training and evaluating models with imbalanced classes. You will use the imbalanced-learn and Scikit-learn libraries to build and evaluate models using the two following techniques:

<br>

## Resampling

<br>

### Notes
* Models are biased toward the majority class. Thus, evaluation metrics, such as accuracty, can be misleading.
* Strategies to deal with imbalanced classes:
    * Oversampling and undersampling
    * Use of right performance metrics for evaluation
    * Change model
* Oversampling
    * Random oversampling
    * SMOTE (Synthetic Minority Oversampling Technique)
* Undersampling
    * Random undersampling
    * Cluster centroid: 
        * Create n clusters 
        * n = num minority class training instances
        * take centroids from clusters as majority class training data

<br>

### Results

<br>

| Strategy              | Bal Acc Score | Avg Pre   | Avg Rec   | Geo Mean  |
| --------------------- | ------------- | --------- | --------- | --------- |
| Random oversample     | 0.6579        | 0.99      | 0.61      | 0.66      |
| SMOTE                 | 0.6619        | 0.99      | 0.69      | 0.66      |
| Cluster centroids     | 0.5443        | 0.99      | 0.42      | 0.53      |
| SMOTEEN               | 0.6435        | 0.99      | 0.58      | 0.64      |

<br>

### Questions and Answers

* <strong>Question:</strong> Which model had the best balanced accuracy score?
* <strong>Answer:</strong> SMOTE had the best balanced accuracy score by slim margin.

<br>

* <strong>Question:</strong> Which model had the best recall score?
* <strong>Answer:</strong> SMOTE also had the best avg recall score.

<br>

* <strong>Question:</strong> Which model had the best geometric mean score?
* <strong>Answer:</strong> SMOTE tied random oversampling for best geometric mean score.

<br>