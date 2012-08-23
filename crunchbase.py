import requests
import string
import re


def slugify(s):
    slug = s.encode('ascii', 'ignore').lower()
    slug = re.sub(r'[^a-z0-9]+', '-', slug).strip('-')
    slug = re.sub(r'[-]+', '-', slug)
    return slug


class CrunchbaseScraper(object):
    """Grabs HFNews tag information from Crunchbase API"""
    def __init__(self, name, tag_type):
        self.name = slugify(name)
        self.tag_type = tag_type

        self.json = None
        self.crunchbase_url = None
        self.overview = None

        if self.tag_type == 'Company':
            self.api_url = 'http://api.crunchbase.com/v/1/company/%s.js' % (name)
            self.money_raised = None
            self.company_url = None
            self.category = None

        elif self.tag_type == 'Person':
            self.api_url = 'http://api.crunchbase.com/v/1/person/%s.js' % (name)
            self.affiliation = None

    def get_json(self):
        """Gets raw JSON from API"""
        self.json = requests.get(self.api_url).json
        return self.json

    def set_company_values(self):
        """Fills in relevant company tag fields given JSON"""
        self.name = self.json['name']
        self.overview = self.json['overview']
        self.crunchbase_url = self.json['crunchbase_url']
        self.money_raised = self.json['total_money_raised']
        self.company_url = self.json['homepage_url']

        c = self.json['category_code']
        if c == 'hardware':
            self.category = 'Consumer Electronics/Devices'
        elif c == 'web':
            self.category = 'Consumer Web'
        elif c == 'games_video':
            self.category = 'Games, Video, and Entertainment'
        elif c == 'network_hosting':
            self.category = 'Network/Hosting'
        elif c == 'public_relations':
            self.category = 'Communications'
        elif c == 'biotech':
            self.category = 'BioTech'
        elif c == 'cleantech':
            self.category = 'CleanTech'
        elif c == 'ecommerce':
            self.category = 'eCommerce'
        else:
            self.category = string.capitalize(c)

        return self.name + ' / Success'

    def set_person_values(self):
        """Fills in relevant person tag fields given JSON"""
        self.name = self.json['first_name'] + ' ' + self.json['last_name']
        self.overview = self.json['overview']
        self.crunchbase_url = self.json['crunchbase_url']
        self.affiliation = self.json['affiliation_name']

        return self.name + ' / Success'


def fetch_info(name, tag_type):
    cb = CrunchbaseScraper(name, tag_type)
    cb.get_json()

    if tag_type == 'Company':
        cb.set_company_values()
        print '\nName: %s' % (cb.name)
        print '\nOverview: %s' % (cb.overview)
        print '\nCrunchbase URL: %s' % (cb.crunchbase_url)
        print '\nMoney Raised: %s' % (cb.money_raised)
        print '\nCompany URL: %s' % (cb.company_url)
        print '\nCategory: %s' % (cb.category)

    else:
        cb.set_person_values()
        print '\nName: %s' % (cb.name)
        print '\nOverview: %s' % (cb.overview)
        print '\nCrunchbase URL: %s' % (cb.crunchbase_url)
        print '\nAffiliation: %s' % (cb.affiliation)
