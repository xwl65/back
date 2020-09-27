import datetime, time
from jenkinsapi.jenkins import *
from jenkinsapi.job import *
from jenkinsapi.build import Build
def test_List():
    jenkins = Jenkins(
        'http://localhost:8080',
        username='x',
        password='11bc63a77c1808e57f2dfeaafef3fc7f31')
    count = 0
    for job_name in jenkins.keys():
        my_job = jenkins.get_job(job_name)
        count = count + 1
    #print “Job” + str(count) + " : "+job_name
        print(count)
        print(my_job)
