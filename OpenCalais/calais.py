import json
import requests


class TagScraper(object):

    def __init__(self, text):
        self.api_endpoint = 'http://api.opencalais.com/enlighten/rest/'
        self.licenseID = "qkrhyynat9qdt6jun3vfwybz"
        self.paramsXML = """
        <c:params xmlns:c="http://s.opencalais.com/1/pred/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">

        <c:processingDirectives c:contentType="text/txt" c:enableMetadataType="GenericRelations,SocialTags" c:outputFormat="Application/JSON" >

        </c:processingDirectives>

        <c:userDirectives >

        </c:userDirectives>

        <c:externalMetadata>

        </c:externalMetadata>

        </c:params>
        """

        self.params = {}
        self.params['licenseID'] = self.licenseID
        self.params['paramsXML'] = self.paramsXML

        if type(text) == unicode:
            self.text = text.encode('ascii', 'ignore')
        else:
            self.text = text
        self.calais_json = None
        self.entities = []
        self.entity_relevances = []
        self.crunchbase_entities = {}

    def get_calais_json(self):
        self.params['content'] = self.text[:4900]
        self.calais_json = requests.get(self.api_endpoint, params=self.params)
        self.calais_json = json.loads(self.calais_json.text)
        self.calais_json.pop('doc')  # omit useless metadata
        return self.calais_json

    def get_entities(self):
        for value in self.calais_json.values():
            if value['_typeGroup'] == u'entities':
                try:
                    if value['relevance'] > .3:
                        self.entities.append(value['name'])
                        self.entity_relevances.append(value['relevance'])

                        if value['_type'] == u'Person':
                            self.crunchbase_entities[value['name']] = 'Person'

                        elif value['_type'] == u'Company':
                            self.crunchbase_entities[value['name']] = 'Company'

                except KeyError:
                    pass

        return self.entities