from datetime import datetime


def disable_jobs(server,epoch):
    for job in reversed(server.get_jobs(folder_depth=None)):
        info = server.get_job_info(job.get("fullname"))
        jobName = info.get("fullName")

        try:
            last_build_number = info['lastCompletedBuild']['number']
        except:
            if info['_class'] == 'com.cloudbees.hudson.plugins.folder.Folder':
                print(jobName + " is a folder . . .")
                continue
            elif info['_class']== 'org.jenkinsci.plugins.workflow.multibranch.WorkflowMultiBranchProject':
                continue
            else:
                try:
                    print(jobName + " is color: "+job.get('color'))
                    continue
                except:
                    print(jobName + " is super weird . . .")
                    continue

        build_info = server.get_build_info(jobName, last_build_number)
        last_build_time = build_info.get('timestamp') / 1000
        color = job.get('color')
        if last_build_time < epoch and color != "disabled":
            try:
                server.disable_job(jobName)
                print("Disabled "+jobName)
                print("Last date was " + str(datetime.fromtimestamp(build_info.get('timestamp') / 1000)))
            except:
                print(jobName + " was not disabled." )
        elif last_build_time > 1609459200:
            print(jobName + " was last built "+str(datetime.fromtimestamp(build_info.get('timestamp') / 1000)))
        elif color == "disabled":
            print(jobName + " was already disabled.")