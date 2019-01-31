import asyncio
import csv

from AR.education_city.tables import Base, Student, Teacher, Admin

class DownloadMixin():
    """
    Handles downloading and creating DB from the info in Genesis
    """
    async def _csv_to_db(self, user_type, cls):
        """
        Gets a CSV file for a user type and loads the result in the DB
        """
        url = 'https://ec2.educationcity.com/user_management/exportCSV'
        resp = await self.post(url, data={'userType': user_type})
        text = await resp.text(encoding='utf-8-sig')
        reader = csv.reader(text.splitlines())
        header = next(reader)
        assert header == cls.csv_header
        for row in reader:
            self.db_session.add(cls.from_csv(row)) 
        
    async def download(self):
        """
        Downloads all tables from Education City and creates a database
        """
        # Create the tables in our sqlite db
        Base.metadata.drop_all(self.engine)
        Base.metadata.create_all(self.engine)

        # Create tasks to download and import the info
        tasks = []
        for user_type, cls in [('Students', Student), ('Teachers', Teacher),
            ('Administrators', Admin)]:
            tasks.append(self.loop.create_task(self._csv_to_db(user_type, cls)))
        await asyncio.gather(*tasks)
