LAB5_HINT_POLICY = {
    "explainer": {
        "classification": {
            1: "Explain what the dataset seems to be about. Explain what info() and describe() reveal in general terms.",
            2: "Draw attention to 1–2 important aspects: e.g. class imbalance, weird encodings, potential data quality issues.",
            3: "Suggest specific checks (e.g. “compute target class distribution”, “check outliers in age or BMI”) but no code."
        },
        "confusion_matrix": {
            1: "Explain accuracy, precision, recall, F1 in plain language. Explain the confusion matrix structure (TP, FP, FN, TN).",
            2: "Point out problems with using only accuracy in an imbalanced dataset.",
            3: "Suggest an extra diagnostic (e.g. check recall for the positive class, or class specific metrics) and explain why. "
        },
        "plots": {
            1: "Explain what ROC curve represents and what AUC means. ",
            2: "Indicate when ROC vs PR is more useful (e.g. for imbalanced data).",
            3: "Suggest an interpretation in words for this particular model (but not writing the full exam-style answer)."
        },
        "regression": {
            1: "Explain what the target is, and which columns are likely predictors.",
            2: "Highlight potential non-linear relationships or problematic features (e.g., extreme values, skewed cost distribution). ",
            3: "Suggest which transformations or features might be worth exploring (e.g., log(cost)) without giving exact code."
        },
        "regression_metrics": {
            1: "Explain each metric (MAE, MSE, RMSE, R²) in plain language. ",
            2: "Explain trade-offs (e.g., why MAE vs RMSE) and what a particular R² means for this model. ",
            3: "Suggest additional checks (e.g., residual plots, checking for heteroscedasticity) conceptually. "
        },
        "residual": {
            1: "Explain what residuals are and what we look for in residual plots. ",
            2: "Identify patterns that suggest problems (e.g., funnel shape, non-linearity) in general.",
            3: "Suggest conceptual remedies (“maybe model is too simple”, “consider feature transformations”) without code."
        }
    },

    "debugger": {
        "classification": {
            1: "Ask the student reflective questions to help them reason about their pipeline. For example, ask on which dataset they are evaluating the model (training or test), and whether the target column might accidentally be included among the feature variables.",
            2: "Guide the student to inspect the relevant parts of their code. Suggest checking where train_test_split is called, verifying how X and y were defined, and confirming that the target column was not dropped or mistakenly included as a feature.",
            3: "Point to the likely conceptual issue without giving code. For example, explain that the model should be trained on the training set and evaluated on the test set, and that features should not include the target variable."
        },
        "confusion_matrix": {
            1: "Ask the student whether the confusion matrix is computed using predicted class labels or probabilities, and whether it is evaluated on the correct dataset.",
            2: "Encourage the student to inspect which variables are passed to the confusion matrix function. Suggest checking whether the predictions come from predict() rather than probability outputs.",
            3: "Explain the conceptual correction: a confusion matrix should compare the true labels with predicted class labels (for example y_test and predicted labels). If probabilities were used instead, the student should convert them to class predictions first."
        },
        "plots": {
            1: "Ask the student what type of prediction values they are using to construct the ROC curve and whether they correspond to probabilities or class labels.",
            2: "Suggest inspecting the part of the pipeline where prediction probabilities are generated and verifying which variables are used for the ROC computation.",
            3: "Explain conceptually that ROC curves should be based on probability scores or decision scores from the classifier rather than discrete predicted labels."
        },
        "regression": {
            1: "Ask the student what type of prediction problem they are solving and whether the target variable is continuous or categorical.",
            2: "Encourage the student to inspect which evaluation metric they used and whether it is appropriate for regression tasks.",
            3: "Explain that regression models should be evaluated with metrics designed for continuous targets (such as MAE, RMSE, or R²) rather than classification metrics like accuracy or confusion matrices."
        },
        "regression_metrics": {
            1: "Ask the student what the metric is intended to measure and which variables they are comparing.",
            2: "Suggest checking which values are passed into the metric function and verifying that they correspond to the true values and predicted values from the test dataset.",
            3: "Explain conceptually that regression metrics should compare the true target values and model predictions from the test set (for example y_test and predicted values)."
        },
        "residual": {
            1: "Ask the student how they computed the residuals and which variables they subtracted.",
            2: "Encourage the student to inspect whether the shapes of the predicted and true values match and whether they originate from the same dataset split.",
            3: "Explain that residuals represent the difference between the true values and predicted values. If residuals were computed using mismatched variables or shapes, the calculation should be corrected conceptually."
        }
    }
}
