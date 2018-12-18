import xlrd
import datetime
import logging
import sys
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from AR.PG.tables import UserProfile
from AR.PG.tables import LearningPlan
from AR.PG.tables import Activity
from AR.PG.tables import ActivityFormat
from AR.PG.tables import Base
from AR.PG import constants

class DownloadMixin():
    """
    This mixin provides routines for downloading table data from PG
    """
    async def _get_tables(self, table_list, date1=None, date2=None):
        """
        Submits a POST request to download tables as an excel sheet, parses the
        result to follow the link, downloads the link and returns an xlrd book
        """
        base_url = 'https://www.mylearningplan.com/DistrictAdmin/'

        data = {
            'cbo_SelectDate1' : 0,
            'cbo_SelectDate2' : 0,
            'rad_FileFormat'  : 'Excel',
            'DownloadKey'     : 'Download'
        }

        for table in table_list:
            data["chk_" + table] = 'on'

        if date1 != None and date2 != None:
            data['cbo_DateLogic1'] = 'After'
            data['cbo_SelectDate1'] = 'dt_StartDate'
            data['SDate1'] = date1.strftime('%m/%d/%Y')
            data['cbo_DateLogic2'] = 'Before'
            data['cbo_SelectDate2'] = 'dt_StartDate'
            data['SDate2'] = date2.strftime('%m/%d/%Y')

        resp = await self.post(base_url + 'Download.asp', data=data)
        text = await resp.text()
        soup = BeautifulSoup(await resp.text(), 'html.parser')
        anchor = soup.select_one("a[href*=../Download/Download-]")
        if anchor == None:
            logging.error("Couldn't find download link in response:")
            logging.error(text)
            sys.exit(1)
        resp = await self.get(urljoin(base_url, anchor['href']))
        contents = await resp.read()
        book = xlrd.open_workbook(file_contents=contents)
        return book

    def _excel_to_db(self, book, sheet_name, orm_class):
        """
        Creates orm objects from excel sheets
        """
        sheet = book.sheet_by_name(sheet_name)
        rows = sheet.get_rows()
        next(rows) # skip the first row
        for row in rows:
            self.db_session.add(orm_class.from_row(row, book.datemode))

    async def download(self):
        """
        Downloads all tables from PG
        """
        # Create the tables in our sqlite db
        Base.metadata.drop_all(self.engine)
        Base.metadata.create_all(self.engine)

        # These tables are not dependent on a date range
        book = await self._get_tables(['UserProfile', 'ActivityFormats'])
        self._excel_to_db(book, 'UserProfile', UserProfile)
        self._excel_to_db(book, 'Activity_Formats', ActivityFormat)

        # These tables are dependent on a date range and can only be downloaded
        # in smaller chunks
        date1 = constants.START_DATE
        while date1 != constants.END_DATE:
            date2 = date1 + constants.TIMEDELTA
            if date2 > constants.END_DATE:
                date2 = constants.END_DATE
            book = await self._get_tables(['LearningPlan', 'Activities'],
                date1=date1, date2=date2)
            self._excel_to_db(book, 'LearningPlan', LearningPlan)
            self._excel_to_db(book, 'Activities', Activity)
            date1 = date2
