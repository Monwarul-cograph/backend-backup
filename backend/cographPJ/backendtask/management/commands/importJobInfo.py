import pandas as pd
from django.core.management.base import BaseCommand
from backendtask.models import JobList
import os
from django.db import models
from django.conf import settings

class Command(BaseCommand):
    help = 'Import info from CSV file'
    def handle(self, *args, **kwargs):
        data_dir = os.path.join(settings.BASE_DIR, 'data')
        csv_file_path = os.path.join(data_dir, 'job_IT・通信業界_sample.csv')

        if not os.path.isfile(csv_file_path):
            self.stdout.write(self.style.ERROR(f'CSV file not found at {csv_file_path}.'))
            return

        try:
            df = pd.read_csv(csv_file_path)

            # Fill missing values with 'UnKnown'
            df = df.fillna('UnKnown')

            # Log the number of records to be imported
            self.stdout.write(self.style.SUCCESS(f'Number of records to import: {len(df)}'))

            for _, row in df.iterrows():
                try:
                    # Convert UnKnown or non-numeric values to a valid numeric representation or None
                    def convert_to_int(value):
                        if value == 'UnKnown' or not isinstance(value, (int, float)):
                            return None
                        return int(value)

                    def convert_to_decimal(value):
                        if value == 'UnKnown' or not isinstance(value, (int, float)):
                            return None
                        return float(value)
                    
                    duplicate = False

                    d = row.get('COMPANY_NAME')
                    e = row.get('LOCATION')

                    if "UnKnown" in str(row.get('COMPANY_NAME')): 
                        d = ""
                    if "UnKnown" in str(row.get('LOCATION')): 
                        e = 0
                   

                    if JobList.objects.filter(
                        COMPANY_NAME = d,
                        LOCATION = e,
                    ):
                        duplicate = True


                    if not duplicate:
                        # Import company data with exception handling for each row
                        JobList.objects.create(
                            COMPANY_NAME = row.get('COMPANY_NAME', 'UnKnown'),
                            JOB_TITTLE = row.get('JOB_TITTLE', 'UnKnown'),
                            JOB_DESCRIPTION = row.get('JOB_DESCRIPTION', 'UnKnown'),
                            LOCATION = row.get('LOCATION', 'UnKnown')
                            )


                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Failed to insert record: {row} due to {e}'))

            self.stdout.write(self.style.SUCCESS('Successfully imported Job info.'))



    



        except pd.errors.EmptyDataError:
            self.stdout.write(self.style.ERROR('CSV file is empty.'))
        except pd.errors.ParserError:
            self.stdout.write(self.style.ERROR('Error parsing CSV file.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An error occurred: {e}'))