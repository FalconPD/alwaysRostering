class Users():
    """
    Handles users operations
    """
    @classmethod
    async def create(cls, session):
        """
        Creates an object linked to a session
        Need a factory function due to async
        """
        self = cls()
        self.session = session
        await self.refresh()
        return self

    async def refresh(self):
        """
        Gets a list of the users from Atlas from a CSV export
        """
        #resp = await self.session.get( 'https://monroek12.rubiconatlas.org/' +
        #    'Atlas/Admin/View/TeachersExport?CSVDoc=1')
        resp = await self.session.get('https://monroek12.rubiconatlas.org/Atlas/Portal/View/Default')
        print(await resp.text())
