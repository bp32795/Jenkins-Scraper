# Jenkins Scraper

This Jenkins Python Tool will either A) gather all jobs and information about them including last commit author, JDK version, Last success, last build regardless of status, and other data, or B) disable all jobs that last ran before a designated epoch. 


## Installation
Requires
 - Python 3
 - A Jenkins Token that has access to the rest API
 - Running the below command in the directory

```bash
  pip install -r requirements
```
    
## Usage/Examples

Gather All Successful Jobs and their last successful build and JDK version.
```bash
jenkinsScraper.py -s "<JenkinsServer>" -u "<UserID>" -p <tokenFromJenkins>
```
Disable all jobs last ran before 2021.
```bash
jenkinsScraper.py -s "<JenkinsServer>" -u "<UserID>" -p <tokenFromJenkins> -d "yes" -epoch 1640995200
```