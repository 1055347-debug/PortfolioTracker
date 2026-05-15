import json 
import yfinance
import statistics
import datetime
allofthedata = {}
oldtotalvaluelist = []
lastday = []
totalvaluelist = []
standarddeviation = {}
portfolio = {"INTC" : 6, "APA" : 25, "WCPRF" : 11, "CVX" : 3, "PFE" : 10}
for x, y in portfolio.items():
    try:
        data = yfinance.download(x, period="6mo")
        lastday1 = data.tail(2)
        lastday2 = lastday1["Close"][x].iloc[-2]
        totalvalue3 = lastday2 * y
        lastday.append(totalvalue3)
        data4 = data.head(1)
        data5 = data4["Close"][x].item()
        totalvalue2 = data5 * y
        oldtotalvaluelist.append(totalvalue2)
        data1 = data.tail(1)
        data2 = data1["Close"][x].item()
        totalvalue = data2 * y
        totalvaluelist.append(totalvalue)
        data3 = data["Close"][x]
        standard = statistics.stdev(data3)
        standarddeviation[x] = [standard]
        allofthedata[x] = {
            f"Current amount of {x}" : totalvalue,
            f"volatility" : standarddeviation[x],
            f"RiskStatus" : "HIGH" if standard > 10 else "LOW"
        }
    except Exception as error_message:
        print(f"WORNG TICKER {x}: {error_message}")
        continue
sum1 = sum(totalvaluelist)
sum2 = sum(oldtotalvaluelist)
totalportofliovalueyesterday = sum(lastday)
difference2 = sum1 - totalportofliovalueyesterday
difference = sum1 - sum2
currenttime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
highestone = "HI"
max_key = max(standarddeviation, key=standarddeviation.get)
fulldata = {
    "IndividualStockInformation" : allofthedata,
    "TotalValue" : sum(totalvaluelist),
    "HowMuchYourPortfolioHasGrownSinceYesterday" : difference2 / totalportofliovalueyesterday,
    "HowMuchYourPortfolioHasGrownI6Months" : difference / sum(oldtotalvaluelist),
    "LastUpdated" : currenttime,
    "HIGHESTRISKASSEST" : max_key
}
with open("Portfoliotracker.json", "w") as json_file:
    json.dump(fulldata, json_file, indent=4)