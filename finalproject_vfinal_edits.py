#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 22:40:44 2020

@author: tobijegede
"""

#importing all of the required modules
import pandas as pd 
import json
import requests
from bs4 import BeautifulSoup
import re

#Used to check if a file already exists
import os.path
from os import path



#To do:
#Decide on how we want users to input a course number
#Can users ask for mutiple options at once and get all their requests return at once?
#Will each indvidual call of menu give a different thing?
# For Aly -- What data type does your function return? How can information be extracted from this data source?
# For Sanjana -- (see the above question for Aly)
# Are we still trying to pull semester information from the syllabus string?
#Is there any additional funcitonality that we want?
# Still need to complete the presentation and associated documentation



#Question -- Why is the index of the eval dataframe an integer.float and not a string?

def csv_func(course_num, path1):
    #initial error -'utf-8' codec can't decode byte 0xa0 in position 0: invalid start byte
    #cause - The error is because there is some non-ascii character in the dictionary and it can't be encoded/decoded.
    #soln -data = pd.read_csv(filename, encoding= 'unicode_escape')
    
    eval= pd.read_csv(path1, encoding= 'unicode_escape')
    code=int(course_num)
   
    eval=eval.rename(columns={'Sem':'Semester','Num':'Course_Code',
                              'CourseName':'Course_Name',
                              'Clearly explain course requirements':'Clearly explains course requirements',
                              'Clear learning objectives & goals':'Explicit Learning Objectives & Goal',
                              'Instructor provides feedback to students to improve':'Constructive Feedback from Instructor', 
                              'Demonstrate importance of subject matter':'Demonstrates importance of subject matter',
                              'Explains subject matter of course':'Explanation of Course Content',
                              'Show respect for all students':'Shows respect for all students'})
    
    eval=eval.dropna(subset=['Course_Code','Division','Year'])      #https://www.w3resource.com/pandas/dataframe/dataframe-dropna.phpeval['Course_Code']=eval['Course_Code'].astype(int)
    eval=eval.set_index('Course_Code')                              #makes course_code the index   
    eval=eval[['Course_Name','Year', 'Semester', 'Instructor', 'Dept','Division', 'LoginID',
               'Hrs Per Week', 'Interest in student learning',
               'Clearly explains course requirements',
               'Explicit Learning Objectives & Goal',
               'Constructive Feedback from Instructor',
               'Demonstrates importance of subject matter',
               'Explanation of Course Content', 'Shows respect for all students',
               'Overall teaching rate', 'Overall course rate']]                 #reordered the columns
    eval['Instructor'] = eval['Instructor'].str.upper()                         #converts all faculty names to upper case
    eval['Year']=eval['Year'].astype(int)
    op=eval.loc[code]
   

    return op


   
    
def getHeinzCourseCatalog(course_num):
       
    #Go to the url 
    course_website = 'https://api.heinz.cmu.edu/courses_api/course_detail/' + course_num
    page = requests.get(course_website)
   
    #Scraping:
    
    #Parse the page
    soup = BeautifulSoup(page.content, 'html.parser')
    
   # Pulls the entire html file for the specific course number 
    course_page = soup.find(id="container-fluid")
  

    #Checks if the course number is a real course number
    if course_page == None: 
        print("Error - Course Number Does Not Exist")
        return 
       
    #Pulls the section header html code for Units, Description, Learning Outcomes, Prereqs and Syllabus
    course_elements= course_page.find_all("p")
    course_features = []
    for element in course_elements:
        header = element.get_text()
        course_features.append(header)
    
    #Assigning the list to variable names
    class_name = course_features[0]
    #removing class name from course_features
    course_features = course_features[1:]
    
    desc_pattern = r'^(Description:)'
    course_units = ''
    course_loutcomes = 'None'
    course_prereqs = 'None'
    course_syl = 'None'
    syllabi = {} #empty dictionary for courses with syllabi
    pattern = '\([-0-9a-zA-z\s]*' #pattern for finding Professor names
    
    #Extracts the relevant information from the html code
    for feature in course_features:
        if 'Units' in feature:
            course_units = feature[-2:]
            course_units = int(course_units)
        elif re.search(desc_pattern,feature) != None:
           course_desc = feature[13:]
        elif 'Learning Outcomes:' in feature:
            course_loutcomes = feature[19:]
        elif 'Prerequisites Description:' in feature:
            course_prereqs = feature[26:]
            
        else:
            course_syl = feature
           
        
    #finds the information contained about syllabus on the course_page
    syllabus = course_page.select('a')
    
    
    #Is there a syllabus?
    if len(syllabus) == 0:
        syllabi[None] = 'None'
        
    #Is there only one syllabus?
    if len(syllabus) == 1:
        syllabus_link = 'https://api.heinz.cmu.edu' + syllabus[0].get('href')
        str_syllabus = str(syllabus)
        syllabus_prof = re.findall(pattern, str_syllabus)
        string = syllabus_prof[0]
        string = string[1:-1]
        string = string.split(' ')
        string = string[1] + ', ' + string[0]
        syllabi[string] = syllabus_link
        
    #Is there more than one syllabus?
    if len(syllabus) > 1: 
        for syl in syllabus:
            syllabus_link = 'https://api.heinz.cmu.edu' + syl.get('href')
            str_syl = str(syl)
            syllabus_prof = re.findall(pattern, str_syl)

            string = syllabus_prof[0]
            string = string[1:-1]
            string = string.split(' ')
            string = string[1] + ', ' + string[0]
          
            syllabi[string] = syllabus_link
            
            
    #For the syllabi, what semester are they for?
    
   
    #Pulls together all of the information generated in this function into a list
    course_details = [course_num, class_name, course_units, course_desc, course_loutcomes, course_prereqs, course_syl, syllabi]
    return course_details



#Just gets the number of the menu option that is selected
def menu():

 
#Step 3: If a valid course number is inputted, prompt the user for more information.
    request = input('''Please type in the number for the menu item that you want:
                    0: Quit 
                    1: Course Time & Instructor for Each Time
                    2: Department Code for the Course
                    3: Course Evaluation Information
                    4: Course Overview (Course Name, Description, and # of Units)
                    5: All Course Information
                    6: Course Syllabi
                    7: Request a New Course Number
                    8: Comparison of Two Different Course ''' )

#Step 4: Change the inputted string value to an integer value
    request_code = int(request)

#Step 5: Create a list of integers with the range of allowable values for the menu
#creates list of allowable menu options
    menu_options = [i for i in range(9)]

#Step 6: Is the inputted menu option valid?
    while request_code not in menu_options:
        print("Error - please enter a valid menu option.")
        request = input('''Please type in the number for the menu item that you want:
                        0: Quit 
                        1: Course Time & Instructor for Each Time
                        2: Course Department
                        3: Course Evaluation Information
                        4: Course Overview (Course Name, Description, and # of Units)
                        5: All Available Course Information
                        6: Course Syllabi
                        7: Request a New Course Number
                        8: Comparison of Two Different Course''' )
        request_code = int(request)




    return request_code



#Takes the menu option selected, and the course_num and returns the desired information
def menu_execution(course_num,request_code):
    

#Step 7: Pull the requested information

    #Allows the user to quit
    if request_code == 0:
        print("\n Thanks for using our platform! Have a good day!")
        return 

    if request_code == 1: 
        request1(course_num)
        option = menu()
        menu_execution(course_num,option)
        
    if request_code == 2: 
        request2(course_num)
        option = menu()
        menu_execution(course_num,option)
    
    if request_code == 3: # Pulls Course Evaluation 
        #removes the “-” character in the course number 
        new_course_num = course_num[0:2] + course_num[3:]
        
        #Gets the location for where the course_evaluation file is downloaded on the user's coputer
        path=input('Enter path for the csv file for Course Evaluation: ')   
   
        #Pulls your requested course_evaluation information
        #add  a try/except loop here to check for the existing file path
        eval = csv_func(new_course_num, path)  
        print(eval)
        #Semester, Year, Instructor, Overall Course Rate
        
        option = menu()
        menu_execution(course_num,option)
        

     
    if request_code == 4: # Course Overview (Course Name, Description, and # of Units)
        course_catalog_info = getHeinzCourseCatalog(course_num)
        if course_catalog_info == None:
            print('Sorry, the course you requested information for does not exist')
          #  menu()
        if course_catalog_info != None:
            course_overview = [course_catalog_info[1], course_catalog_info[3], course_catalog_info[2]]
        print('''Course Overview:
                 Course Number: %s
                 Course Name: %s
                 Course Description: %s
                 Course Units: %d
              ''' % (course_num, course_overview[0], course_overview[1], course_overview[2]))
        option = menu()
        menu_execution(course_num,option)

    if request_code == 5: #All Available Course Information
        course_catalog_info = getHeinzCourseCatalog(course_num)
           
        if course_catalog_info == None:
            print('Sorry, the course you requested information for does not exist')
            option = menu()
            menu_execution(course_num,option)
        else:
            print('All Available Course Information:')
            for i in range(len(course_catalog_info)):
                print(course_catalog_info[i])
                #print('All Course Information: %' % (course_catalog_info))
            request2(course_num)    
            request1(course_num)
            #request3(course num) once this function is ready
            option = menu()
            menu_execution(course_num,option)

    if request_code == 6: 
        course_catalog_info = getHeinzCourseCatalog(course_num)
        if course_catalog_info == None:
            print('Sorry, the course you requested information for does not exist')
            menu()
        syllabi = course_catalog_info[-1]
        if None in syllabi.keys():
            print('There are no available syllabi for this course')
        else:
            print('''\n Here is a list of all available syllabi for this course, and the corresponding professors: \n''')
            for key in syllabi:
                print(key + ': ' + syllabi[key])
        option = menu()
        menu_execution(course_num,option)
    if request_code == 7:  # Enter a new course number
        main()
    #if request_code == 8: #Compare course evaluations
        #course_num2 = input('Enter another course number in the valid format (XX-XXX) whose evaluations you would like to compare with the course ' + course_num)
        #option = menu()
        #menu_execution(course_num,option)
 
# Define menu request functions
 
    # Request 1 pulls section info (time, instructor, location, etc.) from Schedule of Classes (fall 2019)
def request1(course_num):
    if course_num not in schedule.index:
        print('Sorry, there is no schedule information for this course in Fall 2019')
    else:
        name = schedule.loc[course_num]['name']
        lectures = schedule.loc[course_num]['lectures']
        days_dict= {1: 'Monday', 2: 'Tuesday', 3: 'Wednesday', 4: 'Thursday', 5: 'Friday'}
        print('Times and Instructor(s) for %s:' %(name))
        for lecture in lectures:
            print(lecture['instructors'][0])
            print('\t Section: %s' %(lecture['name']))
            for time in lecture['times']:
                print('\t Day(s): %s' %((', ').join(list(map(lambda x: days_dict[x], time['days'])))))
                print('\t Time: %s - %s' %(time['begin'], time['end']))
                print('\t Location: %s %s' %(time['building'], time['room']))
                print('\t Campus: %s' %(time['location']))
    
    # Request 2 pulls department name from Schedule of Classes (fall 2019)
def request2(course_num):
    if course_num not in schedule.index:
        print('Sorry, there is no department information for this course')
    else:
        department = schedule.loc[course_num]['department']
        print('Course Department:')
        print(department)

# Need to put request 3 info into a function in order to call for request 5
#def request3(course_num):

def main():
    
    
    #Step 1: Ask the user for a course number
    course_num = input('''Welcome to the Golden Girls Course Searching Platform! To get started, please enter a course number (XX-XXX): ''')


    # Step 2: Is this a valid format for a course number?
    #pattern is the allowable format for a course_num
                   
    pattern = r'^([0-9][0-9])\-([0-9]{3})$'
    while re.search(pattern, course_num) == None:        
        print('Error - Please enter a valid format for a course number')
        course_num = input('''Welcome to the Golden Girls Course Searching Platform! To get started, please enter a course number (XX-XXX): ''')
        
   # Gets the menu option and the course_num
    menu_execution(course_num,menu())
    
   
  
    
#Controls the number of times that this code is run by checking if the .json already exists
if path.exists("filtered_courses.json") == False:
    
          
  #Connect to ScottyLabs API - This should only be done as few times as possible!
    response = requests.get("https://apis.scottylabs.org/course/courses")
    print(response.status_code)

    all_courses = json.loads(response.text)

    #Retrieve only courses that start with the number 9
    filtered_courses = [course for course in all_courses if course['courseID'].startswith('9')]

    with open("filtered_courses.json", "w") as f:
        json.dump(filtered_courses, f) 
    #Read json file into dataframe    
    schedule = pd.read_json("filtered_courses.json")
    
    #Keep only Heinz courses (course numbers prefixes between 90 and 95)
    pattern= r'^[9][0-5]'   
    schedule_filtered = schedule[schedule['courseID'].str.contains(pattern)]
 
    ##Deleting unnecessary columns
    #drop co-reqs column
    schedule_filtered.drop('coreqs', axis=1, inplace=True)
    #drop description
    schedule_filtered.drop('desc', axis=1, inplace=True)
    #drop prereqs
    schedule_filtered.drop('prereqs', axis=1, inplace=True)
    #drop units
    schedule_filtered.drop('units', axis=1, inplace=True)
    
    #Set index to Course ID
    schedule = schedule_filtered.set_index('courseID') 
else: 
    
    #Read json file into dataframe    
    schedule = pd.read_json("filtered_courses.json")
    
    #Keep only Heinz courses (course numbers prefixes between 90 and 95)
    pattern= r'^[9][0-5]'   
    schedule_filtered = schedule[schedule['courseID'].str.contains(pattern)]
 
    ##Deleting unnecessary columns
    #drop co-reqs column
    schedule_filtered.drop('coreqs', axis=1, inplace=True)
    #drop description
    schedule_filtered.drop('desc', axis=1, inplace=True)
    #drop prereqs
    schedule_filtered.drop('prereqs', axis=1, inplace=True)
    #drop units
    schedule_filtered.drop('units', axis=1, inplace=True)
    
    #Set index to Course ID
    schedule = schedule_filtered.set_index('courseID') 
    

    
    
if __name__ == '__main__': 
    main() 


