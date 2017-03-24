import csv
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
import pandas as pd

def extract_speed_dating_data():
    """
    Convert the "Speed Dating Data" csv file into a dictionary based on 
    columns_needed. The keys in the dictionary are the row numbers of the csv. 
    Each key's value is a dictionary. This nested dictionary has columns 
    (from columns_needed)of the csv as the keys, and the element in the columns 
    as the values.
    
    Return:
        rows_dict: dictionary of dictionaries
    """ 
    # create a new csv file to read from, with only values in columns_wanted as 
    # columns in the new file
    df = pd.read_csv("Speed Dating Data.csv")
    columns_needed = ['pid', 'income', 'age','attr1_1','career_c','pf_o_amb',\
    'amb3_1','shar1_1','pf_o_att','pf_o_sha','intel1_1','match','pf_o_int',\
    'pf_o_sin','intel3_1','wave','iid','sinc3_1','amb1_1','sinc1_1','go_out',\
    'gender','fun1_1','pf_o_fun','attr3_1', 'fun3_1','date']
    new_df = df[columns_needed]
    new_df.to_csv("SpeedDatingDataClean.csv", index=False)
    
    csv_file = open("SpeedDatingDataClean.csv")
    input_file = csv.DictReader(csv_file)
    
    i = 2 # the first row of data in the csv file is row 2
    rows_dict = {}
    for row in input_file:
        for key in row.keys():
            if row[key] != '':
                # make sure row[key] has no commas
                row[key] = row[key].replace(",", "")
                # convert row[key] from type string to float
                row[key] = float(row[key])
        # convert the values of row['date'] and row[go_out'] for 
        # scatterplots to be read more easily, if plotted.
        for col in ['date', 'go_out']:
            if row[col] == 1.0:
                row[col] = 7.0
            elif row[col] == 2.0:
                row[col] = 6.0
            elif row[col] == 3.0:
                row[col] = 5.0
            elif row[col] == 4.0:
                row[col] = 4.0
            elif row[col] == 5.0:
                row[col] = 3.0
            elif row[col] == 6.0:
                row[col] = 2.0
            elif row[col] == 7.0:
                row[col] = 1.0
            
        rows_dict[i] = row
        i += 1

    csv_file.close()
    
    return rows_dict
##### test extract_speed_dating_data() #####    
a = {'iid':66.0,'gender':1.0,'pid':58.0,'match':0.0,'pf_o_att':'',\
     'pf_o_sin':'','pf_o_int':'','pf_o_fun':'','pf_o_amb':'','pf_o_sha':'',\
     'attr1_1':20.0,'sinc1_1':25.0,'intel1_1':15.0,'fun1_1':15.0,'amb1_1':53.0,\
     'shar1_1':20.0,'attr3_1':6.0,'sinc3_1':7.0,'fun3_1':7.0,'intel3_1':8.0,\
     'amb3_1':8.0,'go_out':4.0,'career_c':7.0,'wave':3.0,'income':'',\
     'date':2.0,'age':29.0}
assert extract_speed_dating_data()[912] == a
a = {'pid': 529.0, 'attr1_1': 70.0, 'career_c': 15.0, 'pf_o_amb': 10.0, \
'amb3_1': 7.0, 'shar1_1': 0.0, 'pf_o_att': 10.0, 'income': '', \
'pf_o_sha': 20.0, 'intel1_1': 15.0, 'match': 0.0, 'pf_o_int': 25.0, \
'pf_o_sin': 25.0, 'intel3_1': 7.0, 'wave': 21.0, 'iid': 552.0, 'sinc3_1': 7.0, \
'date': 6.0, 'amb1_1': 0.0, 'sinc1_1': 0.0, 'go_out': 7.0, 'gender': 1.0, \
'age': 25.0, 'pf_o_fun': 10.0, 'attr3_1': 8.0, 'fun3_1': 6.0, 'fun1_1': 15.0}
assert extract_speed_dating_data()[8378] == a

def extract_individual_data():
    """
    Condense the dictionary returned by extract_speed_dating_data() into a
    smaller dictionary. Keys are the iids of the speed dating participants, and 
    values are another dictionary. Each nested dictionary's key should be a 
    column specified in extract_speed_dating_data() and the value should be the 
    value of that column (based on the iid) in the csv.
    
    Return:
        individuals: dictionary of dictionaries
    """
    rows_dict = extract_speed_dating_data()
    col_names = ['iid','attr1_1', 'career_c', 'amb3_1', 'shar1_1', 'intel1_1', \
                 'intel3_1', 'wave', 'sinc3_1', 'amb1_1', 'sinc1_1', 'go_out', \
                 'gender', 'fun1_1', 'attr3_1', 'fun3_1','date','income','age']

    individuals = {}
    for key in rows_dict.keys():
        # create a sum_matches key, where the value is the total number of 
        # matches the participant has at the end of the event
        if (rows_dict[key]["iid"] in individuals) and \
           ("sum_matches" in individuals[rows_dict[key]["iid"]]):
            individuals[rows_dict[key]["iid"]]["sum_matches"] += \
            rows_dict[key]["match"]
        else:
            individuals[rows_dict[key]["iid"]] = {}
            if rows_dict[key]["match"] != '':
                individuals[rows_dict[key]["iid"]]["sum_matches"] = \
                rows_dict[key]["match"]
            for col in col_names:
                individuals[rows_dict[key]["iid"]][col] = rows_dict[key][col]         
    
    return individuals

