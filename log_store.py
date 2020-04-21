import gzip
import os
import sys
import re
import pandas as pd

INPUT_DIR = "/var/log/nginx/"

lineformat1 = re.compile(r"""(?P<ipaddress>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) - - \[(?P<dateandtime>\d{2}\/[a-z]{3}\/\d{4}:\d{2}:\d{2}:\d{2} (\+|\-)\d{4})\] ((\"(GET|POST) )(?P<url>.+)(http\/1\.1")) (?P<statuscode>\d{3}) (?P<bytessent>\d+) (?P<refferer>-|"([^"]+)") (["](?P<useragent>[^"]+)["])""", re.IGNORECASE)
lineformat2 = re.compile(r"""(?P<ipaddress>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) - - \[(?P<dateandtime>\d{2}\/[a-z]{3}\/\d{4}:\d{2}:\d{2}:\d{2} (\+|\-)\d{4})\] ((\"(GET|POST) )(?P<url>.+)(http\/1\.1")) (?P<statuscode>\d{3}) (?P<bytessent>\d+) (["](?P<refferer>(\-)|(.+))["]) (["](?P<useragent>.+)["])""", re.IGNORECASE)

lineformat3 = re.compile(r"""(?P<ipaddress>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) - - \[(?P<dateandtime>\d{2}\/[a-z]{3}\/\d{4}:\d{2}:\d{2}:\d{2} (\+|\-)\d{4})\] ((\"(GET|POST) )(?P<url>.+)(http\/[1-2]\.[0-9]")) (?P<statuscode>\d{3}) (?P<bytessent>\d+) (?P<refferer>-|"([^"]+)") (["](?P<useragent>[^"]+)["])""", re.IGNORECASE)
lineformat4 = re.compile( r"""(?P<ipaddress>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) - (?P<remoteuser>.+) \[(?P<dateandtime>\d{2}\/[a-z]{3}\/\d{4}:\d{2}:\d{2}:\d{2} (\+|\-)\d{4})\] ((\"(?P<method>.+) )(?P<url>.+)(http\/[1-2]\.[0-9]")) (?P<statuscode>\d{3}) (?P<bytessent>\d+) (["](?P<refferer>(\-)|(.+))["]) (["](?P<useragent>.+)["])""", re.IGNORECASE)

def log_reader(INPUT_DIR=INPUT_DIR,lineformat=lineformat1,output='print'):
    
    out=[]
    for f in os.listdir(INPUT_DIR):
        if f.endswith(".gz"):
            logfile = gzip.open(os.path.join(INPUT_DIR, f))
        else:
            logfile = open(os.path.join(INPUT_DIR, f))

        for l in logfile.readlines():
            data = re.search(lineformat, l)
            if data:
                datadict = data.groupdict()
                ip = datadict["ipaddress"]
                datetimestring = datadict["dateandtime"]
                url = datadict["url"]
                bytessent = datadict["bytessent"]
                referrer = datadict["refferer"]
                useragent = datadict["useragent"]
                status = datadict["statuscode"]
                method = data.group(6)
                res=[ip, \
                      datetimestring, \
                      url, \
                      bytessent, \
                      referrer, \
                      useragent, \
                      status, \
                      method]
                if output=='df':
                    out.append(res)
                elif output=='print':
                    print(res)

        logfile.close()

    if output=='df':
        cols=['ip','datetime','url','bytessent','referrer','useragent','statuscode','method']
        return pd.DataFrame(out,columns=cols)

if __name__ == '__main__':
    log_reader()