#!/usr/bin/env python

import sys
import pandas as pd
import math

# get all the names we'll need
names2013 = pd.read_csv("inputData/yob2013.txt",names=["Name","Sex","Births"])
names2014 = pd.read_csv("inputData/yob2014.txt",names=["Name","Sex","Births"])

# let's calculate the 2014 biggest risers/fallers based on the "official Baby Name Wizard Hotness Formula"
# (sqrt |2014N-2013N|) * (2014N-2013N)/2013N

# separate boy and girl names
boynames2013 = names2013[names2013["Sex"] == "M"]
girlnames2013 = names2013[names2013["Sex"] == "F"]
boynames2014 = names2014[names2014["Sex"] == "M"]
girlnames2014 = names2014[names2014["Sex"] == "F"]

# add rank column
boynames2013.loc[:,"Rank"] = boynames2013["Births"].rank(ascending=False)
girlnames2013.loc[:,"Rank"] = girlnames2013["Births"].rank(ascending=False)
boynames2014.loc[:,"Rank"] = boynames2014["Births"].rank(ascending=False)
girlnames2014.loc[:,"Rank"] = girlnames2014["Births"].rank(ascending=False)

# merge 2013 and 2014 frames
boyNamesMerged = pd.merge(boynames2013,boynames2014,on=["Name","Sex"],suffixes=('2013', '2014'))
girlNamesMerged = pd.merge(girlnames2013,girlnames2014,on=["Name","Sex"],suffixes=('2013', '2014'))

# function to calculate hotness
def hotness(row):
    return math.sqrt(math.fabs(row["Births2014"]-row["Births2013"])) * (row["Births2014"]-row["Births2013"])/float(row["Births2013"])

# add hotness column, sort by hotness and reindex
boyNamesMerged.loc[:,"Hotness"] = boyNamesMerged.apply(lambda row: hotness(row), axis=1)
boyNamesMerged.sort_values("Hotness",ascending=False,inplace=True)
boyNamesMerged.reset_index(drop=True)
girlNamesMerged.loc[:,"Hotness"] = girlNamesMerged.apply(lambda row: hotness(row), axis=1)
girlNamesMerged.sort_values("Hotness",ascending=False,inplace=True)
girlNamesMerged.reset_index(drop=True)

# select only names in the top 1000 of either year
boyNamesFiltered = boyNamesMerged[(boyNamesMerged["Rank2013"] < 1000) | (boyNamesMerged["Rank2014"] < 1000)]
girlNamesFiltered = girlNamesMerged[(girlNamesMerged["Rank2013"] < 1000) | (girlNamesMerged["Rank2014"] < 1000)]


# print results
print
print "---------------------------- TOP 10 BOY RISERS ---------------------------"
print
print boyNamesFiltered[:10].reset_index(drop=True)
print
print
print "---------------------------- TOP 10 BOY FALLERS --------------------------"
print
print boyNamesFiltered[-10:].sort_values("Hotness",ascending=True).reset_index(drop=True)

print
print
print "---------------------------- TOP 10 GIRL RISERS --------------------------"
print
print girlNamesFiltered[:10].reset_index(drop=True)
print
print
print "---------------------------- TOP 10 GIRL FALLERS -------------------------"
print
print girlNamesFiltered[-10:].sort_values("Hotness",ascending=True).reset_index(drop=True)




