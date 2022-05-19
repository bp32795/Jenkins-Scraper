import getopt
import jenkins
from datetime import datetime
import sys

from dfCreate import get_job_df
from disable import disable_jobs


def get_server_instance(url, user, passw):
    print("Getting Server Instance . . .")
    server = jenkins.Jenkins(url, username=user, password=passw)
    return server

def main(argv):
    server = ''
    userName = ''
    password = ''
    outfile = 'JenkinsLastBuild'
    disable = ''
    epoch = ''
    try:
        opts, args = getopt.getopt(argv, "hs:u:p:o:d:e", ["server=", "username=", "password=", "outfile=","disable=","epoch="])
    except getopt.GetoptError:
        print('jenkinsScraper.py -s <server> -u <username> -p <token> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('jenkinsScraper.py -s <server> -u <username> -p <token> -o <outputfile> -d <y/n>')
            sys.exit()
        elif opt in ("-s", "--server"):
            server = arg
        elif opt in ("-u", "--username"):
            userName = arg
        elif opt in ("-p", "--password"):
            password = arg
        elif opt in ("-o", "--outfile"):
            outfile = arg
        elif opt in ("-d", "--disable"):
            disable = arg
        elif opt in ("-e", "--epoch"):
            epoch = arg
    server = get_server_instance(server, userName, password)
    if disable != "y" and disable != "yes":
        df = get_job_df(server)
        now = datetime.now()
        outfile = outfile + now.strftime("_%m-%d-%Y_%H-%M-%S") + ".csv"
        df.to_csv(outfile, index=False)
        print("File created at {}.".format(outfile))
    elif disable == "y" or disable == "yes":
        disable_jobs(server,epoch)


if __name__ == '__main__':
    main(sys.argv[1:])
