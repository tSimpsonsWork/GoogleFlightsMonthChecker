This is a python code that uses various libraries and Chromedriver to execute and run.

#Running the code

1.	Python 3 must be downloaded to be used in a IDE or Command line

2.	Pip extension must be installed https://pypi.org/project/pip/ or https://github.com/pypa/pip

3.	In the command line install
•	pip(pip3 on mac) install scikit-learn
•	pip(pip3 on mac) install Selenium
•	pip(pip3 on mac) install Pandas
•	pip(pip3 on mac) install matplotlib

4.	download https://chromedriver.chromium.org/downloads for google chrome! (Already in the project folder just update the driver to your current chrome version “Youtube helps”) 

5.	Now run the program and answer the 4 questions provided.
•	The goal is that you will be selecting a airport of travel by airport code -----PS if you have 3 completed xlsx files press 4 to combine to master when asked----
•	Where are you going?(Airport code - example: HND = Japan or LIS = Portugal) =  ‘BNC’ (only 3 letter airport code)
•	What is your budget? 'will inform you on which are expensive' = ‘600’ (No $ needed or decimals)
•	That's great, what month input (1-12) =  ‘12’ (not Jan or 01)
•	Which sheet 1, 2 or 3 (Max sheets = 3, will override but 4 will combine all 3 ---press 4 only when all 3 are done---) = (1,2,3,or 4)  - this is important to follow 4 will allow you to save 1,2 and 3 to on MasterGFD if you press ‘y’ or ‘Y’ after 4

6.	Once y is pressed a graph will appear with the outputs of the locations searched

7.	The MasterGFD will have the unsorted excel 1-3 onto a sorted excel file.


#Chaninging the code 
•	Line 29: Change baseAirport = “your 3-letter airport”
