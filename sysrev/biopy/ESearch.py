from Bio import Entrez


# Refer to Dataflow.txt (point number ??)


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














