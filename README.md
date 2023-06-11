# Heinz Course Search Platform

The purpose of this program is to allow users to search for and view Heinz course information across three sources: Heinz course catalog, Schedule of Classes, and Faculty Course Evaluations.

## Initializing

### Course Evaluation Data

Prior to using the program, the user will need to retrieve one data source: a csv file containing faculty course evaluations. The csv can be accessed in the repo or can be downloaded from the SmartEvals site through the following steps:
1. Go to this [website](https://www.smartevals.com/Reporting/Students/Results.aspx?Type=Instructors&ShowAll=Chosen) and select Carnegie Mellon University.
2. Select ‘Search by Instructor’ and ‘Heinz College’.
3. As the source evaluations page opens, select the icon on the top left corner to export to CSV and initiate a download.

After downloading, save this file in the same directory as this project code file. Make sure that the file name is `Course_Evaluation_Results.csv`

### Program File

1. Open the program file `goldengirls_finalproject_vfinal.py`
2. If any of the packages used in this file are not installed, type “pip install packagename” to install. The packages used in this program are:
* pandas
* json
* requests
* bs4
* re
* sys
* Os.path (from os import path)

3. The platform is ready for use when the message: “ Welcome to the Golden Girls Course Searching Platform! To get started, please enter a course number (XX-XXX)” appears on the screen.
4. The program can also be opened and run in the Spyder interpreter, click the green run file button to start the program.

## Using the program

After the welcome message of “Welcome to the Golden Girls Course Searching Platform! To get started, please enter a course number (XX-XXX)” enter any Heinz course number in the format “XX-XXX”. If a course number is not entered in the correct format, the user will receive an error message and be prompted to enter a course number again.

Entering a correct course number will return the following menu:

* 0:  Quit 
* 1: Course Time & Instructor for Each Time
* 2: Department Code for the Course
* 3: Course Evaluation Information
* 4: Course Overview (Course Name, Description, and # of Units)
* 5: All Course Information
* 6: Course Syllabi
* 7: Request a New Course Number
* 8: Comparison of Two Different Course

The user should type the corresponding number for the menu item they would like to perform. If the user does not enter a valid menu item number, they will receive an error message and the menu will appear a second time prompting the user to try again.

## Menu Options

Below is a description of each of the eight menu options.

*0:  Quit* 
Entering 0 will display the message “Thanks for using our platform! Have a good day!” and close the program. The user should enter this option when they are finished using the program.

*1: Course Time & Instructor for Each Time*
This option displays the Schedule of Classes course information for the course number entered. It includes the following information:
* Instructor
* Section
* Days the course is taught
* Start time and end time
* Building code and classroom number
* Campus
All sections of the course being offered will be displayed separately. Note that this option currently only returns schedule information for classes offered in the Fall 2019 semester. If the course is not offered in Fall 2019, the user will receive the error message “Sorry, there is no schedule information for this course in Fall 2019.” After receiving the course information or an error message, the user will be prompted to select another menu option.

*2: Department Code for the Course*
Option 2 will return the specific Heinz school in which the course is offered. For example, the option may return “School of Public Policy & Management” or “School of Information Systems & Management.” This information is tied to the Schedule of Classes so if the course is not offered in Fall 2019, the user will receive the error message “Sorry, there is no department information for this course.” The menu will appear again after the user receives the department information or error message.

*3: Course Evaluation Information*
This option will return the faculty course evaluation information for every semester and instructor of the course taught from 2017 to Spring 2020. The information returned includes:
Course Name
Year
Semester (Fall/Spring)
Instructor
Department Code
Hours per week
Overall teaching rating
Overall course rating
The menu will appear again so that the user may section another option after returning the course evaluation information. If there is no course evaluation data for the selected course number, the user will receive the error message “Sorry, the information you requested does not exist” and will be prompted to select another menu option.

If the user has not saved the “Course_Evaluation_Results.csv” in the same directory as the program file or has named the file differently, the program will display an error message and close when the user tries to access menu option #3. It will do the same for the other menu options that return course evaluation information such as menu option #5 and menu option #8. 

*4: Course Overview (Course Name, Description, and # of Units)*
Menu option 4 returns the following information from the Heinz Course Catalog:
Course Name
Course Description
Number of units
The menu will appear again after returning the course information. If the course number does not exist in the Heinz Course Catalog, the user will receive an error message and be prompted to enter a new menu option.

*5: All Course Information*
This option returns all course information contained in Menu item #1 (schedule information), Menu item #2 (department name), Menu item #3 (Faculty course evaluations), and Menu item #4 (Course overview). Additionally, the course learning outcomes, course prerequisites, and course syllabi (if available) from the Heinz Course Catalog will be displayed. If any of the above information is not available, a message displaying it is not available will appear in its place. After returning the course information, the menu will appear again allowing the user to select another option.

*6: Course Syllabi* 
If course syllabi are available, this option will return the link to the syllabus for each of the instructors who have posted a syllabus. If there are no syllabi available for the course, the user will receive the message “There are no available syllabi for this course” and the menu will appear again so that the user may enter another option.

*7: Request a New Course Number*
Users should select this option if they would like to see information for a different course number than the one they initially entered. After selecting option 7, the user will be prompted to enter a new course number in the format “XX-XXX”. If they do not enter the number in the correct format, they will be prompted to enter the course number again. After entering a valid course number, the full menu will appear.

*8: Comparison of Two Different Course*
This option allows the user to compare Faculty Course Evaluation information for two different course numbers. When the user selects this option the current course number that has been entered will appear as the first course to compare, and the user will be prompted to enter another course number (format should be XX-XXX). This menu option will then return the faculty course evaluation information for both courses (see menu item #3 for details on specific information returned). If any of the course numbers do not have course evaluation information, there will be a message indicating that information does not exist. The menu will appear again after the information is returned so the user can select another option.
