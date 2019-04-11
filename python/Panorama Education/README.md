# roster.py

Creates a roster with student information (including sepcial ed status, ell
status, free and reduced lunch status, and TAG). Formatting follows the
[https://panorama-www.s3.amazonaws.com/library/Data%20File%20Guide%20for%20Staff%20Surveys%20or%20Staff%20SEL%20Measures.pdf](Data File Guide for Staff Surveys).

## 3-5

Students a linked to their homeroom teacher(s) with class name being the HR
teacher(s) name(s).

## 6-12

Students are linked to all the teachers in their schedule with the class name
being the block day and course decription for HS classes or the period and
course description for MS classes. Classes with multiple teachers are detected
and all students are rostered for each teacher. Classses that do not have a
teacher, early out at MTHS, or classes that have a placeholder teacher, STAFF
STAFF for lunches at MTMS, are not be rostered.

## NOTES

Homebound students without schedule information or homeroom teachers are still
rostered with that information being left blank.
