from jira.client import JIRA
import argparse
from get_sw_and_hw_versions import VersionFactory

class Jira_HW_SW():
    def __init__(self, MYUSER, MYPASS):
            self.session=JIRA(server=('https://asc.bmwgroup.net/mgujira'), basic_auth=(MYUSER, MYPASS))
    
    def publish(self, PATH):
        ver_factory = VersionFactory('COM13')                                                                                          #need to be parameterized
        versions = ver_factory.get_sw_and_hw_versions()
        if versions[3]=='NotAvailable':
            versions[3]='B3'
        newissue=self.session.search_issues('reporter = currentUser() order by created desc', maxResults=1)                            #read new issue
        taskissue=self.session.issue(newissue[0])
        print(taskissue)
        mydescription=f'SOC: {versions[0]}\nIOC: {versions[1]}\nHW_version: {versions[2]}\nHW_sample: {versions[3]}\nDisplay: AZV370'      
        taskissue.update(description=mydescription, fields={'customfield_13126':[versions[2].split(' ')[0], versions[3]]})
        self.session.add_attachment(taskissue, PATH)
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Script for publish HW and SW on jira')
    parser.add_argument('--user', help="User name")
    parser.add_argument('--passw', help="password")
    parser.add_argument('--path', help="path for the log")
    args = parser.parse_args()
    
    HW_SW=Jira_HW_SW(args.user, args.passw)
    task=HW_SW.publish(args.path)
