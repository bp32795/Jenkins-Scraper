import pandas as pd
from datetime import datetime
import xml.etree.ElementTree as ET

def get_job_df(server):
    df = pd.DataFrame(
        columns=['JobName', 'LastRunDate', 'LastSuccessfulBuild', 'LastSuccessfulBuildDate', 'JDK', 'URL', 'lastrunbyUserID', 'userName', "lastCommit",
                 "lastCommitMessage", "lastCommitAuthor", "lastCommitEmail", "last_status", "enabled"])
    for job in server.get_jobs(folder_depth=None):
        info = server.get_job_info(job.get("fullname"))
        jobName = info.get("fullName")
        print("========================================")
        print("Gather data for :: " + jobName)
        try:
            try:
                last_build_number = info['lastCompletedBuild']['number']
            except:
                if info['_class'] == 'com.cloudbees.hudson.plugins.folder.Folder':
                    print(jobName + " is a folder . . .")
                else:
                    last_build_time = 0
                    jdk = "None"

            build_info = server.get_build_info(jobName, last_build_number)
            if build_info.get("result") != "SUCCESS":
                try:
                    for i in reversed(range(last_build_number)):
                        lastSuccess = server.get_build_info(jobName, i)
                        if lastSuccess.get("result")=="SUCCESS":
                            lastSuccessDate = datetime.fromtimestamp(lastSuccess.get('timestamp') / 1000)
                            lastSuccessBuild = i
                            break
                        else:
                            lastSuccessDate = datetime.fromtimestamp(build_info.get('timestamp') / 1000)
                            lastSuccessBuild = last_build_number
                except:
                    print("\n\n BAD THING \n\n")
                    lastSuccessDate = datetime.fromtimestamp(build_info.get('timestamp') / 1000)
                    lastSuccessBuild = last_build_number


            job_url = build_info.get("url")
            if 'changeSet' in build_info:
                if len(build_info['changeSet']) > 0:
                    try:
                        commit = build_info['changeSet']['items'][0]['commitId']
                        commit_author = build_info['changeSet']['items'][0]['author']['fullName']
                        commit_email = build_info['changeSet']['items'][0]['authorEmail']
                        commit_message = build_info['changeSet']['items'][0]['comment']
                    except:
                        commit = "Not Available"
                        commit_author = "Not Available"
                        commit_email = "Not Available"
                        commit_message = "Not Available"
            elif 'changeSets' in build_info:

                if len(build_info['changeSets']) > 0:
                    print("\n\n\n++++++++++++++++++++++++++\n\n\n")
                    try:
                        print("\n\n\n++++++++++++++++++++++++++\n\n\n")
                        commit = build_info['changeSets'][0]['items'][0]['commitId']
                        commit_author = build_info['changeSets'][0]['items'][0]['author']['fullName']
                        commit_email = build_info['changeSets'][0]['items'][0]['authorEmail']
                        commit_message = build_info['changeSets'][0]['items'][0]['comment']
                    except:
                        commit = "Not Available"
                        commit_author = "Not Available"
                        commit_email = "Not Available"
                        commit_message = "Not Available"
            else:
                commit = "Not Available"
                commit_author = "Not Available"
                commit_email = "Not Available"
                commit_message = "Not Available"
            try:
                userID = build_info['actions'][0]['causes'][0]['userId']
                username = build_info['actions'][0]['causes'][0]['userName']
            except:
                userID = "Timer"
                username = "Timer"
            if username == "":
                username = "None given"
            result = build_info.get('result')
            color = job.get('color')
            last_build_time = datetime.fromtimestamp(build_info.get('timestamp') / 1000)
            xml = server.get_job_config(info.get("fullName")).replace("\n", "")
            try:
                jdk = ET.fromstring(xml).findall('jdk')[0].text
            except:
                jdk = "Not Found"
            if color == "disabled":
                enabled = "F"
            else:
                enabled = "T"
            df.loc[len(df.index)] = [jobName, last_build_time, lastSuccessDate, lastSuccessBuild, jdk, job_url, userID, username, commit, commit_message,
                                     commit_author, commit_email, result, enabled]
            print(
                "Wrote:: " + str([jobName, str(last_build_time), str(lastSuccessDate), lastSuccessBuild, jdk, job_url, userID, username, commit, commit_message,
                                  commit_author, commit_email, result, enabled]))
        except:
            #print("There was an error . . .")
            pass
    return df