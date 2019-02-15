# AfterMarket.pl API client class for Python

This library allows you to issue calls to the AfterMarket.pl public API from Python 2 and Python 3.

## Quick start

Install the library using pip:

```
pip install aftermarketpl
```

Create the API client object, providing your API key.
[Click here to obtain your API key.](https://www.aftermarket.pl/API/Create/)

```python
client = aftermarketpl.Client('<MY API KEY>', '<MY API SECRET>')
```

Call an API function and obtain a result.
[Click here to see the list of API functions.](https://json.aftermarket.pl/)

```python
result = client.send('/domain/check', {'names[]': ['domain1.pl', 'domain2.pl']})
```

## Examples

### Retrieve a list of domains, synchronously

```
import aftermarketpl

client = aftermarketpl.Client('<MY API KEY>', '<MY API SECRET>')
domain_list = client.send('/domain/list')
```

### Retrieve a list of domains, asynchronously

```
import aftermarketpl

def print_domains(domains):
  print(domains)

domain_list = client.send_async('/domain/list', callback=print_domains)
```

Alternatively, you can use await/async on Python 3.5

```
import aftermarketpl
import asyncio

async def main():
  client = aftermarketpl.Client('<MY API KEY>', '<MY API SECRET>')
  loop = asyncio.get_event_loop()
  future1 = loop.run_in_executor(None, client.send, '/domain/check', {'names[]': ['check-1.pl','check-2.pl']})
  future2 = loop.run_in_executor(None, client.send, '/domain/check', {'names[]': ['check-3.pl','check10.pl']})
  return await future1, future2

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```

Or the asyncio decorators and `yield from` in Python 3.4

```
import aftermarketpl
import asyncio

@asyncio.coroutine
def main():
  client = aftermarketpl.Client('<MY API KEY>', '<MY API SECRET>')
  loop = asyncio.get_event_loop()
  future1 = loop.run_in_executor(None, client.send, '/domain/check', {'names': ['check-1.pl','check-2.pl']})
  future2 = loop.run_in_executor(None, client.send, '/domain/check', {'names': ['check-3.pl','check10.pl']})
  result1 = yield from future1
  result2 = yield from future2
  print(result1, result2)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```

### Handle errors

```
import aftermarketpl
from aftermarketpl import APIException

client = aftermarketpl.Client('<MY API KEY>', '<MY API SECRET>')

try: 
  client.send('/domain/check', params={names: ['check-1.pl','check-2.pl']})
except HTTPException as e:
  if e.status == 404:
    print(e.message)
  elif e.status == 400:
    pass
  elif e.status == 500:
    pass
  else:
    print(e)

```

Asynchronous errors can be handled by passing in a function to the reject parameter

```
import aftermarketpl
from aftermarketpl import HTTPException


client = aftermarketpl.Client('<MY API KEY>', '<MY API SECRET>')

def handle_error(e):
  if type(e) != HTTPException: raise e
  if e.status == 404:
    print(e.message)
  elif e.status == 400:
    pass
  elif e.status == 500:
    pass
  else:
    print(e)

client.send_async('/domain/check', params={names: ['check-1.pl','check-2.pl']}, reject=handle_error)
```

### Debugging HTTP requests
```
import aftermarketpl
from aftermarketpl import HTTPException


client = aftermarketpl.Client('<MY API KEY>', '<MY API SECRET>', url= 'https://json.aftermarket.pl', debug=True)
client.send('/domain/check', params={names: ['check-1.pl','check-2.pl']})
client.debug = False
```
