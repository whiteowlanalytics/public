## start date, end date
import requests
import json
from google.cloud import bigquery
import datetime
from KeywordsDataPull import KeywordsDataPull

def main(request):
    keywords_data_pull = KeywordsDataPull('974164595016')
    keywords_data_pull.get_keywords()
    return "Done"