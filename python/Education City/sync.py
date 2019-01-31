import asyncio
import logging

import AR.AR as AR
from AR.tables import Student as GenesisStudent
import AR.credentials as credentials
import AR.education_city as edcity
from AR.education_city.tables import Student as ECStudent

async def sync(loop):
    school_code = 'MLS'
    async with edcity.Session(school_code, f'{school_code}.db', loop) as EducationCity:

        # Start downloading the current Education City database
        download_task = loop.create_task(EducationCity.download())
        await asyncio.sleep(0.25) # give the requests a chance to fire

        # Build images of what the users should be
        logging.debug("Building images...")
        students = []
        for genesis_student in (AR.students()
           .filter(GenesisStudent.current_school==school_code)
           .filter(GenesisStudent.grade_level.in_(['KH', 'KF', '01', '02', '03']))):
            students.append(ECStudent.from_genesis(genesis_student))

        await download_task

#        for ec_student in students:
#            print(ec_student)
                 
logging.basicConfig(level=logging.DEBUG)
AR.init('/home/ryan/alwaysRostering/python/databases/2019-01-29-genesis.db')
loop = asyncio.get_event_loop()
loop.run_until_complete(sync(loop))
