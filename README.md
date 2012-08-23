hfnews-scripts
==============

Standalone internal scripts used on [HFNews](http://hfnews.org), a news aggregator and search engine 
built in Django.

NewsScraper
-----------

Scrapes RSS feeds, runs article text through the [OpenCalais API](http://viewer.opencalais.com) to 
get tags (entities).

Call `fetch_articles(rss.xml)` to print to stdout.

Crunchbase
----------

Used in combination with entities retrieved using `newsscraper.py`.

Call `fetch_info(tag_name, tag_type)` to retrieve relevant information from Crunchbase API. `tag_type` 
can be equal to `Company` or `Person`.
