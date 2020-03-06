from mock import patch
from datetime import datetime, timedelta

from bugbug_http.utils import IdleTTLCache

class MockDatetime():
  def __init__(self, mock_now):
    self.mock_now = mock_now
  def now(self):
    return self.mock_now
  def set_now(self, new_mock_now):
    self.mock_now = new_mock_now
    
def test_purges_after_ttl():
  mockdatetime = MockDatetime(datetime(2019, 4, 1, 10))
  cache = IdleTTLCache(timedelta(hours=2))

  @patch('datetime.datetime', mockdatetime)
  def with_patched_datetime():
    cache.put('key_a', 'payload')

    #after one hour
    mockdatetime.set_now(datetime(2019, 4, 1, 11))
    cache.purge_expired_entries()
    assert('key_a' in cache)

    #after two hours one minute
    mockdatetime.set_now(datetime(2019, 4, 1, 12, 1))
    cache.purge_expired_entries()
    assert('key_a' not in cache)

  with_patched_datetime()

def test_ttl_refreshes_after_get():
  mockdatetime = MockDatetime(datetime(2019, 4, 1, 10))
  cache = IdleTTLCache(timedelta(hours=2))

  @patch('datetime.datetime', mockdatetime)
  def with_patched_datetime():
    cache.put('key_a', 'payload')

    #after one hour
    mockdatetime.set_now(datetime(2019, 4, 1, 11))
    cache.purge_expired_entries()
    assert('key_a' in cache)

    cache.get('key_a')

    #after three hours
    mockdatetime.set_now(datetime(2019, 4, 1, 13))
    cache.purge_expired_entries()
    assert('key_a' in cache)

    #after three hours one minute
    mockdatetime.set_now(datetime(2019, 4, 1, 13, 1))
    cache.purge_expired_entries()
    assert('key_a' not in cache)
  with_patched_datetime()
