import pandas as pd
from django.core.management.base import BaseCommand
from backendtask.models import CompanyList
import os
from django.db import models
from django.conf import settings

class Command(BaseCommand):
    help = 'Import info from CSV file'

    def handle(self, *args, **kwargs):
        data_dir = os.path.join(settings.BASE_DIR, 'data')
        csv_file_path = os.path.join(data_dir, 'company_IT・通信業界_sample.csv')

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

                    a = row.get('名称')
                    b = row.get('事業内容')
                    c = row.get('所在地')

                    if "UnKnown" in str(row.get('名称')): 
                        a = ""
                    if "UnKnown" in str(row.get('事業内容')): 
                        b = 0
                    if "UnKnown" in str(row.get('所在地')): 
                        c = 0

                    if CompanyList.objects.filter(
                        名称 = a,
                        事業内容 = b,
                        所在地 = c,
                    ):
                        duplicate = True

                    print("\n\n")
                    print(row.get('お問い合わせ先URL'))
                    print("\n\n")

                    if not duplicate:
                        # Import company data with exception handling for each row
                        CompanyList.objects.create(
                            更新日=row.get('更新日'),  # This field should be properly parsed or skipped
                            名称=row.get('名称'),
                            業界_小分類=row.get('業界_小分類') if row.get('業界_小分類') != 'UnKnown' else None,
                            求人有無=row.get('求人有無'), # Adjust according to actual data
                            事業内容=row.get('事業内容'),
                            所在地=row.get('所在地'),
                            設立=convert_to_int(row.get('設立')),
                            従業員数=convert_to_int(row.get('従業員数')),
                            資本金=row.get('資本金') if row.get('資本金') != 'UnKnown' else None,
                            企業URL=row.get('企業URL') if row.get('企業URL') != 'UnKnown' else None,
                            上場市場名=row.get('上場市場名') if row.get('上場市場名') != 'UnKnown' else None,
                            代表者=row.get('代表者') if row.get('代表者') != 'UnKnown' else None,
                            平均年齢=convert_to_decimal(row.get('平均年齢')),
                            お問い合わせ先URL = row.get('お問い合わせ先URL') if row.get('お問い合わせ先URL') != 'UnKnown' else None,
                            代表電話番号 = row.get('代表電話番号') if row.get('代表電話番号') != 'UnKnown' else None,
                        )
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Failed to insert record: {row} due to {e}'))

            self.stdout.write(self.style.SUCCESS('Successfully imported company info.'))
        except pd.errors.EmptyDataError:
            self.stdout.write(self.style.ERROR('CSV file is empty.'))
        except pd.errors.ParserError:
            self.stdout.write(self.style.ERROR('Error parsing CSV file.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An error occurred: {e}'))

    
    