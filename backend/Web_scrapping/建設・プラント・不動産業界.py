import re
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os
import glob
import math
from tqdm import tqdm
from random import randint
from itertools import cycle
import traceback
import random
from urllib.parse import urljoin
# Define the DODA category for IT・通信業界
DODA_CATEGORIES = {
    "建設・プラント・不動産業界": "08L"
}

# List of prefectures in Japan, used to handle text data correctly
KEN = [
"北海道","青森","岩手","宮城","秋田","山形","福島","茨城",
"栃木","群馬","埼玉","千葉","東京","神奈川","新潟","富山",
"石川","福井","山梨","長野","岐阜","静岡","愛知","三重",
"滋賀","京都","大阪","兵庫","奈良","和歌山","鳥取","島根",
"岡山","広島","山口","徳島","香川","愛媛","高知",
"福岡","佐賀","長崎","熊本","大分","宮崎","鹿児島","沖縄",
]
KEN = '|'.join(KEN)


UA = [{"ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.1", "pct": 40.65},
      {"ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.3", "pct": 14.95},
      {"ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.3", "pct": 8.88},
      {"ua": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/25.0 Chrome/121.0.0.0 Safari/537.3", "pct": 8.41},
      {"ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.3", "pct": 6.54},
      {"ua": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.3", "pct": 4.67},
      {"ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.3", "pct": 3.74},
      {"ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Unique/100.7.6266.6", "pct": 3.74},
      {"ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.", "pct": 1.87},
      {"ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 OPR/112.0.0.", "pct": 1.87},
      {"ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.", "pct": 0.93},
      {"ua": "Mozilla/5.0 (X11; CrOS x86_64 14541.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.3", "pct": 0.93},
      {"ua": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.", "pct": 0.93},
      {"ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.3", "pct": 0.93},
      {"ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.", "pct": 0.93}]
# 1. Get all doda's company link
# 1.1 Get total company
def get_total_companies(category_code):
    """カテゴリコードに基づいて該当企業数を取得する関数"""
    # https://doda.jp/DodaFront/View/CompanySearch.action?ind=01L&job=1&page=1
    # https://doda.jp/DodaFront/View/CompanySearch.action?ind=22L
    url = f"https://doda.jp/DodaFront/View/CompanySearch.action?ind={category_code}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    result_span = soup.find('span', class_='search_result_number_unit_part')

    if result_span:
        result_text = result_span.text.strip().replace(',', '')
        return int(result_text)
    return 0
#  1.2 Scrape all doda's company link
#  1.2.a Scrape all doda's company link (offer and not offer)
def scrape_company_info(category_name, category_code, num_pages):
    """カテゴリ内の全企業情報をスクレイピングしてCSVに保存する関数"""
    companies_name = []
    companies_info_link = []
    first_job_link = []

    # TODO TEST
    test = list(tqdm(range(1, num_pages + 1), desc=f"Scraping {category_name}"))

    # for num in tqdm(range(1, num_pages + 1), desc=f"Scraping {category_name}"):
    for num in range(0, len(test)- 1):
        # TODO TEST
        url = f"https://doda.jp/DodaFront/View/CompanySearch/j_ind__{category_code}/-page__{test[num]}"

        # url = f"https://doda.jp/DodaFront/View/CompanySearch/j_ind__{category_code}/-page__{num}"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        cards = soup.find_all('div', class_='companyInfoCard')

        for card in cards:
            # TODO TEST
            company_name = card.find('span', class_='company').string.strip()
            info_link = card.find('a', string='企業情報を見る').get('href')

            # company_name = card.find('span', class_='company').text.strip()
            # info_link = card.find('a', text='企業情報を見る').get('href')
            companies_name.append(company_name)
            companies_info_link.append(info_link)

            job_cards = card.find_all('li', class_='companyInfoCard__jobInfo')
            if job_cards:
                first_job_link.append(job_cards[0].find('a').get('href'))
            else:
                first_job_link.append(None)

        time.sleep(1.0)

    save_to_csv(category_name, companies_name, companies_info_link,first_job_link)
#  1.2.b Scrape all offering doda's company link
def scrape_offerring_company_info(category_name, category_code, num_pages):
    """カテゴリ内の全企業情報をスクレイピングしてCSVに保存する関数"""
    companies_name = []
    companies_info_link = []
    first_job_link = []

    for num in tqdm(range(1, num_pages + 1), desc=f"Scraping {category_name}"):
        url = f"https://doda.jp/DodaFront/View/CompanySearch.action?ind={category_code}&job=1&page={num}"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        cards = soup.find_all('div', class_='companyInfoCard')

        for card in cards:
            company_name = card.find('span', class_='company').text.strip()
            info_link = card.find('a', text='企業情報を見る').get('href')
            companies_name.append(company_name)
            companies_info_link.append(info_link)

            job_cards = card.find_all('li', class_='companyInfoCard__jobInfo')
            if job_cards:
                first_job_link.append(job_cards[0].find('a').get('href'))
            else:
                first_job_link.append(None)

        time.sleep(1.5)

    save_to_csv(category_name, companies_name, companies_info_link,first_job_link)
#* Temp function use for store data to google drive
def save_to_csv(category_name, names, links,job_link):
    """企業名とリンク先をCSVファイルに保存する関数"""
    data = {"企業名": names, "企業情報リンク先": links, "求人企業リンク": job_link}
    df = pd.DataFrame(data)    #"C:\Users\user\Desktop\cograph_project\venv\cographPJ\backendtask\newtask.py"
    filename = f"C:/Users/user/Desktop/cograph_project/cograph-database-pj/backend/data/建設・プラント・不動産業界{category_name}.csv"
    df.to_csv(filename, index=False, encoding='utf-8')
    print(f"中間ファイル '{filename}' を保存しました。")

# 2. Scrape company information

#* Temp function use for clean text
def clean_text(text):
    """テキストから余計な空白や記号を除去する関数"""
    text = re.sub(r'\s+', ' ', text)
    text = text.replace('\u3000', ' ')
    return text.strip()
#* Temp function use for reformat date
def reformat_date(date_str):
    match = re.search(r'(\d{4})年(\d{1,2})月', date_str)
    if match:
      year = match.group(1)
      month = match.group(2)
      return f"{year}-{month.zfill(2)}-01"
    else:
      return date_str

# 2.1 Scrape company information
def scrape_doda_company_info(url):
    """企業の詳細情報をスクレイピングする関数"""
    try:
      response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
      if response.status_code != 200:
          return f"Failed to retrieve page, status code: {response.status_code}"

      soup = BeautifulSoup(response.text, 'html.parser')
      profile_area = soup.find('section', class_='profileArea')
      if not profile_area:
          return "profileAreaセクションが見つかりません"

      common_area = soup.find('article', id='commonArea')
      company_name = common_area.find('div', class_='name').p.text.strip()
      industry_detail = common_area.find('div', class_='industry').span.text.strip()

      job_tab = soup.find('li', id='header_tab_job')
      jobs_exist = "求人なし"
      if job_tab:
          job_count_span = job_tab.find('span', class_='tabInner__buttonText__jobs')
          if job_count_span:
              jobs_exist = job_count_span.get('data-count', '').strip() or "無"

      overview_header = profile_area.find('h3')
      overview_update_date = (overview_header.find('span', class_='content__updateDate').text
                              if overview_header else '不明')
      overview_update_date = reformat_date(clean_text(overview_update_date))

      overview_table = profile_area.find('table', class_='table__horizontal')
      if not overview_table:
          return "企業概要のテーブルが見つかりません"

      company_info = {
          '更新日': overview_update_date,
          '名称': company_name,
          '業界(小分類)': industry_detail,
          '求人有無': jobs_exist
      }

      for row in overview_table.find_all('tr', class_='table__row'):
          header = row.find('th', class_='table__header').text.strip()
          data = row.find('td', class_='table__data').text.strip()
          company_info[header] = clean_text(data)

      extract_foundation = lambda s: int(re.search(r'\d+', s).group())
      extract_avg_age = lambda s: float(re.search(r'\d+\.\d+', s).group())
      extract_employee = lambda s: int(re.search(r'\d[,、\d]*', s).group().replace(',', '').replace('、', ''))

      company_info['設立'] = extract_foundation(company_info['設立']) if '設立' in company_info else None
      company_info['平均年齢'] = extract_avg_age(company_info['平均年齢']) if '平均年齢' in company_info else None
      company_info['従業員数'] = extract_employee(company_info['従業員数']) if '従業員数' in company_info else None
      return company_info
    except Exception as e:
        return f"Error accessing {url}: {str(e)}"

# Split data into 求人を出している企業 and 求人を出していない企業
def doda_company_split(file_names):
  """企業の詳細情報をスクレイピングする関数"""
  for i,file in enumerate(file_names):
    df = pd.read_csv(file)
    df_offer = df[df['求人有無'].str.match(r'^\d{1,2}$')]
    df_no_offer = df[df['求人有無'].str.match(r'~^\d{1,2}$')]
    save_temp_csv(df_offer.values.tolist(), "/content/drive/MyDrive/公社・官公庁・学校・研究施設_1/thien/offer", i + 1)
    save_temp_csv(df_no_offer.values.tolist(), "/content/drive/MyDrive/公社・官公庁・学校・研究施設_1/thien/no_offer", i + 1)

# $$$$$$$$$$$$$$$$$$$$$$$$$$ 求人を出している企業のみ $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# 2.2 Scrape company homepage (求人を出している企業のみ)
def scrape_doda_company_url(url):
    """企業のホームページURLを取得する関数"""
    try:
      response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
      if response.status_code != 200:
          return f"Failed to retrieve page, status code: {response.status_code}"

      soup = BeautifulSoup(response.text, 'html.parser')
      application_method = soup.find('div', class_='inner03')
      if application_method :
        dl = application_method.find_all('dl')
        if len(dl) > 1:
          url = dl[1].find('a').get('href')
        else:
          url = "なし"
      elif soup.find("table", {"id": "company_profile_table"}):
        url = soup.find("table", {"id": "company_profile_table"}).find("a").get("href")
      else:
        url = "なし"
      return url
    except Exception as e:
        return f"Error accessing {url}: {str(e)}"

# 2.3 Scrape company phone number
def scrape_company_phone_number(company_name, location):
    """企業の電話番号を取得する関数"""
    query = f"{company_name} {location} site:jp"
    search_url = f"https://www.google.com/search?q={query}"
    phone_number = None
    try:
      response = requests.get(search_url,headers={'User-Agent': random.choices(UA,k=1)[0]['ua']})
      if response.status_code != 200:
          return response.status_code
      soup = BeautifulSoup(response.text, 'html.parser')
      phone_pattern = re.compile(r'\b\d{2,4}[-.\s]?\d{2,4}[-.\s]?\d{4}\b')
      text = soup.get_text()
      phone_number = list(set(phone_pattern.findall(text)))
      return phone_number if phone_number else "なし"
    except Exception as e:
      return f"Error accessing {search_url}: {str(e)}"
def scrape_all_phone_number(csv_files):
  for file_path in csv_files:
    company_info_data = []
    target_df = pd.read_csv(file_path)
    company_list = target_df.values.tolist()
    for i,company in enumerate(tqdm(company_list)):
      contact_url = scrape_company_phone_number(company[1],company[5])
      company_info_data.append(contact_url)
      time.sleep(1.5)


# 2.4 Scrape company homepage (求人を出している企業のみ)
find_contact_link = lambda tag: tag.name == 'a' and tag.find(text=re.compile(r'お問い合わせ|問い合わせ|CONTACT|お問合せ|Contact us'))
def scrape_contact_company_url(url):
    """企業のホームページURLを取得する関数"""
    try:
      response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'})
      repsonse_url = response.url
      if response.status_code != 200:
          return f"Failed to retrieve page, status code: {response.status_code}"
      soup = BeautifulSoup(response.content.decode("utf-8","ignore"), 'html.parser')
      contact_url = soup.find(find_contact_link)
      if contact_url:
        contact_url = urljoin(repsonse_url,contact_url.get('href'))
        return contact_url
      else:
        return "なし"
    except Exception as e:
      return f"Error accessing {url}: {str(e)}"
def scrape_all_contact_company_url(csv_files):
  for file_path in csv_files:
    company_info_data = []
    target_df = pd.read_csv(file_path)
    company_list = target_df.values.tolist()
    for i,company in enumerate(tqdm(company_list)):
      contact_url = scrape_contact_company_url(company[10])
      # print(i,company[11],contact_url)
      company_info_data.append(contact_url)
      time.sleep(1.5)
def process_csv_files(file_paths, save_path):
    """各CSVファイルを処理して企業情報をスクレイピングする関数"""
    for file_path in file_paths:
        company_info_data = []
        target_df = pd.read_csv(file_path)

        print(file_path)

        for i, company_url in enumerate(tqdm(target_df["企業情報リンク先"].to_list(), desc="Processing companies")):
            company_info = scrape_doda_company_info(company_url)
            company_info_data.append(company_info)

            if (i + 1) % 1000 == 0:
                save_temp_csv(company_info_data, save_path, i + 1)
                company_info_data = []
            time.sleep(1.1)

        if company_info_data:
            save_temp_csv(company_info_data, save_path, len(target_df))

        print(f"処理されたファイル: {file_path[:]}")


#* Temp function for concat and store file
def save_temp_csv(data, save_path, index):
    """企業情報を一時的に保存する関数"""
    df_temp_1 = pd.DataFrame([data[0]])
    for num in range(1, len(data)):
        df_temp_2 = pd.DataFrame([data[num]])
        df_temp_1 = pd.concat([df_temp_1, df_temp_2], axis=0)
    df_temp_1 = df_temp_1.reset_index(drop=True)
    temp_filename = os.path.join(save_path, f'temp_company_data_{index}.csv')
    df_temp_1.to_csv(temp_filename, index=False)
    print(f"中間ファイル '{temp_filename}' を保存しました。")

#* Add information to csv file
def add_to_csv(column, csv_files, company_info_data):
  df = pd.read_csv(csv_files)
  df[column] = company_info_data
  df.to_csv(csv_files, index=False)

# 3. Scrape company offer information
# 3.1 Get total offer
def get_total_offer(url):
    """カテゴリコードに基づいて該当企業数を取得する関数"""
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    result_span = soup.find('span', class_='all_job_count search__listCount')
    if result_span:
        result_text = result_span.text.strip().replace(',', '')
        time.sleep(1)
        return int(result_text)
    time.sleep(1)
    return 0
# 3.2 Get offer page number
def get_offer_page_number(url):
    return math.ceil(get_total_offer(url)/50)
# 3.3 Scrape company offer info
def scrape_company_offer_info(company_name,base_url):
  job_listings = []
  for page in range(1, get_offer_page_number(base_url)+1):
      url = f"{base_url}-page__{page}/"
      response = requests.get(url)
      response.raise_for_status()
      soup = BeautifulSoup(response.content, 'lxml')
      posting_job_wrapper  = soup.find('div', {"id":'posting_job_wrapper'})
      cards = posting_job_wrapper.find_all('section', class_='cardDetail')
      for card in cards:
          # =====================================================================================
          job_tittle = card.find('span', class_='cardDetail__titleInnerCompany').text.strip()
          # ============================================================================
          cardDetail__mainItem = card.find_all('dl', class_='cardDetail__mainItem')
          # -------------------------------------------------------------
          job_description = cardDetail__mainItem[0].find('dd', class_='cardDetail__mainContent').text.strip()
          job_description = clean_text(job_description)
          # ====================================================================================
          job_location_section = cardDetail__mainItem[2].find('dd', class_='cardDetail__mainContent').text.strip()
          matches = re.findall(KEN, job_location_section)
          location = list(set(matches))
          job_listings.append({'Company_name':company_name,"job_tittle":job_tittle,'job_description':job_description,"勤務地": location})
      time.sleep(1)
  return job_listings



# # category_code に指定された業界（大項目）
# category_code = "08L"
# # get_total_companies(category_code) から取得された、企業数(int)
# total_companies = get_total_companies(category_code)
# time.sleep(1)
# num_pages = math.ceil(total_companies / 50)
# # 辞書にある、category_name, category_code を参照する
# category_name = "建設・プラント・不動産業界"
# category_code = "08L"
# scrape_company_info(category_name, category_code, num_pages)




csv_files = glob.glob(os.path.join(
    "c:/Users/user/Desktop/cograph_project/cograph-database-pj/backend/data/建設・プラント・不動産業界", '*.csv'
))
print(f'csv_files ~ {csv_files}')

for file_path in csv_files:
    company_info_data = []

    # Read the CSV file safely
    try:
        target_df = pd.read_csv(file_path)
        print(f'file_path ~ {file_path}')
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        continue

    # Process each company URL
    for i, company_url in enumerate(tqdm(target_df.values.tolist(), desc="Processing companies")):
        try:
            # Ensure the scraped data is a dictionary
            company_info = scrape_doda_company_info(company_url[1])
            time.sleep(1.1)

            # Check if `company_info` is a dictionary
            if isinstance(company_info, dict):
                if company_url[2] is not None:
                    url = scrape_doda_company_url(company_url[2])
                    company_info['企業URL'] = url
                else:
                    company_info['企業URL'] = None
                company_info_data.append(company_info)
            else:
                print(f"Expected dictionary, got {type(company_info)} for URL {company_url[1]}")

            # Save data every 1000 entries
            if (i + 1) % 1000 == 0:
                try:
                    save_temp_csv(
                        company_info_data, 
                        "c:/Users/user/Desktop/cograph_project/cograph-database-pj/backend/data/建設・プラント・不動産業界", 
                        i + 1
                    )
                    company_info_data = []
                except Exception as e:
                    print(f"Error saving temporary CSV: {e}")

            time.sleep(1.1)

        except Exception as e:
            print(f"Error processing company URL at index {i} in file {file_path}: {e}")




# csv_files = glob.glob(os.path.join("C:/Users/user/Desktop/cograph_project/cograph-database-pj/backend/data/建設・プラント・不動産業界", '*.csv'))

# for file_path in csv_files:
#   company_info_data = []
#   target_df = pd.read_csv(file_path)

#   print(file_path)

#   for i, company_url in enumerate(tqdm(target_df.values.tolist(), desc="Processing companies")):
#       company_info = scrape_doda_company_info(company_url[1])
#       time.sleep(1.1)
#       if isinstance(target_df['求人企業リンク'][i],str):
#         url = scrape_doda_company_url(company_url[2])
#         company_info['企業URL'] = url
#       else:
#         company_info['企業URL'] = None
#       company_info_data.append(company_info)

#       if (i + 1) % 1000 == 0:
#           save_temp_csv(company_info_data, "C:/Users/user/Desktop/cograph_project/cograph-database-pj/backend/data/建設・プラント・不動産業界", i + 1)
#           company_info_data = []
#       time.sleep(1.1)


# csv_files = glob.glob(os.path.join(
#     "c:/Users/user/Desktop/cograph_project/cograph-database-pj/backend/data/建設・プラント・不動産業界", '*.csv'
# ))
# print(f'csv_files ~ {csv_files}')

# for file_path in csv_files:
#     company_info_data = []

#     # Read the CSV file safely
#     try:
#         target_df = pd.read_csv(file_path)
#         print(f'file_path ~ {file_path}')
#     except Exception as e:
#         print(f"Error reading {file_path}: {e}")
#         continue

#     # Process each company URL
#     for i, company_url in enumerate(tqdm(target_df.values.tolist(), desc="Processing companies")):
#         try:
#             # Ensure the scraped data is a dictionary
#             company_info = scrape_doda_company_info(company_url[1])
#             time.sleep(1.1)

#             # Check if `company_info` is a dictionary
#             if isinstance(company_info, dict):
#                 if company_url[2] is not None:
#                     url = scrape_doda_company_url(company_url[2])
#                     company_info['企業URL'] = url
#                 else:
#                     company_info['企業URL'] = None
#                 company_info_data.append(company_info)
#             else:
#                 print(f"Expected dictionary, got {type(company_info)} for URL {company_url[1]}")

#             # Save data every 1000 entries
#             if (i + 1) % 1000 == 0:
#                 try:
#                     save_temp_csv(
#                         company_info_data, 
#                         "c:/Users/user/Desktop/cograph_project/cograph-database-pj/backend/data/建設・プラント・不動産業界", 
#                         i + 1
#                     )
#                     company_info_data = []
#                 except Exception as e:
#                     print(f"Error saving temporary CSV: {e}")

#             time.sleep(1.1)

#         except Exception as e:
#             print(f"Error processing company URL at index {i} in file {file_path}: {e}")