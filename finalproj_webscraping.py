#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 21 23:58:46 2020

@author: tobijegede
"""

#importing the modules 
import pandas as pd
#import tkinter
import requests
from bs4 import BeautifulSoup
import re


#To do:
# look at the HTML code for the Heinz Course Catalog Website 
# import tkinter (think about creating a GUI?)
# look up information about GitHub
# Include code that checks whehter one of the desired fields is empty (!!!)


def getHeinzCourseCatalog(course_num):
    #Trial Course Numbers to Use: 
        #'90-717' (Writing for Public Policy)
        #'90-819' (Intermediate Programming with Python)
        #'94-806' (Privacy in the Digital Age)    
    
    #Is the course number provided valid?
    pattern = r'^([0-9][0-9])\-([0-9]{3})$'
    if re.search(pattern, course_num) == None:        
        print('Error - Please enter a valid format for a course number')
        return 
     
    #Go to the url 
    course_website = 'https://api.heinz.cmu.edu/courses_api/course_detail/' + course_num
    page = requests.get(course_website)
    #Scraping:
    
    #Parse the page
    soup = BeautifulSoup(page.content, 'html.parser')
    
   # Pulls the entire html file for the specific course number 
    course_page = soup.find(id="container-fluid")
  
    #prints the entire html file
    #print(course_page)

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
   # print(course_features)
    
    #Assigning the list to variable names
    class_name = course_features[0]
    #print(class_name)
    #removing class name from course_features
    course_features = course_features[1:]
    #print(course_features)
    #for feature in course_features:
     #   class_name = feature
    desc_pattern = r'^(Description:)'
    course_units = ''
    course_loutcomes = 'None'
    course_prereqs = 'None'
    course_syl = 'None'
    #mult_links = [] #no longer need this since syllabus column will be dictionaries
    syllabi = {} #empty dictionary for courses with syllabi
    pattern = '\([-0-9a-zA-z\s]*' #pattern for finding Professor names
    for feature in course_features:
        if 'Units' in feature:
            course_units = feature[-2:]
            course_units = int(course_units)
        elif re.search(desc_pattern,feature) != None:
           course_desc = feature[13:]
           #print(course_desc)
        elif 'Learning Outcomes:' in feature:
            course_loutcomes = feature[19:]
           # print(course_loutcomes)
        elif 'Prerequisites Description:' in feature:
            course_prereqs = feature[26:]
            #print(course_prereqs)
            
        else:
            course_syl = feature
           # print(course_syl)
            #Course Syllabus Header & Text
        
            #finds, prints, and formats the information contained about syllabus on the course_page
    syllabus = course_page.select('a')
    #print(syllabus)
    
            #Is there a syllabus?
    if len(syllabus) == 0:
        #mult_links.append('None') #no longer need this since syllabus column will be dictionaries
        #print("There is no syllabus available for this class.")
        syllabi[None] = 'None'
    if len(syllabus) == 1:
        syllabus_link = 'https://api.heinz.cmu.edu' + syllabus[0].get('href')
        str_syllabus = str(syllabus)
        syllabus_prof = re.findall(pattern, str_syllabus)
        #print(syllabus_prof)
        string = syllabus_prof[0]
        string = string[1:-1]
        string = string.split(' ')
        string = string[1] + ', ' + string[0]
        #print(string)
        syllabi[string] = syllabus_link
        #mult_links.append(syllabus_link)
        #print('There is %d syllabus available for this class. \nHere is the link to the syllabus: %s '
               #% (len(syllabus), syllabus_link))
             #Is there more than one syllabus?
    if len(syllabus) > 1: 
        for syl in syllabus:
            syllabus_link = 'https://api.heinz.cmu.edu' + syl.get('href')
            str_syl = str(syl)
            syllabus_prof = re.findall(pattern, str_syl)
            #print(syllabus_prof)
            string = syllabus_prof[0]
            string = string[1:-1]
            string = string.split(' ')
            string = string[1] + ', ' + string[0]
            #print(string)
            syllabi[string] = syllabus_link
            #mult_links.append(syllabus_link)
            #print('There are %d syllabi available for this class. \nHere are the links to the syllabi: %s '
                  #% (len(syllabus), mult_links))
            
            #If syllabus, for what semester? & for what professor?
    
    #Return to the main function to ask for another course number 
    # main()
    
    course_details = [course_num, class_name, course_units, course_desc, course_loutcomes, course_prereqs, course_syl, syllabi]
    return course_details

#getHeinzCourseCatalog('90-717')

'''Creating a DataFrame of a list of courses'''
data = [] #will be a list of lists that's used to append course object returned from function
courses = pd.DataFrame(columns = ['Course Nubmer', 'Name', 'Units', 'Description', 'Outcomes', 'Prerequisites', 'Syllabus', 'Link']) #empty data frame with named columns
course_num = ['90-717', '90-819', '94-806'] #used as a trial list of courses
for num in course_num: #loop to append course information to data object
    course = getHeinzCourseCatalog(num)
    data.append(course)
for obj in data: #loop to add rows to dataframe; each index is named by the course number
    courses.loc[obj[0]] = obj
    


# Potential new function
'''def whichCourseisBetter(course1, course2):
    course1_rating = 
    course2_rating = 
    if  df[course1].averagerating > df[course2].averagerating:
        print('%s is a higher-rated course than %s \n', 
              %(course1, course2))'''




def main():
    course_num = input('Please type in a course number (XX-XXX). Enter "quit" to stop searching: ')
    if course_num.lower() != 'quit':
      course_info = getHeinzCourseCatalog(course_num)
     # print(course_info)
      if course_info == None or len(course_info) == 0:
          print("There is no such class")
        
      else: 
          for i in course_info:
              print(i)

    else:
        print("Enjoy your day! Thanks for stopping by!")
   #Do I need a list of valid course numbers --- before the retrevial process?
        
    
    
    
if __name__ == '__main__': 
    main() 
    
    
    