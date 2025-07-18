# Jira API Documentation

This document outlines the available Jira REST APIs and their capabilities for the Closinglock Jira instance.

## Base Configuration

- **Base URL**: `https://closinglock.atlassian.net`
- **API Version**: REST API v2
- **Authentication**: Basic Auth with username and API token

## Available API Endpoints

### 1. Issue Management

#### Create Issue
- **Endpoint**: `POST /rest/api/2/issue`
- **Status**: ✅ Working
- **Description**: Creates a new issue in Jira
- **Required Fields**:
  - `project.key` - Project key (e.g., "FIN")
  - `summary` - Issue summary/title
  - `description` - Issue description in Jira markup
  - `issuetype.name` - Issue type (e.g., "Task", "Story", "Bug")
  - `priority.name` - Priority level (e.g., "Medium", "High", "Low")

- **Optional Fields**:
  - `assignee.name` - Assignee username
  - `parent.key` - Parent issue key for sub-tasks
  - `labels` - Array of labels
  - `components` - Array of component IDs
  - `fixVersions` - Array of version IDs
  - `customfield_10008` - Epic Link (Epic key)

#### Update Issue
- **Endpoint**: `PUT /rest/api/2/issue/{issue_key}`
- **Status**: ✅ Working
- **Description**: Updates an existing issue
- **Updatable Fields**:
  - `summary` - Issue summary
  - `description` - Issue description
  - `assignee.name` - Assignee
  - `priority.name` - Priority
  - `labels` - Labels
  - `components` - Components
  - `fixVersions` - Fix versions
  - `customfield_10008` - Epic Link

#### Get Issue
- **Endpoint**: `GET /rest/api/2/issue/{issue_key}`
- **Status**: ✅ Working
- **Description**: Retrieves issue details including all fields

#### Get Issue Edit Metadata
- **Endpoint**: `GET /rest/api/2/issue/{issue_key}/editmeta`
- **Status**: ✅ Working
- **Description**: Returns available fields and their edit capabilities

### 2. Comments

#### Add Comment
- **Endpoint**: `POST /rest/api/2/issue/{issue_key}/comment`
- **Status**: ✅ Working
- **Description**: Adds a comment to an existing issue
- **Required Fields**:
  - `body` - Comment content in Jira markup

#### Get Comments
- **Endpoint**: `GET /rest/api/2/issue/{issue_key}/comment`
- **Status**: ✅ Working
- **Description**: Retrieves all comments for an issue

### 3. Time Tracking

#### Update Time Estimate
- **Endpoint**: `PUT /rest/api/2/issue/{issue_key}` with `timetracking` field
- **Status**: ❌ Not Available
- **Error**: `Field 'timetracking' cannot be set. It is not on the appropriate screen, or unknown.`
- **Note**: Time tracking must be managed through the Jira web interface

### 4. Issue Links

#### Create Issue Link
- **Endpoint**: `POST /rest/api/2/issueLink`
- **Status**: ✅ Available (not tested)
- **Description**: Creates links between issues

#### Get Issue Links
- **Endpoint**: `GET /rest/api/2/issue/{issue_key}?fields=issuelinks`
- **Status**: ✅ Working
- **Description**: Retrieves linked issues

### 5. Attachments

#### Upload Attachment
- **Endpoint**: `POST /rest/api/2/issue/{issue_key}/attachments`
- **Status**: ✅ Available (not tested)
- **Description**: Uploads files as attachments to an issue

### 6. Worklogs

#### Add Worklog
- **Endpoint**: `POST /rest/api/2/issue/{issue_key}/worklog`
- **Status**: ✅ Available (not tested)
- **Description**: Adds time spent on an issue

#### Get Worklogs
- **Endpoint**: `GET /rest/api/2/issue/{issue_key}/worklog`
- **Status**: ✅ Available (not tested)
- **Description**: Retrieves worklog entries

## Available Issue Types

Based on the edit metadata, the following issue types are available:

1. **Task** (ID: 10002) - A task that needs to be done
2. **Story** (ID: 10001) - Stories track functionality or features expressed as user goals
3. **Bug** (ID: 10004) - A problem which impairs or prevents the functions of the product
4. **Epic** (ID: 10000) - A big user story that needs to be broken down

