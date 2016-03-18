#!/usr/bin/env python

from os import path
from glob import glob
from shutil import copy
from sys import exit
from csv import reader

from ROOT import TH1F, TCanvas, TLegend, TMarker
from ROOT import gROOT, gStyle, SetOwnership
from ROOT import kRed, kOrange, kYellow, kGreen, kBlue, kViolet, kPink, kCyan, kBlack

START = 1880
END = 2015
REBIN = 5

inputDir = '/Users/lantonel/DataScience/BabyNames/inputData/'

fileList = glob(inputDir+'yob*')

gROOT.SetBatch()
gStyle.SetOptStat(0)

colors = [kRed+1,kOrange+1,kYellow+1,kGreen+1,kBlue+1,kViolet+1,kPink+1,kCyan+1,kBlack]

antonellis = [
#    ['Linda','F',1952],
#    ['Vincent', 'M', 1952],
    ['Jamie', 'M', 1982],
    ['Rebecca', 'F', 1986],
    ['Christopher', 'M', 1988],
    ['Dominic', 'M', 1991]
]

storey_girls = [
    ['Sarah', 'F', 1983],
    ['Nicole', 'F', 1986],
    ['Rebecca', 'F', 1998],
    ['Rachel', 'F', 1998],
]

storey_boys = [
    ['Adam', 'M', 1985],
    ['Robert', 'M', 1988],
    ['Richard', 'M', 1992],
    ['Stephen', 'M', 1995],
    ['Michael', 'M', 2000]
]

name_ideas = [
    ['Madeleine', 'F'],
    ['Vincent', 'M'],
    ['Genevieve', 'F'],
    ['Augustine', 'M'],
    ['Zelie', 'F'],
    ['Maximilian', 'M'],
]

def makePlot(name, sex):

    plot = TH1F(name + "_" + sex, name, END-START, START, END)
    plot.SetLineWidth(3)
    SetOwnership(plot, False)

    if sex == "M" and name not in boyNames:
        return plot
    if sex == "F" and name not in girlNames:
        return plot

    for year in range(START, END):
        if sex == "M" and year in boyNames[name]:
            plot.Fill(year, float(boyNames[name][year])/boyBirths[year])
        elif sex == "F" and  year in girlNames[name]:
            plot.Fill(year, float(girlNames[name][year])/girlBirths[year])

    plot.Rebin(REBIN)
    return plot

# change the plot to go from 0 to 1
# 0 => least popular year
# 1 => most popular year
def normalizePlot(plot):

    min = plot.GetMinimum()
    max = plot.GetMaximum()
    range_ = max - min
    for bin in range(plot.GetNbinsX()+1):
        content = plot.GetBinContent(bin)
        newContent = (content - min) / range_ + 0.1
        plot.SetBinContent(bin, newContent)

def produceBoyGirlPlot(name):

    boyPlot = makePlot(name,"M")
    girlPlot = makePlot(name,"F")

    boyPlot.SetLineColor(kBlue+1)
    girlPlot.SetLineColor(kPink+1)

    legend = TLegend(0.1,0.7,0.4,0.87)
    legend.SetBorderSize(0)
    legend.SetFillStyle(0)

    canvas = TCanvas(name)

    legend.AddEntry(boyPlot, "boys", "L")
    legend.AddEntry(girlPlot, "girls", "L")

    if boyPlot.GetMaximum() > girlPlot.GetMaximum():
        girlPlot.SetMaximum(boyPlot.GetMaximum())

    girlPlot.Draw("C")
    boyPlot.Draw("same C")
    legend.Draw()

    canvas.SaveAs(name + "_BoyGirl.pdf")

def produceFamilyPlot(family, surname):

    canvas = TCanvas(surname,"",2400,800)

    legend = TLegend(0.1,0.5,0.4,0.87)
    legend.SetBorderSize(0)
    legend.SetFillStyle(0)

    counter = 0
    markers = []
    for person in family:
        if len(person) < 2:
            print "error"
            continue
        name = person[0]
        sex = person[1]

        if len(person) >= 3:
            birth = person[2]
        else:
            birth = 0

        plot = makePlot(name, sex)
        normalizePlot(plot)

        plot.SetTitle("")
        plot.GetYaxis().SetLabelSize(0)
        plot.GetXaxis().SetLabelSize(0.07)
        plot.GetYaxis().SetTickSize(0)
        plot.GetYaxis().SetTitle("normalized popularity")
        plot.GetYaxis().SetTitleSize(0.07)
        plot.GetYaxis().SetTitleOffset(0.22)

        plot.SetLineColor(colors[counter])
        legend.AddEntry(plot, name, "L")
        plot.Draw("same C")
        if birth > 0:
            marker = TMarker(birth+0.5,plot.GetBinContent(plot.FindBin(birth)),20)
            marker.SetMarkerColor(colors[counter])
            marker.SetMarkerSize(5)
            markers.append(marker)
            markers[counter].Draw("same")

        counter += 1
    legend.Draw()

    canvas.SaveAs(surname + ".pdf")


# parse input data into a python dictionary, using the name as a key
# use separate dictionaries for boy/girl names
boyNames = {}
girlNames = {}


boyBirths = {}
boyFile = open("BoyBirthsByYear.txt")
for line in boyFile:
    splitline = line.split(" ")
    boyBirths[int(splitline[0])] = int(splitline[1].strip())

girlBirths = {}
girlFile = open("GirlBirthsByYear.txt")
for line in girlFile:
    splitline = line.split(" ")
    girlBirths[int(splitline[0])] = int(splitline[1].strip())


for file in fileList:
    year = file.split("/")[-1][3:7]
#    boyBirths = 0
#    girlBirths = 0
    with open(file) as data:
        entries = reader(data)
        for entry in entries:
            if len(entry) < 3:
                continue
            name = entry[0]
            sex = entry[1]
            count = entry[2]

#            if sex == "M":
#                boyBirths += int(count)
#            if sex == "F":
#                girlBirths += int(count)

            if sex == "M" and name not in boyNames:
                boyNames[name] = {}
                boyNames[name]["sex"] = sex
            elif sex == "F" and name not in girlNames:
                girlNames[name] = {}
                girlNames[name]["sex"] = sex

            if sex == "M":
                boyNames[name][int(year)] = count
            elif sex == "F":
                girlNames[name][int(year)] = count

#    girlBirthsFile.write(year + " " + str(girlBirths) + "\n")
#    boyBirthsFile.write(year + " " + str(boyBirths) + "\n")


print "parsed", len(girlNames), "unique girl names"
print "parsed", len(boyNames), "unique boy names"

produceFamilyPlot(antonellis, "Antonelli")
produceFamilyPlot(storey_girls, "Storey Girls")
produceFamilyPlot(storey_boys, "Storey Boys")
produceFamilyPlot(name_ideas, "Name Ideas")
produceBoyGirlPlot("Jamie")
produceBoyGirlPlot("Madeleine")
produceBoyGirlPlot("Madeline")
produceBoyGirlPlot("Nicole")
produceBoyGirlPlot("Zelie")
