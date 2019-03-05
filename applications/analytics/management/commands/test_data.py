# coding=utf-8

from django.core.management.base import BaseCommand

from elasticsearch import Elasticsearch

from applications.analytics.models import LogStashConfiguration



class Command(BaseCommand):
    def handle(self, *args, **options):
        conf = LogStashConfiguration.get_solo()
        last_processed = conf.last_procesed
        index = conf.index

        es = Elasticsearch(hosts=[conf.elastic_host, ])

        property_data = es.search(index=index, body={"query": {"match": {"type": "property"}}})
        self.remove_parsed_logs(property_data, es)
        # for data in property_data['hits']['hits']:
        #     source = data['_source']
        #     print('-----')
        #     print(source['slug'])
        #     print(source['action'])
        #     print(data['_id'])
        #     print('------')

    def remove_parsed_logs(self, queryset, es):
        bulk = ""
        for result in queryset['hits']['hits']:
          bulk = bulk + '{ "delete" : { "_index" : "' + str(result['_index']) + '", "_type" : "' + str(result['_type']) + '", "_id" : "' + str(result['_id']) + '" } }\n'
        es.bulk( body=bulk )