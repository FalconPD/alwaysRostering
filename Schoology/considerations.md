# Considerations for Genesis / Schoology Integration

When developing our current Schoology integration we encountered a lot of
special scenarios that had to be dealt with. It would be helpful to know
how the Genesis integration would handle these
 
## Homerooms vs. Scheduled Courses

K-3 students do not have scheduled classes. Currently, K-3 students are put in
a Schoology class based on their homeroom teacher(s) listed in their
demographic information.

4-12 students have scheduled classes and each academic class (not lunch, early
out, etc.) is set up in Schoology.

## Merged Rosters

Non-scheduled homerooms may be listed under a shared teacher that is made up of
multiple teachers. In that case all teachers and students are put in the same
class.

Scheduled classes may actually be made up for two sections, an ICR section and
a regular ed section. So far we can only seem to detect this by checking if the
gradebooks have been merged. In this case all students are put into one class
with both the ICR and regular education teacher.

## Grading Periods

Our district currently uses trimesters grades K-3 and quarterly marking periods
grades 4-12. There are also one semester courses that are taught for only half
the year. Currently grading periods are not synced up with the information in
Genesis and every class is listed under one manually created year-long grading
period. For the 2019-2020 School year we were hoping to sync grading periods
with the information in Genesis and set the grading periods for synced classes
accordingly.

## Half-day Kindergarten Teachers

Half-day kindergarten classes are listed under a teacher with AM or PM at the
end of their name (ex. "Mary Smith PM", "Mary Smith AM"). The current
integration looks up the actual teacher and rosters the students under a class
with either AM or PM at the end of it and the actual teacher as the teacher.

## Class Names

Class names are set up to convey useful information depending on the school.
For example the middle school uses periods, but the high school uses periods
and days. A middle school class may be *Period 7 Geometry* but a high school
class could be *3A Geoemetry*.

## Syncing Methodologies

The current integration uses the
[Schoology API](https://developers.schoology.com/api) and syncs everything (not
just changes) daily. Unfortunately this is a very slow process when dealing with
enrollments. We were planning to move to a file-based bulk upload for speed and
explore the feasibility change-only syncing. It would be helpful to know how the
Genesis integration performs syncing.

## Extra_Data_1 for Roles

Looking at the documentation it seems the Extra_Data_1 is used to specify a user
role in Schoology. Currently this is used in our system to specify the
userPrincipalName version of their email address. Would it be possible to use
another attribute?
