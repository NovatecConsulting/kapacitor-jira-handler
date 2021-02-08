from configuration.configuration import user, password, end_status
from atlassian import Jira
from requests.exceptions import HTTPError
import logging

logger = logging.getLogger('core')


def parse_existing_issues(issues, summary) -> bool:
    for issue in issues:
        if issue['fields']['summary'] == summary and not str(issue['fields']['status']['name']) == end_status:
            logger.debug('Issue with given summary already exists and is not set to {status}\n'
                         'Please ensure that the end status <{status}> exists.'.format(status=end_status))
            return True
    return False


def create_jira_ticket(jira_host: str, jira_project_key: str, issue_type: str, alert_json) -> None:
    try:
        jira = Jira(url=jira_host, username=user, password=password)

        # search issues
        search_issues_jql = "project={}".format(jira_project_key)
        issues = jira.jql(search_issues_jql)

        # create issue if not exists in the start status
        if not parse_existing_issues(issues['issues'], alert_json['message']):
            issue_dict = {
                'project': {'key': '{}'.format(jira_project_key)},
                'summary': alert_json['message'],
                'description': alert_json['details'].replace('<br>', '\n'),
                'issuetype': {'name': issue_type}
            }
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
