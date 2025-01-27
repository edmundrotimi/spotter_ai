import os
import time

import pandas as pd
import requests
from django.core.management.base import BaseCommand, CommandError

from core.project.settings import BASE_DIR, MAPQUEST_API_KEY

# Infor
"""
 using geocoding to add Lat and Long coordinates for each truck stop using the address in CSV file
"""


class Command(BaseCommand):
    help = 'Update CSV file by adding lat and logitude columns'  # noqa: A003

    def handle(self, *args, **options):

        self.style.WARNING('Checking if file exists ...')

        try:
            update_file_exists = os.path.join(BASE_DIR, 'core/fuel/utils/update_fuel-prices-for-be-assessment.csv')

            if not os.path.isfile(update_file_exists):

                self.stdout.write(
                    self.style.WARNING('About to update CSV with Latitude and Longtude Columns using Address Columns')
                )
                self.stdout.write(self.style.SUCCESS('Processing and updating CSV File ...'))

                # load and read csv file
                file_path = os.path.join(BASE_DIR, 'core/fuel/utils/fuel-prices-for-be-assessment.csv')
                df = pd.read_csv(file_path)

                # init lat nd long
                latitudes = []
                longitudes = []

                # loop through address in file and get geocoding
                # using maprequest api
                BASE_URL = 'http://www.mapquestapi.com/geocoding/v1/address'

                for address in enumerate(df['Address']):
                    # get lat long
                    params = {
                        'key': MAPQUEST_API_KEY,
                        'location': address[0],
                    }
                    response = requests.get(BASE_URL, params=params)

                    # extract latitude and longitude from the API response
                    data = response.json()
                    print(response.json())
                    if data['info']['statuscode'] == 0:  # Check for a successful response
                        location = data['results'][0]['locations'][0]['latLng']
                        latitudes.append(location['lat'])
                        longitudes.append(location['lng'])
                    else:
                        latitudes.append(None)
                        longitudes.append(None)

                    # pause for 1 second due to OpenStreetMap rate limits
                    time.sleep(1)

                # add to csv file
                df['Latitude'] = latitudes
                df['Longitude'] = longitudes

                # save updated CSV
                updated_file_path = os.path.join(BASE_DIR, 'core/fuel/utils/update_fuel-prices-for-be-assessment.csv')
                df.to_csv(updated_file_path, index=False)

                self.stdout.write(
                    self.style.SUCCESS('CSV file successfully updated with Latitude and Longtude Columns')
                )
            else:
                self.stdout.write(self.style.SUCCESS('Updated file with Latitude and Longitude already exists.'))
        except Exception:
            raise CommandError('Failed update CVS file with Latitude and Longtude Columns')
