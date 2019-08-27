from datetime import date, datetime, timedelta
import inspect
from dateutil.parser import parse as parse_dt

from nordpool import elspot


class AioPrices(elspot.Prices):
    def __init__(self, currency, client):

        super().__init__(currency)
        self.client = client

    async def _io(self, url, **kwargs):
        resp = await self.client.get(url, params=kwargs)
        # aiohttp
        if inspect.isawaitable(resp.json()):
            return await resp.json()
        else:
            # Httpx and asks
            return resp.json()

    async def _fetch_json(self, data_type, end_date=None):
        """ Fetch JSON from API """
        # If end_date isn't set, default to tomorrow
        if end_date is None:
            end_date = date.today() + timedelta(days=1)
        # If end_date isn't a date or datetime object, try to parse a string
        if not isinstance(end_date, date) and not isinstance(end_date, datetime):
            end_date = parse_dt(end_date)

        return await self._io(
            self.API_URL % data_type,
            currency=self.currency,
            endDate=end_date.strftime("%d-%m-%Y"),
        )

    async def fetch(self, data_type, end_date=None, areas=[]):
        """
        Fetch data from API.
        Inputs:
            - data_type
                API page id, one of Prices.HOURLY, Prices.DAILY etc
            - end_date
                datetime to end the data fetching
                defaults to tomorrow
            - areas
                list of areas to fetch, such as ['SE1', 'SE2', 'FI']
                defaults to all areas
        Returns dictionary with
            - start time
            - end time
            - update time
            - currency
            - dictionary of areas, based on selection
                - list of values (dictionary with start and endtime and value)
                - possible other values, such as min, max, average for hourly
        """
        data = await self._fetch_json(data_type, end_date)
        return self._parse_json(data, areas)

    async def hourly(self, end_date=None, areas=[]):
        """ Helper to fetch hourly data, see Prices.fetch() """
        return await self.fetch(self.HOURLY, end_date, areas)

    async def daily(self, end_date=None, areas=[]):
        """ Helper to fetch daily data, see Prices.fetch() """
        return await self.fetch(self.DAILY, end_date, areas)

    async def weekly(self, end_date=None, areas=[]):
        """ Helper to fetch weekly data, see Prices.fetch() """
        return await self.fetch(self.WEEKLY, end_date, areas)

    async def monthly(self, end_date=None, areas=[]):
        """ Helper to fetch monthly data, see Prices.fetch() """
        return await self.fetch(self.MONTHLY, end_date, areas)

    async def yearly(self, end_date=None, areas=[]):
        """ Helper to fetch yearly data, see Prices.fetch() """
        return await self.fetch(self.YEARLY, end_date, areas)





if __name__ == '__main__':
    #import aiohttp
    #import httpx

    #from asks.sessions import Session
    async def kek():
        #client = aiohttp.ClientSession()
        #client = httpx.AsyncClient()
        client = Session()
        p = AioPrices("NOK", client)

        x = await p.hourly()
        #print(x)


    #import asyncio


    #asyncio.run(kek())
