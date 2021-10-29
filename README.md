# ReportCard
CSV file parser that reads the following four files and compiles the information into a final reportCard as seen in the `out.txt` file.
* courses.csv: Contains a list of all available courses with the course name, course ID and teacher.
* marks.csv: Contains a list of all student marks with each mark containing a value, test_id and student ID.
* students.csv: Contains a list of all students with each entry having a student ID and student name.
* tests.csv: Contains a list of all the tests available with each entry having a test ID, course ID and weight.
* out.json: Contains JSON information of each student with all their courses, tests and marks organized and with averages calculated. 

## Getting Started

* Run the app script in the ReportCard directory with all four file paths, plus an output listed as arguments.
* `python app.py <pathToCourses>.csv <pathToStudents>.csv <pathToTests>.csv <pathToMarks>.csv <pathToOutput>.json`
