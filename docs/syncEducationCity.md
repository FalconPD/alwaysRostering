# Education City

## Overview
Education City is licensed per school and contains content for Grades K-6. It is sold through Edmentum and is currently in use in three schools in the district:
* Barclay Brook - Grades K-2
* Mill Lake - Grades K-3
* Oak Tree - Grades K-3

## Login Credentials
These accounts are currently set up to use the [Eliot login format.](Eliot.md)

## Technical Details
Each school has its own set of login credentials. The script iterates over each of them and loads the appropriate grades and students for that school. Most of the information is passed via json POST and GET requests with some regular POSTs thrown in for good measure. Other than logging in, DOM manipulation is not used. The basic steps followed are:
1. Get a list of students from Education City
2. Check to see which students aren't on our report and delete them
3. Check to see which students are on our report but not in Education City and upload them using the bulk_import function. This will add classes as well if the class doesn't yet exist.
4. Get a list of classes from Education City
5. Check to see which students have different information in Education City than in our report and update them

   This is by far the most complex operation. The Education City user_defined_id is our link to the Genesis student id. From there we can check to see if anything has changed. We don't bother reseting passwords, so that if teachers / students decide to change them, they stay the way they are. In some cases new classes have to be added before a student can be updated. We create a list of all the classes and students we have to add and then process each list one item at a time. Each item is its own request, so this goes rather slowly. It will be interesting to see how this works at the beginning of the year when the grades are incremented.

5. Get a list of classes from Education City, the previous step may have changed them.
6. Delete any classes that have no active students in them.
7. Get a list of teachers from Education City.
8. Check to see which teachers aren't on our report and delete them
9. Check to see which teachers are on our report but not in Education City and upload them using the validateUserList function.

   This seems to be setup to work with CSV data and is the way Education City handles its teacher uploads on the website. There is no reason to have an update teacher step because there are so few fields for a teacher. Teachers are referenced by their username as there is no field in validateUserList for user_defined_id although that does show up in the user object after the teacher is created.
