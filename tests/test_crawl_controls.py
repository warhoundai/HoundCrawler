import pytest
from houndcrawler.models import JobRequest
from houndcrawler.worker import Worker
from houndcrawler.engine import Engine
from houndcrawler.compat import options

def links(store,settings,**kwargs):
 worker=Worker(Engine(settings,store));request=JobRequest(urls=['https://example.com/docs/'],**kwargs).model_dump()
 item={'request':request,'kind':'crawl','depth':0}
 result={'discovered_links':[{'url':u} for u in ['https://example.com/docs/a?q=1','https://example.com/docs/a?q=2','https://example.com/blog','https://sub.example.com/docs/x','https://other.com/a','https://example.com/sitemap.xml']]}
 return worker,item,result

def test_scope_query_and_sitemap_controls(store,settings):
 w,i,r=links(store,settings,crawl_entire_domain=False,ignore_query_parameters=True,sitemap='skip')
 assert w.links(i,r)==[('https://example.com/docs/a',1)]
 w,i,r=links(store,settings,allow_subdomains=True)
 out=dict(w.links(i,r));assert 'https://sub.example.com/docs/x' in out and 'https://other.com/a' not in out
 w,i,r=links(store,settings,allow_external_links=True);assert 'https://other.com/a' in dict(w.links(i,r))
 w,i,r=links(store,settings,sitemap='only');assert not w.links(i,r)
 r['acquisition']='sitemap';assert all(depth==0 for _,depth in w.links(i,r))

def test_hard_concurrency_ceiling(store,settings):
 req=JobRequest(kind='batch',urls=['https://example.com/a','https://example.com/b'],max_concurrency=1)
 row=store.create('alpha',req);one=store.claim(120);assert one and one['job']==row['id'];assert store.claim(120) is None

def test_compat_age_units():assert options({'maxAge':10000}).max_age==10
