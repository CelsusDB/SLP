# MineSLP
A simple way to interact with Minecraft's SLP protocol without any third-party libraries

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip install MineSLP
```

## Usage

```python
import MineSLP

data = slp.server(host = server_ip)
server = data.Update()[1]

''' Dict of data '''
data = ({
  'version': server['version']['name'],
  'protocol': server['version']['protocol'],
  'modded': True if 'modinfo' in server else False,
  'description': [ x['text'].rstrip() for x in server['description']['extra'] ],
  'players': server['players']
})

''' Output json data to console '''
print( json.dumps(data, indent=3) )
```
