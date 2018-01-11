# Genesis

## getReports.js

Downloads [reports](../docs/reports.md) from Genesis that are used by the other scripts to get information about current students, teachers, classes, and schools.

*NOTE:*You must have curl installed for this to work. Large file downloads don't work well in casperjs, so curl is used instead.

## get_reports.py

Downloads [reports](../docs/reports.md) from Genesis that are used by other scripts to get information about current students, teachers, classes, and schools. This version runs asynchronously in python and is significantly faster than the previous version.
