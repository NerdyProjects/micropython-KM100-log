import cryptolib
import config
import urequests
import ubinascii
import json
import time
import gc
import traceback

run_count = 150
headers={'accept': 'application/json', 'user-agent': 'TeleHeater/2.2.3'}
enc = cryptolib.aes(config.key, 1)
def request_and_write():
  results = {}
  for path in config.urls:
    url = config.host + path
    response = urequests.get(url, headers=headers)
    body = ubinascii.a2b_base64(response.text)
    decrypted = enc.decrypt(body)
    obj = json.loads(decrypted)
    if 'value' in obj:
      results[path] = obj['value']
  fixed_result = {}
  for key, value in results.items():
    if isinstance(value, str):
      fixed_result[key] = '"' + value + '"'
    else:
      fixed_result[key] = value
  
  data = 'heating_system ' + ','.join(f'{key}={value}' for key, value in fixed_result.items())
    
  write_url = config.influxdb + '/write?db=' + config.influxdb_db
  response = urequests.post(write_url, auth=(config.influxdb_user, config.influxdb_password), data=data)

while run_count > 0:
  try:
    request_and_write()
  except Exception as err:
    traceback.print_exc()
    print('Could not request/write data points', repr(err))
  gc.collect()
  time.sleep(20)
  run_count = run_count - 1

