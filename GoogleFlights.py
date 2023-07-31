# To run this program python 3 is needed
# pip is need for the device https://pypi.org/project/pip/ or https://github.com/pypa/pip (terminal pip3(mac) or windows pip
# $ pip(3) install selenium, pandas
# download the chromewebdriver from https://chromedriver.chromium.org/downloads
# add it to the project fold or get the path of the folder its is in
import time
from _datetime import datetime
import calendar
from selenium import webdriver#install selenium (terminal/ cm line)
from selenium.webdriver.common.by import By#pip install selenium (terminal/ cm line)
import pandas as pd##pip install selenium (terminal/ cm line)
from sklearn.model_selection import train_test_split##pip install selenium (terminal/ cm line)
from sklearn.neighbors import KNeighborsClassifier#pip install Sckit-learn(terminal/ cm line)
from sklearn.metrics import accuracy_score, f1_score ##pip install Sckit-learn(terminal/ cm line)
import matplotlib.pyplot as pt ##pip install matplotlib(terminal/ cm line)
#Line 29 baseAirport to use your Airport
#-------------------------------------------------------------------------------------------------------
#current time
currentMonth = datetime.now().month
currentYear = datetime.now().year
#-------------------------------------------------------------------------------------------------------
#gets depature
print("Welcome to the google flights month selection")
print("The goal is that you will be selecting a airport of travel by airport code -----PS if you have 3 completed xlsx files press 4 to combine to master when asked----")
print()
departure = input("Where are you going?(Airport code - example: HND = Japan or LIS = Portugal) ")
length = len(departure)
#=========================================
baseAirport = "MIA" #Use your 3 letter Airport
#=========================================
#-------------------------------------------------------------------------------------------------------
while length != 3:
    departure = input("Please enter 3 letter airport code ")
    length = len(departure)
#Checks for length MIA = 3
#-------------------------------------------------------------------------------------------------------
budget = input("What is your budget? 'will inform you on which are expensive' ")
#This method test to see if the budget is an integer
def isValidInt(input):
    if input[0] == '-':
        return input[1:].isdigit()
    else:
        return input.isdigit()
#-------------------------------------------------------------------------------------------------------
#Checks budget for non strings
while bool(not isValidInt(budget)):
    budget = input("Please put a integers and non negatives ")
if int(budget) < 0:
    budget = int(budget) * -1
#-------------------------------------------------------------------------------------------------------
def isExpensive(usd):
    if usd > int(budget):
        return "Yes"
    else:
        return "No"
#Used later in def scrape to compare prices

#Put the month of travel
month = input("That's great, what month input (1-12) ")
while bool(not isValidInt(month)):
    month = input("Please put a correct month! {1-12} ")
#-------------------------------------------------------------------------------------------------------
#Takes care of negatives
if int(month) < 0:
    month = int(month) * -1

#-------------------------------------------------------------------------------------------------------
#handles following year
if int(month) < currentMonth:
    currentYear += 1

#-------------------------------------------------------------------------------------------------------
#Important! saves files on xlsx
count = input("Which sheet 1, 2 or 3 (Max sheets = 3, will override but 4 will combine all 3 ---press 4 only when all 3 are done---) ")
while bool(not isValidInt(count)):
    count = input("Please put a integers and non negatives ")
if int(count) < 0:
    count = int(count) * -1
#-------------------------------------------------------------------------------------------------------
_, weekdays = calendar.monthrange(currentYear, int(month))# this is for getting the year and amount of days in a month
currentYear = str(currentYear)
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options)
#Firsday of the month and index of arrays
firstDay = "1"
index = 0
#-------------------------------------------------------------------------------------------------------
minDays = weekdays - 4 #Change to have it do 30 days or less
#-------------------------------------------------------------------------------------------------------
location = [departure] * (minDays - 1)  #[index] * weekdays
prices = [-1] * (minDays - 1) #[index] * weekdays
datesOfTravel = [0] * (minDays - 1) #[index] * weekdays
expensive = [""] * (minDays - 1) #[index] * weekdays
#-------------------------------------------------------------------------------------------------------
#Searches google flights for prices
def scrape(input, counter):
    if int(month) > 0 and int(month) < 13:
        driver.get("https://www.google.com/travel/flights?q=Flights%20to%20" + departure.upper() + "%20from%20" + baseAirport + "%20on%20" + currentYear + "-" + month + "-" + input.zfill(2) +"%20oneway&curr=USD")
    else:
        print(month + " is not on the calendar")
        driver.quit()

    div_element = driver.find_element(By.CLASS_NAME, 'JMc5Xc')
    aria_label = div_element.get_attribute('aria-label')
    price = aria_label.split(' ')[1]
    print()
    #Prints in console for debuggin print("$" + price + " on this day: " + input.zfill(2))#Prints in console for debuggin
    date_str = month.zfill(2) + "/" + input.zfill(2) + "/" + currentYear
    adding = str(int(input) + 5)
    date_str += "-" + month.zfill(2) + "/" + adding.zfill(2) + "/" + currentYear
    first = int(price)

    driver.get("https://www.google.com/travel/flights?q=Flights%20to%20" + baseAirport + "%20from%20" + departure.upper() +"%20on%20" + currentYear + "-" + month + "-" + str(adding).zfill(2) +"%20oneway&curr=USD")
    time.sleep(2)
    div_element = driver.find_element(By.CLASS_NAME, 'JMc5Xc')
    aria_label = div_element.get_attribute('aria-label')
    price2 = aria_label.split(' ')[1]
    print()
    # print("$" + price2 + " on this day: " + adding.zfill(2))#Prints in console for debuggin
    second = int(price2)
    final = first + second
    prices[counter] = int(final)
    datesOfTravel[counter] = date_str
    expensive[counter] = isExpensive(final)
    print("Total: $" + str(prices[counter]) + " on this day " + date_str)



