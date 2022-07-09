from flask import Flask, request, render_template, jsonify, url_for, flash, redirect
import os
from datetime import datetime, timedelta

app = Flask(__name__, static_folder='public', template_folder='views')


#def hello():
  #return "Hello World!"
@app.route('/create', methods=['GET', 'POST'])
def create():
   if request.method == 'POST':
    salary = request.form['salary']
    salary = float(salary) if salary else 50000
    commuteRoundTripHrs = request.form['hoursCommuted']
    commuteRoundTripHrs = float(commuteRoundTripHrs) if commuteRoundTripHrs else 1
    
    monthlyCommuteCost = request.form['monComCost']
    monthlyCommuteCost = float(monthlyCommuteCost) if monthlyCommuteCost else 100
    monthlyChildCareCost = request.form['monChildCareCost']
    monthlyChildCareCost = int(monthlyChildCareCost) if monthlyChildCareCost else 0
    customStartDate = request.form['startDate']
    customStartDate = datetime.strptime(customStartDate, '%Y-%m-%d') if customStartDate else 0
  #return render_template('index.html')
    if customStartDate == 0:
      startDate = datetime(2020, 3, 17)
    else:
      startDate = customStartDate
    endDate = datetime.today()
    deltaDate = endDate - startDate
    deltaCount = deltaDate.days
    avgDaysPTO = 12
    avgDaysSick = 9
    avgDaysHol = 8
    avgBusDays = 260
    avgWorkingDays = avgBusDays - (avgDaysPTO + avgDaysSick + avgDaysHol)
    yearModu = deltaCount % 365
    yearsCount = deltaCount // 365
    yearModPercent = yearModu / 365
    yearModBusDays = round(avgWorkingDays * yearModPercent)
    totalBusDays = int(yearModBusDays + (yearsCount * avgWorkingDays))
    #salary = 32000
    hourly = round((salary/52)/40)
    #commuteRoundTripHrs = 1
    timeSaved = int(commuteRoundTripHrs * totalBusDays)
    hourlyWorth = (hourly * timeSaved)
    
    #monthlyCommuteCost = 165
    yearlyCommuteCost = monthlyCommuteCost * 12
    totalCommuteCost = round((yearlyCommuteCost * yearsCount) + (yearlyCommuteCost * yearModPercent))
    yearlyChildCareCost = monthlyChildCareCost * 12
    totalChildCareCost = round((yearlyChildCareCost * yearsCount) + (yearlyChildCareCost * yearModPercent))
    totalSavings = round(totalCommuteCost + totalChildCareCost + hourlyWorth)
    annualRaise = int(yearlyCommuteCost + yearlyChildCareCost + (hourly * (commuteRoundTripHrs * avgWorkingDays)))
    respStr = "You have not commuted for approximately <b>{}</b> business days.<br>" \
    "You saved you atleast <b>{}</b> hours lost to commuting.<br>" \
    "You saved you approximately <b>${}</b> on your commuting expenses.<br>" \
    "If you were paid to commute, your time was worth <b>${}</b>.<br>" \
    "This saved you approximately <b>${}</b> on your child care expenses.<br>" \
    "Working remote is equal to a <b>${}</b> annual raise.<br>" \

    "Working remotely is worth <b>${}</b> for you." \
    .format(totalBusDays,timeSaved,totalCommuteCost,hourlyWorth,totalChildCareCost,annualRaise,totalSavings) 
    return respStr 
  #return render_template('create.html')

@app.route("/")

def index():
  return render_template('index.html')

if __name__ == "__main__":
  app.run()

  ###