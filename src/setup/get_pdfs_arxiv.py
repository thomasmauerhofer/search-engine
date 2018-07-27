#!/usr/bin/env python3
# encoding: utf-8
import pickle

import arxiv

# {'id': 'http://arxiv.org/abs/1710.10201v1',
# 'guidislink': True,
# 'updated': '2017-10-27T15:33:29Z',
# 'updated_parsed': time.struct_time(tm_year=2017, tm_mon=10, tm_mday=27, tm_hour=15, tm_min=33, tm_sec=29, tm_wday=4, tm_yday=300, tm_isdst=0),
# 'published': '2017-10-27T15:33:29Z',
# 'published_parsed': time.struct_time(tm_year=2017, tm_mon=10, tm_mday=27, tm_hour=15, tm_min=33, tm_sec=29, tm_wday=4, tm_yday=300, tm_isdst=0),
# 'title': 'New Methods for Metadata Extraction from Scientific Literature',
# 'title_detail': {
#                   'type': 'text/plain',
#                   'language': None,
#                   'base': 'http://export.arxiv.org/api/query?search_query=unsipervised+document+structure+analysis+of+digital+scientific+articles&id_list=&start=0&max_results=10',
#                   'value': 'New Methods for Metadata Extraction from Scientific Literature'},
#                   'summary': 'Within the past few decades we...',
#                   'summary_detail': {
#                                       'type': 'text/plain',
#                                       'language': None,
#                                       'base': 'http://export.arxiv.org/api/query?search_query=unsipervised+document+structure+analysis+of+digital+scientific+articles&id_list=&start=0&max_results=10',
#                                       'value': 'Within the past few ...'
#                                      },
#                   'authors': ['Dominika Tkaczyk'],
#                   'author_detail': {'name': 'Dominika Tkaczyk'},
#                   'author': 'Dominika Tkaczyk',
#                   'arxiv_comment': 'PhD Thesis',
#                   'links': [{'href': 'http://arxiv.org/abs/1710.10201v1', 'rel': 'alternate', 'type': 'text/html'},
#                             {'title': 'pdf', 'href': 'http://arxiv.org/pdf/1710.10201v1', 'rel': 'related', 'type': 'application/pdf'}],
#                   'arxiv_primary_category': {'term': 'cs.DL', 'scheme': 'http://arxiv.org/schemas/atom'},
#                   'tags': [{'term': 'cs.DL', 'scheme': 'http://arxiv.org/schemas/atom', 'label': None},
#                            {'term': 'cs.IR', 'scheme': 'http://arxiv.org/schemas/atom', 'label': None},
#                            {'term': 'I.7.5; H.3.7', 'scheme': 'http://arxiv.org/schemas/atom', 'label': None}],
#                   'pdf_url': 'http://arxiv.org/pdf/1710.10201v1',
#                   'affiliation': 'None',
#                   'arxiv_url': 'http://arxiv.org/abs/1710.10201v1',
#                   'journal_reference': None,
#                   'doi': None
#                  }



#papers = arxiv.query(search_query="unsipervised document structure analysis of digital scientific articles")
#arxiv.download(papers[0], "tmp/")
from config import REQ_DATA_PATH
from engine.api import API

api = API()
#print(len(api.get_all_paper()))

tmp = ["aaaa", "bbbb"]
#with open(REQ_DATA_PATH + "finished_papers.txt", 'wb') as fp:
#    pickle.dump(tmp, fp)

with open (REQ_DATA_PATH + "finished_papers.txt", 'rb') as fp:
    tmplist = pickle.load(fp)

print(tmplist)


