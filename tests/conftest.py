import os
import pytest
from houndcrawler.database import Store
from houndcrawler.config import Settings
from cryptography.fernet import Fernet

@pytest.fixture
def store():
    url=os.environ.get('HOUNDCRAWLER_TEST_DATABASE_URL')
    if not url:pytest.skip('Set HOUNDCRAWLER_TEST_DATABASE_URL to an isolated test database')
    if not url.split('?',1)[0].endswith('/houndcrawler_test'):raise RuntimeError('Refusing to clear a database not named houndcrawler_test')
    db=Store(url)
    with db.pool.connection() as c:c.execute('TRUNCATE hc_jobs,hc_frontier,hc_results,hc_events,hc_cache,hc_artifacts,hc_credentials,hc_monitors,hc_outbox,hc_agent_state,hc_notification_profiles,hc_origin_slots RESTART IDENTITY CASCADE')
    with db.pool.connection() as c:c.execute('UPDATE hc_network_slots SET owner=NULL,lease_until=0')
    yield db
    db.close()
@pytest.fixture
def settings(store,tmp_path):return Settings(database='test',keys={'alpha':'a'*40,'beta':'b'*40},storage=str(tmp_path),encryption_key=Fernet.generate_key().decode(),workers=2)
