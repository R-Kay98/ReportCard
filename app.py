import csv
import sys
import json

class Student:
    
    def __init__(self, student_id, student_name):
        self.student_id = student_id
        self.student_name = student_name
        self.averageGrade = 0
        self.courses = {}
        
    def addCourse(self, course_id, test_id, markVal, courseDict):
        '''
            Despite the name, the function's final purpose is to add a single test (containing a mark)
            to a particular course. If the course doesn't exist yet, it will be created. If it does, the
            addTest method will be called on one of the student's course instances to add the score.
            
            INPUTS
                course_id : str, mandatory
                    Unique identifier for the course for which the student received the particular mark in.
                test_id : str, mandatory
                    Unique identifier for the test for which the student received the particular mark in.
                markVal : int, mandatory
                    Mark the student received on the test with the corresonding test_id.
                courseDict : dictionary, mandatory
                    A dictionary containing class instances of all the courses offered, along with their tests.
            
            RETURNS
                None.
        '''
        
        course = courseDict[course_id]
        if course_id not in self.courses.keys():
            newCourse = Course(course.course_id, course.course_name, course.course_teacher)
            newCourse.validCourseWeights = course.validCourseWeights
            self.courses[course_id] = newCourse
        self.courses[course_id].addTest(course_id, test_id, markVal, courseDict)
            
    def findAverageGrade(self):
        '''
            This function will add up all the students course grades for each particular course and find the
            final average grade. The class instance's average grade will be set to this value.
            
            INPUTS
                None.
            
            RETURNS
                None.
        '''
        
        counter = 0
        for key, value in self.courses.items():
            self.averageGrade += float(value.course_grade)
            counter += 1
        if counter != 0:
            self.averageGrade = self.averageGrade/counter
            self.averageGrade = round(self.averageGrade, 2)
            
class Course:
    
    def __init__(self, course_id, course_name, course_teacher):
        self.course_id = course_id
        self.course_name = course_name
        self.course_teacher = course_teacher
        self.course_grade = 0
        self.validCourseWeights = False
        self.tests = {}

    def addTest(self, course_id, test_id, markVal, courseDict):
        '''
            The test from the course instance's 'tests' dictionary with unique identifier 'test_id' will
            have it's mark value set to markVal (the student's score on the test). If the test doesn't exist,
            it will first be created prior to setting the markVal.
            
            INPUTS
                course_id : str, mandatory
                    Unique identifier for the course for which the student received the particular mark in.
                test_id : str, mandatory
                    Unique identifier for the test for which the student received the particular mark in.
                markVal : int, mandatory
                    Mark the student received on the test with the corresonding test_id.
                courseDict : dictionary, mandatory
                    A dictionary containing class instances of all the courses offered, along with their tests.
            
            RETURNS
                None.
        '''
        
        test = courseDict[course_id].tests[test_id]
        if test_id not in self.tests.keys():
            newTest = Test(test.test_id, test.test_weight)
            self.tests[test_id] = newTest
        self.tests[test_id].mark = markVal

    def findCourseGrade(self, student_id):
        '''
            This function will find the course grade for this particular course instance which
            corresponds to a particular student. This is done by iterating over it's tests and
            calculating the weighted score.
            
            INPUTS
                student_id : str, mandatory
                    Unique identifier for the student whose course grade we want to determine.
            
            RETURNS
                None.
        '''
    
        for key, value in self.tests.items():
            self.course_grade += (float(value.mark)*float(value.test_weight))/100
            self.course_grade = round(self.course_grade, 1)

class Test:
    
    def __init__(self, test_id, test_weight):
        self.test_id = test_id
        self.test_weight = test_weight
        self.mark = 0

