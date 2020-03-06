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
    
mockdatetime = MockDatetime(datetime(2019, 4, 1, 10))
@patch('datetime.datetime', mockdatetime)
def test_purges_after_ttl():
  mockdatetime.set_now(datetime(2019, 4, 1, 10))
  cache = IdleTTLCache(timedelta(hours=2))
  cache.put('key_a', 'payload')
  assert('key_a' in cache)

  #1 hour in the future
  mockdatetime.set_now(datetime(2019, 4, 1, 11))
  cache.purge_expired_entries()
  assert('key_a' in cache)

  #2 hours and one minute in the future
  mockdatetime.set_now(datetime(2019, 4, 1, 12, 1))
  cache.purge_expired_entries()
  assert('key_a' not in cache)

mockdatetime = MockDatetime(datetime(2019, 4, 1, 10))
def test_refreshes_ttl_with_get():
  pass
#  mockdatetime.set_now(datetime(2019, 4, 1, 10))
#  cache = IdleTTLCache(timedelta(hours=2))
#  cache.put('key_a', 'payload')
#  assert('key_a' in cache)
#
#  #1 hour in the future
#  mockdatetime.set_now(datetime(2019, 4, 1, 11))
#  cache.purge_expired_entries()
#  assert('key_a' in cache)
#  cache.get('key_a')
#
#  #2 hours and one minute in the future
#  mockdatetime.set_now(datetime(2019, 4, 1, 12, 1))
#  cache.purge_expired_entries()
#  assert('key_a' in cache)
#
#  #3 hours in the future
#  mockdatetime.set_now(datetime(2019, 4, 1, 13, 0))
#  cache.purge_expired_entries()
#  assert('key_a' in cache)
#
#  #4 hours and two minutes in the future
#  mockdatetime.set_now(datetime(2019, 4, 1, 15, 2))
#  cache.purge_expired_entries()
#  assert('key_a' not in cache)
