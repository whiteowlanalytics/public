## start date, end date
import requests
import json
from google.cloud import bigquery
import datetime


def csr_api(endpoint, params=False):
        u = "https://api.clientseoreport.com/v3/"+endpoint
        if params != False:
            u += "?campaign_id="+str(params)
            
        h = {
        'Authorization': 'Basic ########'
        }
        r = requests.request("GET", u, headers=h)
        j = r.json()
        return j

def hello_world(request):
    request_json = request.get_json()
    if request.args and 'message' in request.args:
        return request.args.get('message')
    elif request_json and 'message' in request_json:
        return request_json['message']
    else:

        today = datetime.date.today().strftime('%Y-%m-%d')
        tod = datetime.date.today()
        d = datetime.timedelta(days = 365)
        a = (tod - d).strftime('%Y-%m-%d')


        ## big query connection
        client = bigquery.Client(project="974164595016")
        dataset_ref = client.dataset('data')
        table_ref = dataset_ref.table('clc_api_data')
        table = client.get_table(table_ref)

        ## get campaign data from api
        campaign_data = csr_api("campaigns")

        #loop through campaign data
        for y in campaign_data["data"]:
            ## get keywords for campaign
            kw_data = csr_api("keywords",y['id'])           
            
            for z in kw_data["data"]:
                ## get keyword feed ranking data
                feed_data = csr_api("resources/rankings/keyword/date?keyword_id="+str(z["id"])+"&start_date="+a+"&end_date="+today)
                ftotals = feed_data["data"]
                for ftx in ftotals:                
                    client.insert_rows(table, [{"campaign_id": str(y["id"]), "company": str(y["company"]), "keyword_id": str(z["id"]), "keyword_phrase": str(z["keyword_phrase"]), "google_ranking": int(ftx["googleRanking"]), "bing_ranking": int(ftx["bingRanking"]), "date": str(ftx["date"])}])

        return "Done"