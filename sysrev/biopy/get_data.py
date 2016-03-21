from ESearch import *



#     run_query(query)
# takes in a query, and runs through pubmed, returning a nested dictionary as a result.
# each key on the outer dictionary is a Paper PubmedID and under each key is a nested dictionary with information
# on each of the papers returned
# eg.
#       [ID]:[Article_title]
#            [Date_created]
#            [date_completed]
#            [Abstract]
#            [Authors]
#            [Link]
#

def run_query(query):
    results = search(query)
    id_list = results['IdList']

    result_list = {}

    papers = fetch_details(id_list)
    n = 0

    for paper in papers:
        paper_info = {}

        #add the title, and dates
        paper_info['Article_title'] = paper['MedlineCitation']['Article']['ArticleTitle']
        date_created = paper['MedlineCitation']['DateCreated']
        date_text = date_created['Day'] + '/' + date_created['Month'] + '/' + date_created['Year']
        date_text_complete = ''
        if 'DateCompleted' in paper['MedlineCitation'].keys():
            date_completed = paper['MedlineCitation']['DateCompleted']
            date_text_complete += date_completed['Year'] + '-' + date_completed['Month'] + '-' + date_completed['Day']
        else:
            date_text_complete += 'incomplete'
            # date_text_complete = date_completed['Day']+'/'+date_completed['Month']+'/'+date_completed['Year']
        paper_info['Date_created'] = date_text
        paper_info['Date_completed'] = date_text_complete



        #add the abstracts
        try:
            abstract_info = paper['MedlineCitation']['Article']['Abstract']['AbstractText']
            abstract_text = ''
            for section in abstract_info:

                abstract_text +=  section

            paper_info['Abstract'] = abstract_text
        except:
            paper_info['Abstract'] = "No Abstract."




        #add the authors with their affiliations
        Authors = paper['MedlineCitation']['Article']['AuthorList']
        author_string = ''
        for author in Authors:
            author_dictionary = author
            if 'ForeName' in author_dictionary.keys():
                author_string += author_dictionary['ForeName']
            else:
                author_string += 'No forename found -- '
            if 'LastName' in author_dictionary.keys():
                author_string += author_dictionary['LastName']
            else:
                author_string += 'No last name found -- '
            affiliation_string = author_dictionary['AffiliationInfo']
            if affiliation_string == []:
                author_string += '  -- No affiliation information found' + '  ,'
            else:
                affiliation_string = affiliation_string[0]['Affiliation']
                author_string += ' ' + affiliation_string + '  ,'
        paper_info['Authors'] = author_string



        #link to the paper
        paper_info['Link'] = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=pubmed&id=" + id_list[
            n] + "&cmd=prlinks&retmode=ref"



        result_list[id_list[n]] = paper_info
        n += 1

    return result_list



# returns the number of query results obtained from pubmed
def get_count(query):
    pubmed_result_count= search_record_count(query)
    return pubmed_result_count['eGQueryResult'][0]['Count']


def spelling_suggestion(query):
    spelling_suggestion = spell_check(query)
    return spelling_suggestion['CorrectedQuery']





# for tests

if __name__ == '__main__':
    result_obtained = spelling_suggestion('(adhd OR addh OR adhs) AND (child OR adolescent) AND (acupuncture)')
    #print result_obtained
    import json
    print(json.dumps(result_obtained, indent=2, separators=(',', ':')))
