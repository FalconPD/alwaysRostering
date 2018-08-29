# Roles

alwaysRostering has methods can create queries for various roles commonly used in subscription services.  These queries are for active staff or students. Staff roles are: Staff, Teacher, Admin, Sysadmin, or Student.

## Staff: staff() (filtered by job code)

All active staff that currently have a State ID. This filters out shared teachers.

## Teacher: teachers() (filtered by job code)

* 1001: Elementary Kindergarten - 8th Grade
* 1003: Kindergarten
* 1004: Elementary School Teacher K-5
* 1007: Elementary Teacher in secondary setting
* 1015: English/Elementary
* 1017: Science/Elementary
* 1018: Social Studies/Elementary
* 1102: Mathematics Grades 5-8
* 1103: Science Grades 5-8
* 1104: Social Studies Grades 5-8
* 1106: Language Arts/Literacy Grades 5-8
* 1150: Spanish Grades 5-8
* 1200: Art
* 1273: Cinema/TV Production
* 1283: Photography/Technical
* 1301: Business Organization
* 1308: Economics/Economic Geography
* 1315: Business Law
* 1317: Marketing/Sales
* 1331: Bookkeeping Accounting
* 1345: Clerical Office Practices
* 1401: English Non-Elementary
* 1485: English as a 2nd Language
* 1500: Language Arts/Literacy
* 1510: French
* 1530: Italian
* 1540: Latin
* 1550: Spanish
* 1607: Health & Physical Education
* 1630: Physical Education
* 1700: Family & Consumer Sciences - Comprehensive
* 1706: Family & Consumer Sciences - Child & Family Development
* 1760: Family & Consumer Sciences - Foods / Nutrition & Food Service
* 1805: Career Education
* 1812: General Shop
* 1821: Drafting adn Design Technology
* 1856: Electronics
* 1897: Technology Education
* 1901: Math Non-Elementary
* 1962: Computer Literacy/Applications/Programming
* 2100: Music Comprehensive
* 2110: Music Instrumental
* 2130: Music Vocal
* 2202: Science General
* 2206: Science Physical
* 2231: Science Biological
* 2235: Science Chemistry
* 2236: Science Physics
* 2302: Social Studies Non-Elementary
* 2322: Social Students History
* 2400: Supplementary Instruction (In-Class)
* 2401: Supplementary Instruction (Pull-Out)
* 2405: Resource Program In-Class
* 2406: Resource Program Pull-Out Support

## Admin: admins() (filtered by job code)

* 0102: Superintendent
* 0122: Assistant Superintendent
* 0201: High School Principal
* 0202: Assistant High School Principal
* 0221: Middle School Principal
* 0222: Assistant Middle School Principal
* 0231: Elementary School Principal
* 0232: Assistant Elementary Principal
* 0306: Supervisor PPS
* 0310: Supervisor Athletics
* 0312: Supervisor Art 
* 0314: Supervisor English
* 0315: Supervisor Foreign Languages
* 0319: Supervisor Mathematics
* 0321: Supervisor Music
* 0322: Supervisor Science
* 0324: Supervisor Special Education
* 0399: Supervisor Special Projects
* 0524: Director Special Ed
* 2410: Teacher Coach

## System Admin: sysadmins() (filtered by job code and manually added)

* 9200: Technicians
* Director of Information Technology
* Educational Technology Facilitator

## Students: students()

All active, in-district students
