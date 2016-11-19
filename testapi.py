import urllib2


app_id = 'be604784'
app_key = '28ac20cf27d3c8286f9991ad120acaed'

result = urllib2.urlopen("http://api.adzuna.com:80/v1/api/jobs/gb/search/1?app_id=be604784&app_key=28ac20cf27d3c8286f9991ad120acaed&results_per_page=20&what=javascript%20developer&what_exclude=java&where=london&sort_by=salary&salary_min=30000&full_time=1&permanent=1&content-type=application/json"
).read()
print result
