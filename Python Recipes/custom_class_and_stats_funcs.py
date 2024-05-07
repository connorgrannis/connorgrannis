import numpy as np
import pandas as pd
from typing import List
import re
import statsmodels.api as sm
from statsmodels.formula.api import ols
from sklearn.feature_selection import chi2
from scipy import stats

pd.set_option('display.max_columns', 50)
pd.set_option('display.max_rows', 50)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', None)

class Xlator(dict):
    """ Pronounced translator. All-in-one multiple-string-substitution class """
    def _make_regex(self):
        """ Build re object based on the keys of the current dictionary """
        return re.compile("|".join(map(re.escape, self.keys())))
    def __call__(self, match):
        """ Handler invoked for each regex match """
        return self[match.group(0)]
    def xlat(self, text):
        """ Translate text, returns the modified text. """
        return self._make_regex().sub(self, text)


class OptimizedDataFrame(pd.DataFrame):
    def optimize_floats(self) -> pd.DataFrame:
        """ downcast float64 to as small as possible """
        floats = self.select_dtypes(include=['float64']).columns.tolist()
        self[floats] = self[floats].apply(pd.to_numeric, downcast='float')
        return self
    def optimize_ints(self) -> pd.DataFrame:
        """ downcast int64 to as small as possible """
        ints = self.select_dtypes(include=['int64']).columns.tolist()
        self[ints] = self[ints].apply(pd.to_numeric, downcast='integer')
        return self
    def optimize_objects(self, datetime_features: List[str]) -> pd.DataFrame:
        """ downcast objects like datetimes and characters to as small as possible """
        for col in self.select_dtypes(include=['object']):
            if col not in datetime_features:
                if not (type(self[col][0])==list):
                    num_unique_values = len(self[col].unique())
                    num_total_values = len(self[col])
                    if float(num_unique_values) / num_total_values < 0.5:
                        # get rid of hyphens
                        try:
                            self[col] = list(map(lambda x: Xlator({"-": " "}).xlat(x), self[col]))
                        except TypeError:
                            pass
                        self[col] = self[col].astype('category')
            else:
                self[col] = pd.to_datetime(self[col])
        return self
    def _optimize(self, datetime_features: List[str] = []) -> pd.DataFrame:
        """ optimize all columns """
        return self.optimize_floats().optimize_ints().optimize_objects(datetime_features)
    def optimize(self, datetime_features: List[str] = []) -> pd.DataFrame:
        """ optimize everything and report the memory reduction """
        orig_mem = self.memory_usage().sum()
        opt_df = self._optimize(datetime_features)
        opt_mem = opt_df.memory_usage().sum()
        print(f"Memory usage reduced by {round(((orig_mem-opt_mem)/orig_mem)*100, 2)}%")
        return opt_df
    def count_values_table(self, col):
        """ displays the value, count, and % of total """
        count_val = self[col].value_counts()
        count_val_percent = 100 * count_val / len(self[col])
        count_val_table = pd.concat([count_val, count_val_percent.round(2)], axis=1)
        count_val_table.reset_index(inplace=True)
        # reset the column names
        count_val_table.columns = range(count_val_table.columns.size)
        count_val_table_ren_columns = count_val_table.rename(
                            columns = {0: 'Value', 1 : 'Count Values', 2 : '% of Total Values'}
        )
        return count_val_table_ren_columns
    def missing_values_table(self):
        mis_val = self.isnull().sum()
        mis_val_percent = 100 * self.isnull().sum() / len(self)
        mis_val_table = pd.concat([mis_val, mis_val_percent], axis=1)
        mis_val_table_ren_columns = mis_val_table.rename(
        columns = {0 : 'Missing Values', 1 : '% of Total Values'})
        mis_val_table_ren_columns = mis_val_table_ren_columns[
            mis_val_table_ren_columns.iloc[:,1] != 0].sort_values(
        '% of Total Values', ascending=False).round(1)
        print ("Your selected dataframe has " + str(self.shape[1]) + " columns.\n"      
            "There are " + str(mis_val_table_ren_columns.shape[0]) +
            " columns that have missing values.")
        return mis_val_table_ren_columns
    def show_categorical_counts(self, cat_vars):
        print("Total Records:", self.shape[0], "- Value Counts per Categorical Attribute:\n")
        # todo: make a single dataframe with a multi-index
        for att in cat_vars:
            print(att)
            print((pd.DataFrame(self[att]
                                .value_counts(normalize = False, sort = True, ascending = False, bins = None, dropna = False))
                                .rename(columns={att:"Count"})
                    ))
            print("\n")

