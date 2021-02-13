# Unit 11—Risky Business

## Background
<br>
Auto loans, mortgages, student loans, debt consolidation ... these are just a few examples of credit and loans that people are seeking online. Peer-to-peer lending services such as LendingClub or Prosper allow investors to loan other people money without the use of a bank. However, investors always want to mitigate risk, so you have been asked by a client to help them use machine learning techniques to predict credit risk.

In this assignment, you will build and evaluate several machine-learning models to predict credit risk using free data from LendingClub. Credit risk is an inherently imbalanced classification problem (the number of good loans is much larger than the number of at-risk loans), so you will need to employ different techniques for training and evaluating models with imbalanced classes. You will use the imbalanced-learn and Scikit-learn libraries to build and evaluate models using the two following techniques:

<br>

## Resampling

<br>

### Files
[Resampling Analysis Notebook](credit_risk_resampling.ipynb)

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
| Random oversample     | 0.8325        | 0.99      | 0.84      | 0.83      |
| SMOTE                 | 0.8388        | 0.99      | 0.87      | 0.84      |
| Cluster centroids     | 0.8215        | 0.99      | 0.76      | 0.82      |
| SMOTEEN               | 0.8388        | 0.99      | 0.86      | 0.84      |

<br>

### Questions and Answers

* <strong>Question:</strong> Which model had the best balanced accuracy score?
* <strong>Answer:</strong> SMOTE and SMOTEEN have top balanced accuracy score, only slightly higher than random oversampling. Cluster centroids not far behind.

<br>

* <strong>Question:</strong> Which model had the best recall score?
* <strong>Answer:</strong> SMOTE had the best avg recall score.

<br>

* <strong>Question:</strong> Which model had the best geometric mean score?
* <strong>Answer:</strong> SMOTE and SMOTEEN tie for best geometric mean score.

<br>

## Ensemble Learning

<br>

### Files
[Ensemble Learning Analysis Notebook](credit_risk_ensemble.ipynb)

<br>

### Notes

<br>

### Questions and Answers

* <strong>Question:</strong> Which model had the best balanced accuracy score?
* <strong>Answer:</strong> 

<br>

* <strong>Question:</strong> Which model had the best recall score?
* <strong>Answer:</strong> 

<br>

* <strong>Question:</strong> Which model had the best geometric mean score?
* <strong>Answer:</strong> 

<br>

* <strong>Question:</strong> What are the top three features?
* <strong>Answer:</strong> 

<br>