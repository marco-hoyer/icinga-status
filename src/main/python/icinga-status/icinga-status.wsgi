import subprocess
from yaml import dump
try:
    from yaml import CDumper as Dumper
except ImportError:
    from yaml import Dumper

'''
Created on 13.09.2013

@author: Marco Hoyer

This simple wsgi application parses icingastatus output to export performance data via yaml.
It excepts a HTTP GET parameter named metrics

Example:
/icinga-status?query=STATUSFILEAGETT,NUMHSTUP
'''
    
def execute(executable, params):
    if isinstance(params, str):
        params = [params]
    command = [executable]
    command.extend(params)
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = p.stdout.read()
    err = p.stderr.read()
    if not p.wait():
        return out
    else:
        print "Error executing " + executable + " : " + err

def convert_query_string_to_list(string):
    if string.startswith("query="):
        return string.lstrip("query=").split(',')
    else:
        return []

def get_icinga_metrics(metric_key_list):
    raw_data = execute("icingastats",['--mrtg','--delimiter=,','--data=' + ','.join(metric_key_list)])
    metric_values_list = raw_data.rstrip(',\n\r').split(',')
    # check if there are string in icingastats output, indicating wrong key names
    for value in metric_values_list:
        if not value.isdigit():
            return []
    return metric_values_list

def get_yaml_dict_from_kv_lists(keys,values):
    if (len(keys) == len(values)):
        # merge keys and values to dict and dump it as string
        return dump( dict(zip(keys, values)), Dumper=Dumper )
    else:
        return None

# handle mod_wsgi requests
def application(environ, start_response):
    
    metric_key_list = convert_query_string_to_list(environ["QUERY_STRING"])
    metric_values_list = get_icinga_metrics(metric_key_list)

    metric_yaml = get_yaml_dict_from_kv_lists(metric_key_list,metric_values_list)
    if not metric_yaml is None: 
        output = metric_yaml
        status = '200 OK'
    else:
        output = 'Error parsing output from icingastats\n  keys: ' + str(metric_key_list) + '\nvalues: ' + str(metric_values_list)
        status = '500 Internal Server Error'
        
    response_headers = [('Content-type', 'text/plain'),
                        ('Content-Length', str(len(output)))]
    start_response(status, response_headers)

    return [output]

if __name__ == '__main__':
    pass
        
