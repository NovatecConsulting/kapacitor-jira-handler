# Python Jira API for Kapacitor Alerts 
This project was developed for the Alerting UI in the **inspectIT Ocelot - Configuration Server** [Project](https://github.com/inspectIT/inspectit-ocelot/tree/master/components/inspectit-ocelot-configurationserver).

## Usage
* Download the [kapacitor-jira-handler.zip](https://github.com/NovatecConsulting/kapacitor-jira-handler/releases) 
from the latest Release or create a zip file with all required files with `make bundle`
* Create a "handler script" directory, copy and unzip the ZIP file there. *For example under the kapacitor load directory: 
`/etc/kapacitor/load/handler_scripts/jira-api`.*  
This path is required later in the handler-files. 
* Navigate to the handler script path and install all dependencies: `pip3 install -r requirements.txt`
* To use the Jira handler, create one or more handler-files `<custom_name>.yml` under the `/etc/kapacitor/load/handlers` directory.
* Edit the [configurations](configuration) to your specifications *(log path and level, user, password and workflow end status)*.

### Handler-file example
```yml
# /etc/kapacitor/load/handlers/jira-handler-team1.yml
    id: jira-issue-handler_team_1                               # handler id in the Ocelot - Configuration Server UI
topic: jira_team_1                                              # channel in the Ocelot - Configuration Server UI
kind: exec
options:
  prog: '/usr/bin/python3'                                      # path to python3
  args:
    - '/etc/kapacitor/load/handler_scripts/jira-api/main.py'    # entrypoint path (required)
    - 'http://jira-host                         '               # jira host (required)
    - 'project-name'                                            # jira project key (required)
    - 'Bug'                                                     # jira issue type (required)
```
Note that the entrypoint path must be refer to the previous unzipped directory.
The handlers are visible on the inspectIT Ocelot - Configuration Server UI.

### Config
The log path and level, jira user, password and workflow end status can be edited in the [configuration.py](configuration/configuration.py) file.

### Testing
The script can be tested with the [example.json](tests/example_alert.json) file: `python3 main.py "http://<jira-host>" "<project-key>" "<issue-type>" < tests/example_alert.json'`
