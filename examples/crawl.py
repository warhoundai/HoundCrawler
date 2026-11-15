"""Run against your own HoundCrawler instance; never put keys in source."""
import os
from houndcrawler.client import Client
with Client(os.environ['HOUNDCRAWLER_ENDPOINT'],api_key=os.environ['HOUNDCRAWLER_API_KEY']) as client:
 job=client.submit('crawl',['https://example.com/'],max_pages=25,options={'formats':['text'],'render':'never'})
 print(client.wait(job['id']))
 for page in client.results(job['id']):print(page)
