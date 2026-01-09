LAB3_HINT_POLICY = {
    "explainer": {
        "info": {
            1: "Explain what information df.info() provides at a high level.",
            2: "Explain how data types and non-null counts affect later analysis.",
            3: "Explain how df.info() can reveal potential data quality issues, without naming them."
        },
        "missing": {
            1: "Explain why missing data matters conceptually.",
            2: "Explain common strategies to reason about missing data patterns.",
            3: "Explain how missing data decisions affect downstream statistics."
        },
        "outliers": {
            1: "Explain what outliers are and why they matter.",
            2: "Explain how to reason about whether detected outliers are plausible.",
            3: "Explain how outlier treatment can influence correlations and tests."
        },
        "correlation": {
            1: "Explain what correlation measures conceptually.",
            2: "Explain how to interpret strength and direction of relationships.",
            3: "Explain common pitfalls in interpreting correlations."
        },
        "chi_square": {
            1: "Explain the purpose of chi-square and Fisher tests.",
            2: "Explain what the test compares conceptually.",
            3: "Explain how to interpret significance without stating outcomes."
        }
    },

    "debugger": {
        "info": {
            1: "Ask what stands out in the df.info() output.",
            2: "Ask which columns might cause issues later and why.",
            3: "Ask how the structure could influence preprocessing choices."
        },
        "missing": {
            1: "Ask where missing values appear.",
            2: "Ask whether missingness seems systematic.",
            3: "Ask how different handling choices could change results."
        },
        "outliers": {
            1: "Ask which values were flagged as outliers.",
            2: "Ask whether those values seem realistic in context.",
            3: "Ask what would change if those points were kept or removed."
        },
        "correlation": {
            1: "Ask which variables appear related.",
            2: "Ask whether any relationships are surprising.",
            3: "Ask what other factors might explain the observed relationships."
        },
        "chi_square": {
            1: "Ask what hypothesis the test is evaluating.",
            2: "Ask how the observed and expected values differ.",
            3: "Ask what the result implies for independence, without stating it."
        }
    }
}
