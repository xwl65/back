from jenkinsapi.jenkins import Jenkins

def test_jenkins():
    jenkins = Jenkins(
        'http://localhost:8080',
        username='x',
        password='11bc63a77c1808e57f2dfeaafef3fc7f31')

    jenkins['testcase'].invoke(securitytoken='11bc63a77c1808e57f2dfeaafef3fc7f31',
                               build_params={
                                   'testcases': '.'

                               })

    print(jenkins['testcase'].get_last_build().get_console())

    