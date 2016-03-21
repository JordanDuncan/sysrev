NCBI provides several public APIs that allow programmatic access to many databases and tools.

For this web application, we will be using a Package Biopython.

Biopython is a set of freely available tools for biological computation written in Python by an international team of developers. [2]

It is a distributed collaborative effort to develop Python libraries and applications which address the needs of current and future work in bioinformatics. The source code is made available under the Biopython License, which is extremely liberal and compatible with almost every license in the world.[2]

Specifically we will be using a package, entrez, in Biopython to access the Pubmed data.

Provides code to access NCBI over the WWW.

From the Web Application, we will be sending in an appropriate Query to the API servers and 
gathering the appropriate information obtained back from them.








[ More information on the text below can be found at http://www.ncbi.nlm.nih.gov/books/NBK25499/ ]

Following are some of the Functions/Services provided by the API

  -EInfo (database statistics)

   eutils.ncbi.nlm.nih.gov/entrez/eutils/einfo.fcgi

	Provides the number of records indexed in each field of a given database, the date of the last update of the database, and the available links from the database to other Entrez databases.

  -ESearch (text searches)

   eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi

	Responds to a text query with the list of matching UIDs in a given database (for later use in ESummary, EFetch or ELink), along with the term translations of the query.

  -EPost (UID uploads)

   eutils.ncbi.nlm.nih.gov/entrez/eutils/epost.fcgi

	Accepts a list of UIDs from a given database, stores the set on the History Server, and responds with a query key and web environment for the uploaded dataset.

  -ESummary (document summary downloads)

   eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi

	Responds to a list of UIDs from a given database with the corresponding document summaries.

  -EFetch (data record downloads)

   eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi

	Responds to a list of UIDs in a given database with the corresponding data records in a specified format.

  -ELink (Entrez links)

   eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi

	Responds to a list of UIDs in a given database with either a list of related UIDs (and relevancy scores) in the same database or a list of linked UIDs in another Entrez database; checks for the existence of a specified link from a list of one or more UIDs; creates a hyperlink to the primary LinkOut provider for a specific UID and database, or lists LinkOut URLs and attributes for multiple UIDs.

  -EGQuery (global query)

   eutils.ncbi.nlm.nih.gov/entrez/eutils/egquery.fcgi

	Responds to a text query with the number of records matching the query in each Entrez database.

  -ESpell (spelling suggestions)

   eutils.ncbi.nlm.nih.gov/entrez/eutils/espell.fcgi

    Retrieves spelling suggestions for a text query in a given database.

  -ECitMatch (batch citation searching in PubMed)

   eutils.ncbi.nlm.nih.gov/entrez/eutils/ecitmatch.cgi

	Retrieves PubMed IDs (PMIDs) corresponding to a set of input citation strings.

