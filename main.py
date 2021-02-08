from src.core import create_jira_ticket
from configuration.configuration import log_path, log_level

import logging
import sys
import json


def arg_check():
    logger = logging.getLogger('arg_check')
    try:
        if len(sys.argv) == 4:
            jira_host = sys.argv[1]
            jira_project_key = sys.argv[2]
            issue_type = sys.argv[3]
            if "http://" not in jira_host:
                logger.error('The host URL must start with "http://"  \n'
                             'Received URL: {}'.format(jira_host))
                sys.exit()
            return jira_host, jira_project_key, issue_type
        else:
            logger.error('Not enough or too many arguments were passed. \n'
                         'Argument 1 must be the host url, argument 2 must be the Jira project name and argument 3 must be the issue-type \n'
                         'Example usage: python3 main.py "http://localhost:8085" "test-project" "Bug" < tests/example_alert.json')
            sys.exit()
    except Exception:
        logger.exception("Parsing arguments failed")


def main():
    logger = logging.getLogger('main')
    logging.basicConfig(filename=log_path,
                        filemode='a',
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=log_level)
    jira_host, jira_project_key, issue_type = arg_check()
    logger.debug('Read in stdin json and call create_jira_ticket')
    create_jira_ticket(jira_host=jira_host, jira_project_key=jira_project_key, issue_type=issue_type, alert_json=json.loads(sys.stdin.readline()))


if __name__ == '__main__':
    main()
