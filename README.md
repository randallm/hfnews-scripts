hfnews-scripts
==============

Standalone internal scripts used on [HFNews](http://hfnews.org), a news aggregator and search engine
built in Django.

NewsScraper
-----------

Scrapes RSS feeds and runs them through Readability to get news articles. Requires bs4, readability-lxml, lxml, requests, and feedparser.

Call `fetch_articles(rss.xml)` to print to stdout.

Calais
------

Takes body of text and runs it through the
[OpenCalais](http://viewer.opencalais.com) API to get entities (tags). Requires requests.

    tag = TagScraper(text)
    tag.get_calais_json()
    tag.get_entities()

    # all entities under 30% relevance are filtered out:
    print tag.entities
    print tag.crunchbase_entities

Crunchbase
----------

Used in combination with entities retrieved using `calais.py` to get relevant company/person information. Requires requests.

Call `fetch_info(tag_name, tag_type)` to retrieve relevant information from Crunchbase API. `tag_type`
can be equal to `Company` or `Person`.
