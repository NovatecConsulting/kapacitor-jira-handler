from configuration.configuration import user, password, end_status
from atlassian import Jira
from requests.exceptions import HTTPError
import logging

logger = logging.getLogger('core')

# api body template
issue_dict = {
    'project': {'key': ''},
    'summary': '',
    'description': '',
    'issuetype': {'name': ''},
    'labels': []
}


def parse_issues_exists(issues, alert_id: str, alert_level: str) -> bool:
    no_creation = False

    for issue in issues:
        if alert_id in issue['fields']['labels'] and not str(issue['fields']['status']['name']) == end_status:
            logger.debug('Issue with given id <{id}> already exists and is not set to {status}\n'
                         'Please also ensure that the end status <{status}> exists.'.format(id=alert_id, status=end_status))
            if alert_level not in issue['fields']['labels']:
                issue_dict['issuekey'] = issue['key']
                break
            no_creation = True
        break
    return no_creation


def create_jira_ticket(jira_host: str, jira_project_key: str, issue_type: str, alert_json) -> None:
    try:
        jira = Jira(url=jira_host, username=user, password=password)

        # search issues
        search_issues_jql = "project={}".format(jira_project_key)
        issues = jira.jql(search_issues_jql)

        # prepare issue api body
        issue_dict['project']['key'] = jira_project_key
        issue_dict['summary'] = alert_json['message']
        issue_dict['description'] = alert_json['details'].replace('<br>', '\n')
        issue_dict['issuetype']['name'] = issue_type
        issue_dict['labels'] = [alert_json['id'], alert_json['level']]

        # create issue if not exists in the start status
        if not parse_issues_exists(issues['issues'], alert_json['id'], alert_json['level']):
            new_issue = jira.issue_create_or_update(fields=issue_dict)
            logger.debug('Issue "{}" has been created'.format(new_issue))

    except HTTPError as error:
        response_text = error.response.text
        if "issue type is required" in response_text:
            logger.exception("Issue Type <{}> dose not exists!".format(issue_type))
        else:
            logger.exception(response_text)
    except ConnectionError:
        logger.exception('Connection error')
    except Exception:
        logger.exception("Triggering the jira issue handler failed")