###### Testing
alc_log = pd.read_csv("/Users/connorgrannis/Documents/Programming/Cocktails/2024/2024_log.csv")
alc_log.head()

# optimize
alc_log = OptimizedDataFrame(alc_log).optimize("Date")

# test additional methods
alc_log.missing_values_table()
alc_log.count_values_table('Amount')
alc_log.count_values_table('DrinkType')

# show column dtypes
alc_log.dtypes
cat_vars = alc_log.select_dtypes('category').columns.to_list()
continuous_vars = ["Amount"]
ordinal_vars = "year", "month", "day", "hour", "minute", "week_of_year", "day_of_week"

alc_log.show_categorical_counts(cat_vars)


class Stats:
    def __init__(self, data_frame, categorical_variable, numerical_variable):
        self.data_frame = data_frame
        self.categorical_variable = categorical_variable
        self.numerical_variable = numerical_variable
    def chi_squared_test(self, alpha):
        # See: XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
        param_string = self.numerical_variable + " ~ " + self.categorical_variable
        model = ols(param_string, data=self.data_frame).fit()
        result = sm.stats.anova_lm(model, typ=2)
        #print(result)
        p_value = result.iat[0, 3]
        reject_h0 = (p_value < alpha)
        return p_value, reject_h0
    def t_test(self, alpha):
        # See: XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
        param_string = self.numerical_variable + " ~ " + self.categorical_variable
        model = ols(param_string, data=self.data_frame).fit()
        result = sm.stats.anova_lm(model, typ=2)
        #print(result)
        p_value = result.iat[0, 3]
        reject_h0 = (p_value < alpha)
        return p_value, reject_h0
    def anova_test(self, categorical_variable, numerical_variable, alpha):
        # See: XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
        param_string = numerical_variable + " ~ " + categorical_variable
        model = ols(param_string, data=self.data_frame).fit()
        result = sm.stats.anova_lm(model, typ=2)
        #print(result)
        p_value = result.iat[0, 3]
        reject_h0 = (p_value < alpha)
        return p_value, reject_h0
    


def anova_test(data_frame, categorical_variable, numerical_variable, alpha):
    # See: https://towardsdatascience.com/statistics-in-python-using-anova-for-feature-selection-b4dc876ef4f0
    param_string = numerical_variable + " ~ " + categorical_variable
    model = ols(param_string, data=data_frame).fit()
    result = sm.stats.anova_lm(model, typ=2)
    #print(result)
    p_value = result.iat[0, 3]
    reject_h0 = (p_value < alpha)
    return p_value, reject_h0

cat_att = "DrinkType"
alpha = 0.05

res_dict = {}
for idx, num_att in enumerate(continuous_vars):
    p_value, reject_h0 = anova_test(alc_log, cat_att, num_att, alpha)
    res_dict[idx] = {
        "P_Value": p_value, 
        "Reject_H0": reject_h0, 
        "Cat_Attribute": cat_att, 
        "Num_Attribute": num_att}

print(pd.DataFrame(res_dict).T
      [["P_Value", "Reject_H0", "Cat_Attribute", "Num_Attribute"]])

# ^^ Importing the packages within the function is giving different results than if it is loaded in the global space!!!!!
# I guess there's a random component during the initalization of the package? Weird that the results are consistent though... If the packages are loaded within the function I always get the same results. Same with global scope. They're just different from each other.
# let's plot a few graphs to see what we believe is the truth
# also looks like the differences are only with the ordinal variables.
    
