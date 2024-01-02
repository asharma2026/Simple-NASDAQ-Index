import pandas as pd
from datetime import datetime
#read through the reuters round up and print:
# company: percent raise
#optional: sorted.
def removecomma(str):
    """
    input: string
    output: string with no comma
    """
    f = ""
    for s in str:
        if s != ",":
            if s != '$':
                f += s
    return f

def roundup(file):
    otplist = []
    ntplist=[]
    companynamelist=[]
    datelist=[]
    fh = open(file)
    i=0
    for line in fh:
        if i == 0:
            date = line[0:6].strip()
        else:
            if "raises" and "from" in line:
                linei = line.find('$')
                listline = line[linei:].split()
                for ind in range(len(listline)):
                    listline[ind] = listline[ind].strip("$")
                    line1 = line.split(':')
                    name = line1[0] #define name of company
                    name = name[-6:-2].strip()
                    if listline != []:
                        newp = float(removecomma(listline[0]))
                        oldp = float(removecomma(listline[2]))
                        otplist.append(oldp)
                        ntplist.append(newp)
                        companynamelist.append(name)
                        datelist.append(date)
        i+=1
    pddf=pd.DataFrame()
    pddf["Ticker"] = companynamelist
    pddf["Old Target Price"] = otplist
    pddf["New Target Price"] = ntplist
    pddf["Date"] = datelist
    return pddf