##### test extract_individual_data() #####
a = {'amb1_1': 15.0, 'date': 1.0, 'sinc1_1': 20.0, 'go_out': 7.0, 'age': 21.0, \
'gender': 0.0, 'fun1_1': 15.0, 'intel3_1': 8.0, 'attr1_1': 15.0, \
'shar1_1': 15.0, 'amb3_1': 7.0, 'iid': 1.0, 'sinc3_1': 8.0, 'career_c': '', \
'income': 69487.0, 'sum_matches': 4.0, 'attr3_1': 6.0, 'wave': 1.0, \
'fun3_1': 8.0, 'intel1_1': 20.0}
assert extract_individual_data()[1] == a
a = {'amb1_1': 0.0, 'gender': 1.0, 'fun1_1': 15.0, 'intel3_1': 7.0, \
'date': 6.0, 'sinc1_1': 0.0, 'go_out': 7.0, 'age': 25.0,'attr1_1': 70.0, \
'shar1_1': 0.0, 'attr3_1': 8.0, 'wave': 21.0, 'fun3_1': 6.0, 'intel1_1': 15.0,\
'amb3_1': 7.0, 'iid': 552.0, 'sinc3_1': 7.0, 'career_c': 15.0, 'income': '', \
'sum_matches': 6.0}
assert extract_individual_data()[552] == a
    
def delete_empty_data(col_names, data_version):
    """
    Delete nested dictionaries that have values equal to ''.
     
    Parameters:
        col_names: list of some column names from the csv file
        data_version: string
    Return:
        data: dictionary of dictionaries
    """
    # call either extract_individual_data() or extract_speed_dating_data()
    if data_version == "individual":
        data = extract_individual_data()
    elif data_version == "original":
        data = extract_speed_dating_data()
    for key in data.keys():
        for col in col_names:
            if key in data:
                if (col != "wave") and (data[key][col] == ''):
                    del data[key]
                if col == "wave":
                    for i in range(6, 10):
                        if (key in data) and (data[key]["wave"] == \
                        float(i)):
                            del data[key] 
                            
    return data
    
##### test delete_empty_data() #####
assert 118 not in delete_empty_data(['iid'],"individual")
a = {'amb1_1': 10.0, 'date': 5.0, 'sinc1_1': 10.0, 'go_out': 7.0, 'age': 25.0, \
'gender': 0.0, 'fun1_1': 10.0, 'intel3_1': 9.0, 'attr1_1': 35.0, \
'shar1_1': 0.0, 'amb3_1': 8.0, 'iid': 3.0, 'sinc3_1': 9.0, 'career_c': '', \
'income': '', 'sum_matches': 0.0, 'attr3_1': 8.0, 'wave': 1.0, 'fun3_1': 8.0, \
'intel1_1': 35.0}
assert delete_empty_data(["iid", "date", "sum_matches"],"individual")[3] == a

def scatterplot_data(columns_needed, xaxis_col, data_version):
    """
    Create scatterplot data for xaxis and yaxis ("sum_matches").
    
    Parameters:
        columns_needed: list of some column names from the csv file;
        xaxis_col: string;
                   must be the column name for which xaxis_hist values are being
                   created
        data_version: string
        
    Return:
        xaxis: list of floats
        sum_matches: list of floats
    
    """        
    cleaned_data = delete_empty_data(columns_needed, \
                                                       data_version)
    xaxis = []
    sum_matches = []    
    for iid in cleaned_data.keys():
        xaxis.append(cleaned_data[iid][xaxis_col])
        sum_matches.append(cleaned_data[iid]["sum_matches"])
            
    return xaxis, sum_matches
    
##### test scatterplot_data() #####
xaxis, sum_matches = scatterplot_data(["iid", "age", "sum_matches"], "age", \
    "individual")
assert len(xaxis) == len(sum_matches)
    
def plot_scatterplot(xaxis_label, columns_needed, xaxis_col, data_version): 
    """
    Plots a scatterplot of xaxis vs sum_matches.
    
    Parameters:
        xaxis_label: string
        xaxis_col: string;
                   must be the column name for which xaxis_hist values are being
                   created
        columns_needed: list of some columns in csv file
        data_version: string
        
    Return:
        xaxis: list of floats
        sum_matches: list of floats
        full_label: string
    """
    plt.clf()
    xaxis, sum_matches = scatterplot_data(columns_needed, xaxis_col, \
    data_version)
    assert len(xaxis) == len(sum_matches)
    plt.scatter(xaxis,sum_matches)
    plt.title('Age vs Total Matches')
    plt.xlabel(xaxis_label);
    plt.ylabel("Total Matches");
    full_label = xaxis_label + " vs Total Matches"
    plt.legend()
    plt.show()

    return xaxis, sum_matches, full_label
    
def scatterplot_results(xaxis_label, columns_needed, xaxis_col, data_version):
    """
    Print the name, sample size, and pearson correlation coefficient of the
    scatterplot.
    
    Parameters:
        xaxis_label: string
        columns_needed: list of some column names from the csv file
        xaxis_col: string;
                   must be the column name for which xaxis_hist values are being
                   created
        data_version: string
    """
    xaxis, sum_matches, full_label = plot_scatterplot(xaxis_label, \
    columns_needed, xaxis_col, data_version)
    r = pearsonr(xaxis, sum_matches)[0]
    print '--Scatterplot of', full_label + '--'
    print "  Sample Size:                     " + str(len(xaxis))
    print "  Pearson Correlation Coefficient: " + str(r)
    print

def main():
    #scatterplot_results("Going Out (not on a date) Frequency", \
    #["iid", "go_out", "sum_matches"], "go_out", "individual")
    #scatterplot_results("Dating Frequency", ["iid", "date", "sum_matches"], \
    #"date", "individual")
    scatterplot_results("Age", ["iid", "age", "sum_matches"], "age", \
    "individual")
    #scatterplot_results("Median Household Income ($) (based on zipcode)", \
    #["iid", "income", "sum_matches"], "income", "individual")

if __name__ == "__main__":
    main()