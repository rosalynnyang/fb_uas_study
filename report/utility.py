import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency
from IPython.display import display, Markdown
import rpy2.robjects.numpy2ri
from rpy2.robjects.packages import importr
rpy2.robjects.numpy2ri.activate()
stats = importr('stats')

# function for creating crosstabs and producing chisq test results
def crosstab_chisq(catvar1, catvar2, df, col_names=None, title=None):
    """
    This function helps calculate and display crosstab tables as well as
    chi-square test statistics (p-values) examining associations between two
    categorial variables.
    """
    if title is None:
        display(Markdown(f"#### Crosstab of {catvar1} and {catvar2}"))
    else:
        display(Markdown(f"{title}"))
    
    ct= pd.crosstab(df[catvar1], df[catvar2])
    cross_idx = ct.index.values
    ct.loc['Total n'] = 0
    for idx in cross_idx:
        ct.loc['Total n'] += ct.loc[idx]
    for idx in cross_idx:
        ct.loc[idx] = ((ct.loc[idx] / ct.loc['Total n']) * 100).apply(lambda x: f"{x:,.1f}")
    ct.loc['Total n'] = ct.loc['Total n'].apply(lambda x: f"{int(x):,}")
    if col_names is not None:
        ct.columns = col_names
    display(ct)

    chi2, p, dof, ex = chi2_contingency(pd.crosstab(df[catvar1], df[catvar2]))
    display(Markdown(f"*Chi-squared statistic = {chi2.round(1)}, degree of freedom = {dof}, p = {p.round(3)}*"))
    
    display(Markdown("-----"))


    
# function for frequency table of a single column: percentages and total
def freq_percent_table(catvar, df):
    #display(Markdown(f"#### Percentage distribution of {catvar}"))
    ct = pd.DataFrame(df[catvar].value_counts().sort_index())
    cross_idx = ct.index.values
    ct.loc['Total n'] = 0
    for idx in cross_idx:
        ct.loc['Total n'] += ct.loc[idx]
    for idx in cross_idx:
        ct.loc[idx] = ((ct.loc[idx] / ct.loc['Total n']) * 100).apply(lambda x: f"{x:,.1f}")
    ct.loc['Total n'] = ct.loc['Total n'].apply(lambda x: f"{int(x):,}")
    #display(ct)
    #display(Markdown("-----"))
    return ct
    
    
    
# function for weighted frequency table of a single column: percentages and total
def weighted_freq_percent_table(catvar, weightvar, df):
    #display(Markdown(f"#### Weighted percentage distribution of {catvar}"))
    ct = df[[weightvar, catvar]].groupby([catvar]).sum()
    cross_idx = ct.index.values
    ct.loc['Total n'] = 0
    for idx in cross_idx:
        ct.loc['Total n'] += ct.loc[idx]
    for idx in cross_idx:
        ct.loc[idx] = ((ct.loc[idx] / ct.loc['Total n']) * 100).apply(lambda x: f"{x:,.1f}")
    #display(ct)
    #display(Markdown("-----"))
    return ct



def create_comparison_tables(fb_dataframe, uas_dataframe, fb_cols, uas_cols):
    fb_freq = {}
    fb_freq_r = {}
    uas_freq = {}
    uas_freq_r = {}
    uas_freq_w = {}
    comparison_tables = {}
    # unweighted fb
    for col in fb_cols:
        fb_freq[col] = freq_percent_table(col, fb_dataframe)
    # raked fb
    for col in fb_cols:
        fb_freq_r[col] = weighted_freq_percent_table(col, 'weight', fb_dataframe)
    # unweighted uas
    for col in uas_cols:
        uas_freq[col] = freq_percent_table(col, uas_dataframe)
     # raked uas
    for col in uas_cols:
        uas_freq_r[col] = weighted_freq_percent_table(col, 'weight', uas_dataframe)
     # weighted uas
    for col in uas_cols:
        uas_freq_w[col] = weighted_freq_percent_table(col, 'final_weight', uas_dataframe)
    # create comparison tables
    for fb_col, uas_col in zip(fb_cols, uas_cols):
        temp_df = pd.concat([fb_freq[fb_col], fb_freq_r[fb_col], uas_freq[uas_col], uas_freq_r[uas_col], uas_freq_w[uas_col]],  axis=1, ignore_index=True)
        temp_df.columns = ['FB unweighted (%)', 'FB raked (%)', 'UAS unweighted (%)', 'UAS raked (%)', 'UAS originally weighted (%)']
        comparison_tables[fb_col] = temp_df
    # display
    for fb_col in fb_cols:
        display(Markdown(f"#### Comparing unweighted and weighted estimates of {fb_col}"))
        display(comparison_tables[fb_col])
        

# this function uses R stats package to calculate Fisher's exact test
def fishers_p(catvar1, catvar2, df):
    crosstab = pd.crosstab(df[catvar1], df[catvar2])
    res = stats.fisher_test(crosstab.values, workspace = 2e9)
    p = res[0][0]
    return p


# function for creating percent crosstabs only
def crosstab_percent_table(catvar1, catvar2, df, col_order, chisq_test=False):
    ct= pd.crosstab(df[catvar1], df[catvar2]).reindex(col_order, axis="columns")
    cross_idx = ct.index.values
    ct.loc['Total n'] = 0
    for idx in cross_idx:
        ct.loc['Total n'] += ct.loc[idx]
    for idx in cross_idx:
        ct.loc[idx] = ((ct.loc[idx] / ct.loc['Total n']) * 100).apply(lambda x: f"{x:,.1f}")
    ct.loc['Total n'] = ct.loc['Total n'].apply(lambda x: f"{int(x):,}")
    display(ct)
    if chisq_test is True:
        chi2, p, dof, ex = chi2_contingency(pd.crosstab(df[catvar1], df[catvar2]))
        display(f"*Chi-squared statistic = {chi2.round(1)}, degree of freedom = {dof}, p = {p.round(3)}*")