## Available Priorities

1. **Highest** (ID: 1)
2. **High** (ID: 2)
3. **Medium** (ID: 3) - Default
4. **Low** (ID: 4)
5. **Lowest** (ID: 5)

## Available Components

1. **Client Portal** (ID: 10010) - All things related to Closinglock Client Experience
2. **Company Portal** (ID: 10011) - Closinglock user home and TPS integrations
3. **Employee Portal** (ID: 10012)
4. **Other** (ID: 10013) - Misc.
5. **Pricing Calculator** (ID: 10014) - Sales Pricing Calculator

## Custom Fields

### Epic Link
- **Field Key**: `customfield_10008`
- **Type**: Epic Link
- **Description**: Links issues to epics
- **Operations**: `["set"]`

### Sprint
- **Field Key**: `customfield_10010`
- **Type**: Sprint field
- **Description**: Assigns issues to sprints
- **Operations**: `["set"]`

### Category
- **Field Key**: `customfield_10033`
- **Type**: Select field
- **Description**: Categorizes issues
- **Allowed Values**:
  - Software research & development
  - Software upkeep & maintenance
- **Operations**: `["set"]`

### Tester
- **Field Key**: `customfield_10074`
- **Type**: User picker
- **Description**: Assigns a tester to the issue
- **Operations**: `["set"]`

## Limitations and Restrictions

### 1. Time Tracking
- **Issue**: Cannot set `timetracking` field via API
- **Workaround**: Use Jira web interface for time estimates
- **Impact**: Time estimates must be set manually

### 2. Field Permissions
- Some fields may not be editable depending on:
  - User permissions
  - Issue status
  - Screen configurations
  - Workflow restrictions

### 3. Issue Type Restrictions
- Epic issues cannot be edited or deleted via API
- Some issue types may have restricted operations

## Authentication

### Basic Auth
```bash
curl -u "username:api_token" \
  -H "Accept: application/json" \
  -H "Content-Type: application/json" \
  "https://closinglock.atlassian.net/rest/api/2/issue/PROJ-123"
```

### Session-based Auth
```python
import requests

session = requests.Session()
session.auth = (username, api_token)
session.headers.update({
    'Accept': 'application/json',
    'Content-Type': 'application/json'
})
```

## Error Handling

### Common HTTP Status Codes
- **200**: Success (GET requests)
- **201**: Created (POST requests)
- **204**: No Content (PUT/DELETE requests)
- **400**: Bad Request (invalid data)
- **401**: Unauthorized (invalid credentials)
- **403**: Forbidden (insufficient permissions)
- **404**: Not Found (resource doesn't exist)
- **409**: Conflict (business rule violation)

### Error Response Format
```json
{
  "errorMessages": [],
  "errors": {
    "field_name": "Error description"
  }
}
```

## Best Practices

1. **Rate Limiting**: Respect API rate limits
2. **Error Handling**: Always check response status codes
3. **Field Validation**: Use edit metadata to validate field availability
4. **Batch Operations**: Use bulk operations when possible
5. **Logging**: Log API requests and responses for debugging

## Testing Commands

### Test Issue Creation
```bash
python3 jira_markdown_converter.py input/jira/spike/example.md \
  --base-url https://closinglock.atlassian.net \
  --username your-email@closinglock.com \
  --api-token your-api-token \
  --project-key FIN \
  --issue-type Task \
  --priority Medium
```

### Test Issue Update
```bash
python3 jira_markdown_converter.py input/jira/spike/example.md \
  --base-url https://closinglock.atlassian.net \
  --username your-email@closinglock.com \
  --api-token your-api-token \
  --project-key FIN \
  --issue-key FIN-123
```

### Test Comment Addition
```bash
python3 jira_markdown_converter.py input/jira/spike/example.md \
  --base-url https://closinglock.atlassian.net \
  --username your-email@closinglock.com \
  --api-token your-api-token \
  --project-key FIN \
  --issue-key FIN-123 \
  --as-comment
```

## Notes

- This documentation is based on testing with the Closinglock Jira instance
- API availability may vary based on Jira configuration and user permissions
- Always test new API calls in a development environment first
- Keep API tokens secure and rotate them regularly