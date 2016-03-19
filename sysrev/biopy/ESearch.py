from Bio import Entrez


# Refer to Dataflow.txt (point number 3)


def search(query):
    Entrez.email = '2131791M@student.gla.ac.uk'
    handle = Entrez.esearch(db='pubmed',
                            sort='relevance',
                            retmax='20',
                            retmode='xml',
                            term=query)

    # results is a dictionary containing, information from the data returned from NCBI Entrez Utilities.
    # info such as number of results, ID list, etc/

    results = Entrez.read(handle)
    # for information on .read, refer to DataFlow.txt. (Read handles the parsing of the XML returned from NCBI Entrez Utilities
    # into python objects)


    return results


def store_ids(id_list, webenv='', querykey=''):
    Entrez.email = '2131791M@student.gla.ac.uk'
    if webenv == '':
        handle = Entrez.epost(db='pubmed',
                              id=id_list)
    else:
        handle = Entrez.epost(db='pubmed',
                              QueryKey=querykey,
                              WebEnv=webenv)

    records = Entrez.read(handle)
    return records


def fetch_ids(webenv, querykey):
    Entrez.email = '2131791M@student.gla.ac.uk'
    handle = Entrez.efetch(db='pubmed',
                           QueryKey=querykey,
                           WebEnv=webenv)
    ids = Entrez.read(handle)
    return ids


def fetch_details(id_list):
    ids = ','.join(id_list)
    Entrez.email = '2131791M@student.gla.ac.uk'
    handle = Entrez.efetch(db='pubmed',
                           retmode='xml',
                           id=ids)
    results = Entrez.read(handle)
    return results


def doc_summaries(id_list):
    ids = ','.join(id_list)
    Entrez.email = '2131791M@student.gla.ac.uk'
    handle = Entrez.esummary(db='pubmed',
                             id=ids)
    docSummaries = Entrez.read(handle)
    return docSummaries


def search_record_count(query):
    Entrez.email = '2131791M@student.gla.ac.uk'
    handle = Entrez.egquery(term=query)
    count = Entrez.read(handle)
    return count


def spell_check(query):
    Entrez.email = '2131791M@student.gla.ac.uk'
    handle = Entrez.espell(term=query)
    spell_check_info = Entrez.read(handle)
    return spell_check_info




# For tests


if __name__ == '__main__':
    results = search('(adhd OR addh OR adhs) AND (child OR adolescent) AND (acupuncture)')
    id_list = results['IdList']
    papers = fetch_details(id_list)
    webenv = 'NCID_1_141103525_165.112.9.37_9001_1458207436_2014848750_0MetA0_S_MegaStore_F_1'
    querykey = '1'
    # storeInfo = storeIDs(id_list,webenv,querykey)
    # ids = fetchIDs(webenv,querykey)
    # docSummaries = doc_summaries(id_list)
    count = search_record_count('cancer')
    #spell_check_info = spell_check('cancer OR feever')
    # print papers
    # for i, paper in enumerate(papers):
    # print("%d) %s" % (i+1, paper['MedlineCitation']))
    # print("%d) %s" % (i+1, paper['Article']['Abstract']))
    # Pretty print the first paper in full
    import json

    for index in range(10):
        #print(json.dumps(spell_check_info, indent=2, separators=(',', ':')))
        print(json.dumps(papers[index]['MedlineCitation'], indent=2, separators=(',', ':')))
        # print(json.dumps(papers[index]['MedlineCitation']['Article']['AuthorList'], indent=2, separators=(',', ':')))