# When imported within function
#   0.000000                  True            DrinkType               Amount
#   0.392019                 False            DrinkType                 year
#   0.022050                  True            DrinkType                month
#   0.095335                 False            DrinkType                  day
#   0.033859                  True            DrinkType                 hour
#   0.567045                 False            DrinkType               minute
#   0.028856                  True            DrinkType         week_of_year
#   0.156606                 False            DrinkType          day_of_week

# when imported in global space
#   0.000000                  True            DrinkType               Amount
#   0.000000                  True            DrinkType                 year
#   0.000000                  True            DrinkType                month
#   0.016744                  True            DrinkType                  day
#   0.000000                  True            DrinkType                 hour
#   0.000001                  True            DrinkType               minute
#   0.000000                  True            DrinkType         week_of_year
#   0.000002                  True            DrinkType          day_of_week

# import matplotlib.pyplot as plt
# import seaborn as sns

# sns.boxplot(x="DrinkType", y="Amount", data=alc_log_opt)
# sns.despine()
# plt.show()


############################### STILL CLEANING UP THE BELOW CODE ###############################


# stats doesn't really make sense until it's aggregated up
# Use Chi-Squared test to check for a relationship between all pairs of categorical variables.
def create_chi2_matrix(df):
    #See: https://medium.com/analytics-vidhya/constructing-heat-map-for-chi-square-test-of-independence-6d78aa2b140f
    column_names=df.columns # Assign column names to row indexs 
    chisqmatrix=pd.DataFrame(df,columns=column_names,index=column_names)
    # Set counters to zero
    outer_count=0
    inner_count=0
    for icol in column_names: # outer loop
        for jcol in column_names: # inner loop
            # Convert to cross tab - for Chi-square test, we have to first convert variables into contigency table
            mycrosstab=pd.crosstab(df[icol],df[jcol])
            #print(mycrosstab)
            # Get p-value and other information
            stat,p,dof,expected=stats.chi2_contingency(mycrosstab)
            #print("Details:",icol,jcol,stat,p,dof)
            # Rounding very small p-values to zero
            chisqmatrix.iloc[outer_count,inner_count]=round(p,10)
            # Expected frequencies should be at least 5 for the majority (80%) of the cells.
            # Check expected frequency of each group
            cntexpected=expected[expected<5].size
            # Getting percentage 
            perexpected=((expected.size-cntexpected)/expected.size)*100
            if perexpected<20:
                chisqmatrix.iloc[outer_count,inner_count]=2.00        # Assign 2 as a flag 
            if icol==jcol:
                chisqmatrix.iloc[outer_count,inner_count]=0.00
            inner_count=inner_count+1
        outer_count=outer_count+1
        inner_count=0
    return chisqmatrix

chi2matrix = create_chi2_matrix(data_df[categorical_attribute_names])
print(chi2matrix.head(999))


def find_outliers(df_in, att_name):
    quantile_low  = 0.25  # These are typical values, but you can set them as apropriate - see literature
    quantile_high = 0.75
    multiplier = 1.5
    
    Q1 = df_in[att_name].quantile(quantile_low)
    Q3 = df_in[att_name].quantile(quantile_high)
    IQR = Q3-Q1
    good_range_low  = Q1 - multiplier * IQR
    good_range_high = Q3 + multiplier * IQR
    
    outlier_list=((df_in[att_name] <= good_range_low) | (df_in[att_name] >= good_range_high)).tolist()
    outlier_indices=[i for i, x in enumerate(outlier_list) if x]

    if len(outlier_indices) > 0:
        outlier_value_list = []
        for i in outlier_indices:
            outlier_value_list.append( [i, df_in.iloc[i][att_name]] )
            
        from operator import itemgetter
        outlier_value_list = sorted(outlier_value_list, key=itemgetter(1), reverse=True)
        
        print("\nAttribute: [", att_name, "]   Good Range: [",good_range_low, ",", good_range_high, "]   Number of Outliers: [", len(outlier_indices),"]")
        print("Index           Value")
        for i in outlier_value_list:
            print("%5d      %10.3f" % (i[0], i[1]))

        plt.figure(figsize=(10,1))
        sns.boxplot(x=att_name, data=df_in)
        plt.show()
    
    return outlier_indices