def writeJSONOutput(students, myJSON, pathToOutput):
    
    '''
        This function will write the JSON output containing the student's course and test grades.
        The output is exactly that of the sample file.
        
        INPUTS
            students : dict, mandatory
                Dictionary containing all the student class instances which contains 
            myJSON : dict, mandatory
                Initially a dictionary format, this will contain the entirety of the desired output
                with regards to the student/course/test information. This will then be converted into
                a JSON file.
            pathToOutput : str, mandatory
                Path to the file where want the JSON data to be dumped to.
        
        RETURNS
            None.
    '''
    
    counter = 0
    myJSON['students'] = []
    
    for k1, v1 in students.items():
        myJSON['students'].append({})
        myJSON['students'][counter]['id'] = int(v1.student_id)
        myJSON['students'][counter]['name'] = v1.student_name
        myJSON['students'][counter]['totalAverage'] = v1.averageGrade
        myJSON['students'][counter]['courses'] = []
        counterTwo = 0
        for k2, v2 in v1.courses.items():
            myJSON['students'][counter]['courses'].append({})
            if v2.validCourseWeights == False:
                myJSON['students'][counter]['courses'][counterTwo]['error'] = 'Invalid course weights'
                continue
            myJSON['students'][counter]['courses'][counterTwo]['id'] = int(v2.course_id)
            myJSON['students'][counter]['courses'][counterTwo]['name'] = v2.course_name
            myJSON['students'][counter]['courses'][counterTwo]['teacher'] = v2.course_teacher
            myJSON['students'][counter]['courses'][counterTwo]['courseAverage'] = v2.course_grade
            counterTwo += 1
        counter += 1
    
    with open(pathToOutput, 'w', encoding='utf-8') as f:
        json.dump(myJSON, f, ensure_ascii=False, indent=2)

def main():
    
    students = {}
    courses = {}
    tests = {}
    
    pathToCourses = sys.argv[1]
    pathToStudents = sys.argv[2]
    pathToTests = sys.argv[3]
    pathToMarks = sys.argv[4]
    pathToOutput = sys.argv[5]
    
    with open(pathToStudents, 'r') as file:
        reader = csv.reader(file)
        next(reader, None)
        for row in reader:
            if len(row) != 2:
                continue
            student_id = row[0]
            student_name = row[1]
            students[student_id] = Student(student_id, student_name)
    
    with open(pathToCourses, 'r') as file:
        reader = csv.reader(file)
        next(reader, None)
        for row in reader:
            if len(row) != 3:
                continue
            course_id = row[0]
            course_name = row[1]
            course_teacher = row[2]
            courses[course_id] = Course(course_id, course_name, course_teacher)
            
    with open(pathToTests, 'r') as file:
        reader = csv.reader(file)
        next(reader, None)
        for row in reader:
            if len(row) != 3:
                continue
            test_id = row[0]
            course_id = row[1]
            course_weight = row[2]
            courses[course_id].tests[test_id] = Test(course_id, course_weight)
            tests[test_id] = course_id
    
    '''
        Here we are performing a check on all the test weights for a particular course. If they don't add to 100, a flag
        will be set and the data will not be outputted for that particular course.
    '''
    
    for key, value in courses.items():
        totalWeights = 0
        for k2, v2 in value.tests.items():
            totalWeights += int(v2.test_weight)
        if totalWeights == 100:
            courses[key].validCourseWeights = True
    
    with open(pathToMarks, 'r') as file:
        reader = csv.reader(file)
        next(reader, None)
        for row in reader:
            if len(row) != 3:
                continue
            test_id = row[0]
            student_id = row[1]
            markVal = row[2]
            course_id = tests[test_id]
            students[student_id].addCourse(course_id, test_id, markVal, courses)
    
    '''
        With the data all parsed and the class instances organized and build, we will now find find/calculate the appropriate
        grade information.
    '''
    
    for k1, v1 in students.items():
        for k2, v2 in v1.courses.items():
            students[k1].courses[k2].findCourseGrade(k1)
        students[k1].findAverageGrade()
    
    writeJSONOutput(students, {}, pathToOutput)
    
if __name__ == '__main__':
    main()     