#Which excel do you want 4 is the Master!
sheet = ""
if count == "1":
    sheet = "1"
elif count == "2":
    sheet = "2"
elif count == "3":
    sheet = "3"
else:
    sheet = "4"
#Excutes the search
while int(firstDay) < minDays and sheet != "4":
    scrape(firstDay, index)
    time.sleep(1)
    firstDay = str(int(firstDay) + 1)
    index += 1
#Skips thr search if 4 is pressed
if sheet != "4":
    driver.close()
#Stores Data
    data = {'Locations': location, 'Dates': datesOfTravel, 'Price': prices, 'Expensive': expensive}
    print(data)
    GFD = "GoogleFlightData" + sheet + ".xlsx"
#GFD is which excel of use
    excelWriter = pd.ExcelWriter(GFD)
    df = pd.DataFrame(data)
    df.to_excel(excelWriter)
    excelWriter.close()
    print("Once you are ready to save the files to the master start it again then press 4 for sheet on excel")
else:
    driver.close()
    print(sheet + " is equal to combine the 3 xlsx files ")
    try:
        excel1 = pd.read_excel('GoogleFlightData1.xlsx')

        excel2 = pd.read_excel('GoogleFlightData2.xlsx')

        excel3 = pd.read_excel('GoogleFlightData3.xlsx')

        combined1 = excel1[['Locations', 'Dates', 'Price', 'Expensive']]
        combined2 = excel2[['Locations', 'Dates', 'Price', 'Expensive']]
        combined3 = excel3[['Locations', 'Dates', 'Price', 'Expensive']]


        join = pd.concat([combined1, combined2, combined3])
        joined = join.sort_values(by='Price', ascending=True)

        print("=======================================================================================================")
        print(joined)#Prints in table before executation
        print("=======================================================================================================")
        print()
        decide = input("Do want to save the table to the master and the 3 cheapest flights to the csv (input == y)? ")
        print()
        if decide == "Y" or decide == "y":
            #Important! saves over 1-3 to MasterDGFD
            joined.to_excel('MasterGFD.xlsx')
            print("Saved!")


            # # x and y axis of the knn
            # x_axis = joined[['Price']]
            # y_axis = joined['Expensive']
            # knn = KNeighborsClassifier(n_neighbors=3)
            # #k = #
            # #sets the training and testing
            # x_training, x_testing, y_training, y_testing = train_test_split(x_axis, y_axis, test_size=0.8, random_state=42, train_size=0.2)
            #
            # #Fits the x - y training
            # knn.fit(x_training, y_training)
            # #gets the predicated data
            # y_prediction = knn.predict(x_testing)
            # #Calculates Accuracy and F1 (Precision and Recall)
            # accurate = accuracy_score(y_testing, y_prediction)#Used to find the accuracy of the master data
            # f1 = f1_score(y_testing, y_prediction, pos_label='No')#Used to find the F1 score in SKLearn from the master data
            # print(f"Accuracy:, {accurate:.4f}")
            # print(f"F1 Score: {f1:.4f}")





            # #labels for plotting and graphing
            # labels = ['F1', 'Accuracy']
            # values = [f1, accurate]
            #
            # pt.subplot(2, 2, 1)
            # pt.scatter(labels, values)
            # pt.ylabel('Total')
            # pt.title('F1 and Accuracy Scatter')
            #
            # pt.subplot(2, 2, 2)
            # pt.pie(values, labels=labels, autopct='%1.1f%%')
            # pt.ylabel('Total')
            # pt.title('F1 and Accuracy Pie')
            #
            # pt.tight_layout()
            # pt.show()



        else:
            print("Enjoy you trip! and press 4 next time to save to master")#If you do not save
    except FileExistsError:
        print("No file found.")
        #if there is no files to save




#---------------------------------------------------------------------------------





