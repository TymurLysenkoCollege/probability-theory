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
xArr = [  list(range(0, 13)), list(range(12, 25)), list(range(24, 37))
        , list(range(36, 49)), list(range(48, 61)), list(range(60, 73))
        , list(range(72, 85)), list(range(84, 97)), list(range(96, 109))]

xArrStr = [  "0-12", "12-24", "24-36", "36-48", "48-60"
           , "60-72", "72-84", "84-96", "96-108"]

mArr = [16, 12, 12, 9, 8, 8, 6, 6, 4]

# print frequency polygon
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

# lambda
lam = 0.5 * ( (1 / xAver) + (1 / sigma) )
print("Lambda =", lam)

# Table with probabilities

pTab = tt.Texttable()

pTab.add_row( ["X", "x[i]", "x[i + 1]", "-lambda[x[i]]", "-lambda[x[i + 1]]", "e ^ -lambda[x[i]]"
             , "e ^ -lambda[x[i + 1]]", "p[i]", "theoretical m[i]", "m", "(m[t]^T - m) ^ 2 / m[t]^T"])

sumLeftX  = 0
sumRightX = 0
criteriaSum = 0

for i in range(0, len(xArrStr)):
  sumLeftX  += xArr[i][0]
  sumRightX += xArr[i][len(xArr[i]) - 1]

  # teoreticalM = probability * sumMArr
  # criteria = ((teoreticalM - mArr[i]) ** 2) / teoreticalM
  # criteriaSum += criteria

  pTab.add_row([xArrStr[i]] + xArrStr[i].split("-") + (6 * [""]) + # TODO : get to know how to count these lambdas, p[i]
               [mArr[i]] + [""])

# pTab.add_row(["Sum"] + )

pTab.set_cols_width(11 * [10])
printPTab = pTab.draw()

print(printPTab)
