# Port Schemas Backups
This script is to backup the schemas for the following assets inside of your Port tenancy
* Blueprints
* Scorecards
* Automations/Self-Service Actions

Please note, Pages are not included at this stage due to the Pages API still being in beta and subject to change.

The schemas are stored as JSON and can be used to restore a scheme or cherry pick attributes as required. If you need to restore an entire scheme, please note that the schemas will contain `createdAt, createdBy, updatedAt, updatedBy` metadata attributes that will need to be removed from the schema before restoring. You can simply copy paste the result JSON object into the JSON field for your corresponding blueprint using the JSON edit mode in the UI.

```
    {
      "id": "sc_GPA1aVwQHf1Qxva9",
      "identifier": "devops-tool-health",
      "title": "DevOps Tool Health",
      ...
      ...
      ...
      "createdAt": "2025-05-22T06:44:32.615Z",
      "createdBy": "dxhRBelM8pZiZ0kw7B9ghG5eGOMSbIJR",
      "updatedAt": "2025-05-22T06:44:32.615Z",
      "updatedBy": "dxhRBelM8pZiZ0kw7B9ghG5eGOMSbIJR"
    }
```

## What is created?
A .zip archive containing all the JSON schemas for Blueprints, Scorecards, Automations and Self-Service Actions. The zip file is saved to the same directory as the script. The archive takes the following structure
```
├── port-schemas-backup
│   ├── blueprints
│   │   ├── my-blueprint.json
│   │   ├── ...
│   │   ├── ...
│   ├── scorecards
│   │   ├── my-scorecard.json
│   │   ├── ...
│   │   ├── ...
│   ├── actions
│   │   ├── my-action.json
│   │   ├── ...
│   │   ├── ...
```

## How to run
Get your Port Client Id and Client Secret from Port
```
export PORT_CLIENT_ID=<your Port Client ID>
export PORT_CLIENT_SECRET=<your Port Client Secret>
```

```
pip install -r requirements.txt
python main.py
```