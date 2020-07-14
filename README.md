# Blueliv
This is Blueliv's Python3 API encapsulation.

You can fin all the details related to this API in https://community.blueliv.com/#!/docs/consumer (you will need to register for the Community edition) and, naturally, request a token code for the API.

Once registered and with a valid token, you can perform several actions on the Community sandbox and Threat Intel platform, from searching IoCs, sparks, tags... to publishing throught the API.

You may use token in two ways:

- In an explicit way, passing the token in the class constructor (for example, `SparksRequest(token=token)`)
- In an implicit way setting the environment variable (`BLUELIV_API_TOKEN='your token'`)

The implicit way is added to be able to deal with the package in contexts where environment variables are used to change the behaviour of applications and resources. For example, in docker containers, Heroku, etc.


## Structure

Here you will find a description of the classes and methods you may take advantage of.

### blueliv.core

This is the base module and classes to vertebrate real actions. It is not a pure interfaces module because there exist some implementations that are common for all the subclasses and submodels (for example, .request or .search).


#### BluelivRequest

This is the base class for all the requests we can perform against the platform. It is not typical for you to use directly this base class, as most relevant logic is embed onto subclasses (CrawlerRequest, IocsRequest, ...).

```
class BluelivRequest(BASERequestModel):
```

### blueliv.crawl

This is the module where Crawl classes are set. The Blueliv crawler lets you extract IOCs from the given URL or String.

```
class CrawlerRequest(BluelivRequest):
```

The use is as easy as:

```
from blueliv.crawl import CrawlerRequest

crawler = CrawlerRequest()
crawler.crawl(term='mafia', is_text=True)
```

### blueliv.iocs

This is the module where IoCs classes are set. The most relevant functions here are listing IoC types, finding IoCs in your sparks timeline and in the discover timeline.  

```
class IocsRequest(BluelivRequest):
```

To list types:

```
from blueliv.iocs import IocsRequest

iocs = IocsRequest()
iocs.types()
```

Finding IoCs in your timeline:

```
from blueliv.iocs import IocsRequest

iocs = IocsRequest()
iocs.timeline(limit=0, since_id=0)
```

Finding IoCs in the discover stream:

```
from blueliv.iocs import IocsRequest

iocs = IocsRequest()
iocs.discover(limit=0, since_id=0)
```

### blueliv.malwares

This is the module where Malwares operations can be performed. You can list malwares, show details about a specific one or, even, _upload_:  

```
class MalwaresRequest(BluelivRequest):
```

To list:

```
from blueliv.malwares import MalwaresRequest

malwares = MalwaresRequest()
malwares.list(page=0, pageSize=0)
```

Show details for a malware id:

```
from blueliv.malwares import MalwaresRequest

malwares = MalwaresRequest()
malwares.show(malware_id=1234)
```

Upload a sample to the Community sandbox:

```
from blueliv.malwares import MalwaresRequest

iocs = MalwaresRequest()
iocs.upload(filename='/tmp/malware.xxx')
```

_In future versions the io.BytesIO api will be implemented to let developers pass binary array as parameter instead of a filename._


### blueliv.sparks

Sparks are posts in the Community stream that may have information, IoCs and tags attached. Wiht this module you can take advantage of several capabilities in your (and in other's) spark-streams.  

```
class SparksRequest(BluelivRequest):
```

To get a spakr by id:

```
from blueliv.sparks import SparksRequest

sparks = SparksRequest()
sparks.get(spark_id=1234)
```

To retrieve from your timeline:

```
from blueliv.sparks import SparksRequest

sparks = SparksRequest()
sparks.timeline(limit=0, since_id=0)
```

In the discover stream:

```
from blueliv.sparks import SparksRequest

sparks = SparksRequest()
sparks.discover(limit=0, since_id=0)
```

Retrieve IoCs from a specific spark id:

```
from blueliv.sparks import SparksRequest

sparks = SparksRequest()
sparks.iocs(spark_id=1234, limit=0, since_id=0)
```

and, _publish_ to the spark stream, in your timeline:

```
from blueliv.sparks import SparksRequest

sparks = SparksRequest()
sparks.publish(title='My test spark',
               description='Description should be detailed',
               tlp='green',
               source_urls=...,
               source_malware_id=...,
               tags=...,
               iocs=...):
```

### blueliv.tags

Here you can play with tags associated with the other categories.  

```
class TagsRequest(BluelivRequest):
```

To list all known tags:

```
from blueliv.tags import TagsRequest

tags = TagsRequest()
tags.list()
```

List sparks associated with a tag slug:

```
from blueliv.tags import TagsRequest

tags = TagsRequest()
tags.list_sparks(tag_slug='mafia', limit=0, since_id=0)
```

List IoCs associated with a tag slug:

```
from blueliv.tags import TagsRequest

tags = TagsRequest()
tags.list_iocs(tag_slug='mafia', limit=0, since_id=0)
```

### blueliv.users

And, finally, you can get information related to specific users in the platform.  

```
class UsersRequest(BluelivRequest):
```

To list **your own** information:

```
from blueliv.users import UsersRequest

users = UsersRequest()
users.me()
```

List sparks associated with an user:

```
from blueliv.users import UsersRequest

users = UsersRequest()
users.list_sparks(username='rramirez', limit=0, since_id=0)
```

List IoCs associated with an user:

```
from blueliv.users import UsersRequest

users = UsersRequest()
users.list_iocs(username='rramirez', limit=0, since_id=0)
```

## Search

The Blueliv's API includes several powerful search capabilities that we have include in the core base class (*blueliv.core.BASERequestModel.search(...)*).

This is a decision oriented to save lines of code avoiding a re-implementation in every class. Within this inherited "search" method, the caller class is checked and the search API request is performed properly.

So, if you want to search for sparks, iocs or tags (what is supported right now):

```
from blueliv.iocs import IocsRequest

iocs = IocsRequest()
result = iocs.search(search_term='my term', tag='my tag', limit=0, since_id=0)
```

```
from blueliv.sparks import SparksRequest

sparks = SparksRequest()
result = sparks.search(search_term='my term', tag='my tag', limit=0, since_id=0, as_json=True)
```

In this case, as_json was True so the result will be a list of dicts. If as_json is False, it will return a JSON-formatted string.


```
from blueliv.tags import TagsRequest

tags = TagsRequest()
tags.search(search_term='my tag')
```



## Created and upload to PyPi

This package was created using PyPi/pip configuration options through setup.py. The following command:

`$ python3 setup.py sdist bdist_wheel`

Will create both the source-dist package and the WHL (Zip compressed) one. But to upload to PyPi you only need the source generated by:

`$ python3 setup.py sdist`

The upload process is simplified through the `twine` tool:

`$ twine upload dist/*`
