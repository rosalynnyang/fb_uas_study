import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency
from IPython.display import display, Markdown

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