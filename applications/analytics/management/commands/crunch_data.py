# coding=utf-8

import json, ast
import datetime

from dateutil import parser

from django.core.management.base import BaseCommand
from django.utils import timezone

from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan

from applications.property.models import Property, PropertyAnalytics
from applications.agent.models import Agent
from applications.builder.models import Builder
from applications.advertisement.models import Advertisement
from applications.analytics.models import LogStashConfiguration

from utils.helpers import as_utc


class Command(BaseCommand):
    def handle(self, *args, **options):
        conf = LogStashConfiguration.get_solo()
        last_processed = conf.last_procesed
        index = conf.index

        es = Elasticsearch(hosts=[conf.elastic_host, ])

        property_data = es.search(index=index, body={
            "query": {
                "match": {
                    "type": "property"
                }
            }
        }, scroll='60s', search_type='scan')
        v_ct_ips, c_ct_ips, r_ct_ips = [], [], []
        results = self.scroll_full_results(property_data, es)
        for data in results:
            try:
                ref = data['_id']
                source = data['_source']
                date = parser.parse(source.get('@timestamp'))
                month = timezone.now().month
                year = timezone.now().year
                if date > last_processed and source['verb'] == 'GET':
                    type_dict = {"ip": source['clientip'], "slug": source['slug'], "session_id": source['session_id']}
                    p = Property.objects.get(slug=type_dict['slug'])
                    analytics, created = PropertyAnalytics.objects.get_or_create(property=p, month=month, year=year)

                    if source['action'] == 'v_ct':
                        if not type_dict in v_ct_ips:
                            p.view_count += 1
                            p.save()
                            v_ct_ips.append(type_dict)
                            analytics.view_count += 1
                            analytics.save()
                    if source['action'] == 'c_ct':
                        if not type_dict in c_ct_ips:
                            p.click_count += 1
                            p.save()
                            c_ct_ips.append(type_dict)
                            analytics.click_count += 1
                            analytics.save()
                    if source['action'] == 'r_ct':
                        if not type_dict in r_ct_ips:
                            p.response_count += 1
                            p.save()
                            r_ct_ips.append(type_dict)
                            analytics.response_count += 1
                            analytics.save()
            except Exception as e:
                print(e)
        # self.remove_parsed_logs(property_data, es)

        agent_data = es.search(index=index, body={
            "query": {
                "match": {
                    "type": "agent"
                }
            }
        }, scroll='60s', search_type='scan')
        v_ct_ips, c_ct_ips, r_ct_ips = [], [], []
        results = self.scroll_full_results(agent_data, es)
        for data in results:
            try:
                ref = data['_id']
                source = data['_source']
                date = parser.parse(source.get('@timestamp'))
                if date > last_processed and source['verb'] == 'GET':
                    type_dict = {"ip": source['clientip'], "slug": source['slug'], "session_id": source['session_id']}
                    p = Agent.objects.get(slug=type_dict['slug'])
                    if source['action'] == 'v_ct':
                        if not type_dict in v_ct_ips:
                            p.view_count += 1
                            p.save()
                            v_ct_ips.append(type_dict)
                    if source['action'] == 'c_ct':
                        if not type_dict in c_ct_ips:
                            p.click_count += 1
                            p.save()
                            c_ct_ips.append(type_dict)
                    if source['action'] == 'r_ct':
                        if not type_dict in r_ct_ips:
                            p.response_count += 1
                            p.save()
                            r_ct_ips.append(type_dict)
            except Exception as e:
                print(e)

        # self.remove_parsed_logs(agent_data, es)

        builder_data = es.search(index=index, body={
            "query": {
                "match": {
                    "type": "builder"
                }
            }
        }, scroll='60s', search_type='scan')
        v_ct_ips, c_ct_ips, r_ct_ips = [], [], []
        results = self.scroll_full_results(builder_data, es)
        for data in results:
            try:
                ref = data['_id']
                source = data['_source']
                date = parser.parse(source.get('@timestamp'))
                if date > last_processed and source['verb'] == 'GET':
                    type_dict = {"ip": source['clientip'], "slug": source['slug'], "session_id": source['session_id']}
                    p = Builder.objects.get(slug=type_dict['slug'])
                    if source['action'] == 'v_ct':
                        if not type_dict in v_ct_ips:
                            p.view_count += 1
                            p.save()
                            v_ct_ips.append(type_dict)
                    if source['action'] == 'c_ct':
                        if not type_dict in c_ct_ips:
                            p.click_count += 1
                            p.save()
                            c_ct_ips.append(type_dict)
                    if source['action'] == 'r_ct':
                        if not type_dict in r_ct_ips:
                            p.response_count += 1
                            p.save()
                            r_ct_ips.append(type_dict)
            except Exception as e:
                print(e)
        # self.remove_parsed_logs(builder_data, es)

        advert_data = es.search(index=index, body={
            "query": {
                "match": {
                    "type": "advert"
                }
            }
        }, scroll='60s', search_type='scan')
        v_ct_ips, c_ct_ips, r_ct_ips = [], [], []
        results = self.scroll_full_results(advert_data, es)
        for data in results:
            try:
                ref = data['_id']
                source = data['_source']
                date = parser.parse(source.get('@timestamp'))
                if date > last_processed and source['verb'] == 'GET':
                    type_dict = {"ip": source['clientip'], "slug": source['slug'], "session_id": source['session_id']}
                    p = Advertisement.objects.get(slug=type_dict['slug'])
                    if source['action'] == 'v_ct':
                        if not type_dict in v_ct_ips:
                            p.view_count += 1
                            p.save()
                            v_ct_ips.append(type_dict)
                    if source['action'] == 'c_ct':
                        if not type_dict in c_ct_ips:
                            p.click_count += 1
                            p.save()
                            c_ct_ips.append(type_dict)
                    if source['action'] == 'r_ct':
                        if not type_dict in r_ct_ips:
                            p.response_count += 1
                            p.save()
                            r_ct_ips.append(type_dict)
            except Exception as e:
                print(e)
        # self.remove_parsed_logs(advert_data, es)

        conf.last_procesed = timezone.now()
        conf.save()

    def remove_parsed_logs(self, queryset, es):
        bulk = ""
        try:
            for result in queryset['hits']['hits']:
                bulk = bulk + '{ "delete" : { "_index" : "' + str(result['_index']) + '", "_type" : "' + str(
                    result['_type']) + '", "_id" : "' + str(result['_id']) + '" } }\n'
            es.bulk(body=bulk)
        except Exception as e:
            print(e)

    def scroll_full_results(self, res, es):
        results = []
        scroll_size = res['hits']['total']

        while scroll_size > 0:
            try:
                scroll_id = res['_scroll_id']
                res = es.scroll(scroll_id=scroll_id, scroll='60s')
                results += res['hits']['hits']
                scroll_size = len(res['hits']['hits'])
            except Exception as e:
                print('Scroll Error: ', e)
                break
        return results




