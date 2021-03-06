import texttable as tt
import math as mt

def listAver(inList):
  return sum(inList) / len(inList)

def multLists(leftList, rightList, listSize):
  result = list()

  for i in range(0, listSize):
    result.append(leftList[i] * rightList[i])

  return result

# main

# input values
n = 14

# Empirical ditribution
xArr = [list(range(0, 13)), list(range(12, 25)), list(range(24, 37))
      , list(range(36, 49)), list(range(48, 61)), list(range(60, 73))
      , list(range(72, 85)), list(range(84, 97)), list(range(96, 109))]

xArrStr = ["0-12", "12-24", "24-36", "36-48", "48-60"
         , "60-72", "72-84", "84-96", "96-108"]

mArr = [6 + n, 5 + n, 5 + n, 5 + n, 5 + n, 5 + n, 4 + n, 5 + n, 4 + n]

empDict = dict()

for i in range(0, len(xArrStr)):
  empDict[xArrStr[i]] = set()
  empDict[xArrStr[i]] = mArr[i]

empTab = tt.Texttable()

empTab.add_row(["X"] + xArrStr)
empTab.add_row(["m[i]"] + mArr)

printEmpTab = empTab.draw()

print(printEmpTab)

# Frequency polygon
xAverList = len(xArr) * [0]

for i in range(0, len(xArr)):
  xAverList[i] = listAver(xArr[i])
  print("y(%(x)f) = %(y)f" % { "x" : xAverList[i], "y" : mArr[i] })

# Count table and other data for Pirson's test
countTbl = tt.Texttable()

countTbl.add_row(["x"]    + xArrStr   + ["Sum"])
sumMArr = sum(mArr)
countTbl.add_row(["m[i]"] + mArr      + [sumMArr])
countTbl.add_row(["x[i]"] + xAverList + [sum(xAverList)])

xMultmList = multLists(xAverList, mArr, len(xAverList))
sumxMultm  = sum(xMultmList)
countTbl.add_row(["x[i] * m[i]"] + xMultmList + [sumxMultm])

xAverSqrArr   = multLists(xAverList, xAverList, len(xArr))
xSqrMultmList = multLists(xAverSqrArr, mArr, len(mArr))
sumxSqrMultm  = sum(xSqrMultmList)
countTbl.add_row(["x[i]^2 + m[i]"] + xSqrMultmList + [sumxSqrMultm])

countTbl.set_cols_width((len(xArrStr) + 2) * [10])
printCountTbl = countTbl.draw()

print(printCountTbl)

xAver   = float(sumxMultm) / float(sumMArr)
dispers = (float(sumxSqrMultm) / float(sumMArr)) - float(xAver) ** 2
sigma   = mt.sqrt(dispers)

print("x aver = %(xa)f\nD = %(dsp)f\nsigma = %(sgm)f" % { "xa" : xAver, "dsp" : dispers, "sgm" : sigma })

# Table with probabilities
pTab = tt.Texttable()

pTab.add_row(["X", "x[i]", "x[i + 1]", "p[i]", "theoretical m[i]", "m", "(m[t]^T - m) ^ 2 / m[t]^T"])

probability = 1 / len(mArr)
teoreticalM = probability * sumMArr

sumLeftX  = 0
sumRightX = 0
criteriaSum = 0

for i in range(0, len(xArrStr)):
  sumLeftX  += xArr[i][0]
  sumRightX += xArr[i][len(xArr[i]) - 1]

  criteria = ((teoreticalM - mArr[i]) ** 2) / teoreticalM
  criteriaSum += criteria

  pTab.add_row([xArrStr[i]] + xArrStr[i].split("-") +
               [probability] + [teoreticalM] + [mArr[i]] +
               [criteria])

pTab.add_row(["Sum"] + [sumLeftX, sumRightX
           , len(xArrStr) * probability, len(xArrStr) * teoreticalM, sum(mArr)
           , criteriaSum])

pTab.set_cols_width(7 * [10])
printPTab = pTab.draw()

print(printPTab)

degreesOfFreedom = len(xArr) - 3
signiflvl        = 0.05
chisqcr          = 1.635

print("Chi[b]^2 = %(chibs)f\nk = %(degoffr)f\nalpha = %(signiflvl)f\nChi[cr]^2 = %(chicrs)f"
      % { "chibs" : criteriaSum, "degoffr" : degreesOfFreedom, "signiflvl" : signiflvl, "chicrs" : chisqcr })
