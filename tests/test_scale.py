"""Opt-in 10k-page real HTTP qualification against a controlled local fixture."""
import asyncio,json,os,socket,time,platform
from pathlib import Path
import pytest
from aiohttp import web
from houndcrawler.network import Network
from houndcrawler.models import JobRequest,Options
from houndcrawler.engine import Engine
from houndcrawler.worker import Worker
@pytest.mark.asyncio
async def test_ten_thousand_http_pages(store,settings):
 if os.environ.get('HOUNDCRAWLER_SCALE')!='true':pytest.skip('Explicit scale qualification profile')
 count=10000
 async def handler(request):
  path=request.path
  if path=='/robots.txt':return web.Response(text='User-agent: *\nAllow: /\n')
  if path=='/sitemap.xml':return web.Response(text='<urlset>'+''.join('<url><loc>http://fixture.example/page/'+str(i)+'</loc></url>' for i in range(count))+'</urlset>',content_type='application/xml')
  return web.Response(text='<html><main><h1>Fixture '+path+'</h1><p>Controlled acquisition scale evidence. This content is intentionally synthetic and not a competitor benchmark.</p></main></html>',content_type='text/html')
 app=web.Application();app.router.add_get('/{tail:.*}',handler);runner=web.AppRunner(app);await runner.setup();site=web.TCPSite(runner,'127.0.0.1',0);await site.start();port=site._server.sockets[0].getsockname()[1]
 class Resolver:
  async def resolve(self,host,port=0,family=0):return [{'hostname':host,'host':'127.0.0.1','port':fixture_port,'family':socket.AF_INET,'proto':0,'flags':0}]
  async def close(self):pass
 fixture_port=port;settings.workers=8;engine=Engine(settings,store,Network(8,resolver=Resolver(),store=store));worker=Worker(engine)
 job=store.create('alpha',JobRequest(kind='crawl',urls=['http://fixture.example/sitemap.xml'],max_pages=count+2,max_depth=1,max_seconds=3600,max_download_bytes=1073741824,options=Options(formats=['text'],render='never',max_age=0)))
 started=time.monotonic();task=asyncio.create_task(worker.run())
 try:
  async with asyncio.timeout(3500):
   while store.get('alpha',job['id'])['status'] not in ('completed','partial','paused'):await asyncio.sleep(.5)
  row=store.get('alpha',job['id'])
  with store.pool.connection() as c:r=c.execute("SELECT count(*) n FROM hc_results WHERE job=%s AND url LIKE 'http://fixture.example/page/%%' AND NOT(result?'error')",(job['id'],)).fetchone()
  report={'fixture':'synthetic real HTTP via injected test-only resolver','html_pages':r['n'],'expected':count,'elapsed_seconds':time.monotonic()-started,'status':row['status'],'cpu_count':os.cpu_count(),'platform':platform.platform(),'memory_kib':int(next(line.split()[1] for line in Path('/proc/meminfo').read_text().splitlines() if line.startswith('MemTotal:'))),'commit':os.environ.get('GITHUB_SHA'),'comparison':'not run'}
  Path('benchmark-results').mkdir(exist_ok=True);Path('benchmark-results/crawler-scale.json').write_text(json.dumps(report,indent=2));assert r['n']==count and row['status']=='completed',report
 finally:worker.stopping=True;task.cancel();await asyncio.gather(task,return_exceptions=True);await runner.cleanup()
