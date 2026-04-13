import sys
sys.path.append("C:\\Users\\Jonathan.Venturi\\AppData\\Local\\Packages\\PythonSoftwareFoundation.Python.3.9_qbz5n2kfra8p0\\LocalCache\\local-packages\\Python39\\site-packages")
sys.path.append("C:\\Users\\Jonathan.Venturi\\AppData\\Local\\Packages\\PythonSoftwareFoundation.Python.3.9_qbz5n2kfra8p0\\LocalCache\\local-packages\\Python39\\Scripts")

from jira import JIRA

jira = JIRA('https://jira.atlassian.com')

issue = jira.issue('PRO-1000')
print(issue.fields.project.key)            # 'JRA'
