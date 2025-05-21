# API Endpoints Documentation

This document provides information about the available API endpoints in the FastAPI Vue Template project.

## Base URL

All API endpoints are prefixed with `/api/v1`.

## Authentication

Most endpoints require authentication via JWT token. Include the token in the Authorization header:

```
Authorization: Bearer <token>
```

## Endpoints

### Authentication

#### Login

- **URL**: `/api/v1/auth/login`
- **Method**: `POST`
- **Auth Required**: No
- **Request Body**:
  ```json
  {
    "username": "string",
    "password": "string"
  }
  ```
- **Success Response**: 
  ```json
  {
    "access_token": "string",
    "token_type": "bearer"
  }
  ```

#### Get Current User

- **URL**: `/api/v1/users/me`
- **Method**: `GET`
- **Auth Required**: Yes
- **Success Response**: 
  ```json
  {
    "id": "integer",
    "email": "string",
    "username": "string",
    "full_name": "string",
    "is_active": "boolean",
    "is_superadmin": "boolean"
  }
  ```

### Users

#### Get Users

- **URL**: `/api/v1/users/`
- **Method**: `GET`
- **Auth Required**: Yes (Superadmin only)
- **Query Parameters**:
  - `skip`: integer (default: 0)
  - `limit`: integer (default: 100)
- **Success Response**: 
  ```json
  [
    {
      "id": "integer",
      "email": "string",
      "username": "string",
      "full_name": "string",
      "is_active": "boolean"
    }
  ]
  ```

#### Get User by ID

- **URL**: `/api/v1/users/{user_id}`
- **Method**: `GET`
- **Auth Required**: Yes (Superadmin or self)
- **URL Parameters**:
  - `user_id`: integer
- **Success Response**: 
  ```json
  {
    "id": "integer",
    "email": "string",
    "username": "string",
    "full_name": "string",
    "is_active": "boolean"
  }
  ```

#### Create User

- **URL**: `/api/v1/users/`
- **Method**: `POST`
- **Auth Required**: Yes (Superadmin only)
- **Request Body**:
  ```json
  {
    "email": "string",
    "username": "string",
    "password": "string",
    "full_name": "string"
  }
  ```
- **Success Response**: 
  ```json
  {
    "id": "integer",
    "email": "string",
    "username": "string",
    "full_name": "string",
    "is_active": "boolean"
  }
  ```

#### Update User

- **URL**: `/api/v1/users/{user_id}`
- **Method**: `PUT`
- **Auth Required**: Yes (Superadmin or self)
- **URL Parameters**:
  - `user_id`: integer
- **Request Body**:
  ```json
  {
    "email": "string",
    "username": "string",
    "password": "string",
    "full_name": "string",
    "is_active": "boolean"
  }
  ```
- **Success Response**: 
  ```json
  {
    "id": "integer",
    "email": "string",
    "username": "string",
    "full_name": "string",
    "is_active": "boolean"
  }
  ```

#### Delete User

- **URL**: `/api/v1/users/{user_id}`
- **Method**: `DELETE`
- **Auth Required**: Yes (Superadmin only)
- **URL Parameters**:
  - `user_id`: integer
- **Success Response**: 
  ```json
  {
    "message": "User deleted successfully"
  }
  ```

### Organizations

#### Get Organizations

- **URL**: `/api/v1/organizations/`
- **Method**: `GET`
- **Auth Required**: Yes
- **Success Response**: 
  ```json
  [
    {
      "id": "integer",
      "name": "string",
      "description": "string"
    }
  ]
  ```

#### Get Organization by ID

- **URL**: `/api/v1/organizations/{org_id}`
- **Method**: `GET`
- **Auth Required**: Yes
- **URL Parameters**:
  - `org_id`: integer
- **Success Response**: 
  ```json
  {
    "id": "integer",
    "name": "string",
    "description": "string",
    "environments": [
      {
        "id": "integer",
        "name": "string",
        "description": "string"
      }
    ],
    "groups": [
      {
        "id": "integer",
        "name": "string",
        "description": "string"
      }
    ],
    "policies": [
      {
        "id": "integer",
        "name": "string",
        "description": "string"
      }
    ]
  }
  ```

#### Create Organization

- **URL**: `/api/v1/organizations/`
- **Method**: `POST`
- **Auth Required**: Yes (Superadmin only)
- **Request Body**:
  ```json
  {
    "name": "string",
    "description": "string"
  }
  ```
- **Success Response**: 
  ```json
  {
    "id": "integer",
    "name": "string",
    "description": "string"
  }
  ```

#### Update Organization

- **URL**: `/api/v1/organizations/{org_id}`
- **Method**: `PUT`
- **Auth Required**: Yes (Superadmin only)
- **URL Parameters**:
  - `org_id`: integer
- **Request Body**:
  ```json
  {
    "name": "string",
    "description": "string"
  }
  ```
- **Success Response**: 
  ```json
  {
    "id": "integer",
    "name": "string",
    "description": "string"
  }
  ```

#### Delete Organization

- **URL**: `/api/v1/organizations/{org_id}`
- **Method**: `DELETE`
- **Auth Required**: Yes (Superadmin only)
- **URL Parameters**:
  - `org_id`: integer
- **Success Response**: 
  ```json
  {
    "message": "Organization deleted successfully"
  }
  ```

### Environments

#### Get Environments

- **URL**: `/api/v1/environments/`
- **Method**: `GET`
- **Auth Required**: Yes
- **Query Parameters**:
  - `organization_id`: integer (optional)
- **Success Response**: 
  ```json
  [
    {
      "id": "integer",
      "name": "string",
      "description": "string",
      "organization_id": "integer",
      "created_at": "datetime"
    }
  ]
  ```

#### Get Environment by ID

- **URL**: `/api/v1/environments/{env_id}`
- **Method**: `GET`
- **Auth Required**: Yes
- **URL Parameters**:
  - `env_id`: integer
- **Success Response**: 
  ```json
  {
    "id": "integer",
    "name": "string",
    "description": "string",
    "organization_id": "integer",
    "created_at": "datetime",
    "elements": [
      {
        "id": "integer",
        "name": "string",
        "description": "string"
      }
    ]
  }
  ```

#### Create Environment

- **URL**: `/api/v1/environments/`
- **Method**: `POST`
- **Auth Required**: Yes
- **Request Body**:
  ```json
  {
    "name": "string",
    "description": "string",
    "organization_id": "integer"
  }
  ```
- **Success Response**: 
  ```json
  {
    "id": "integer",
    "name": "string",
    "description": "string",
    "organization_id": "integer",
    "created_at": "datetime"
  }
  ```

#### Update Environment

- **URL**: `/api/v1/environments/{env_id}`
- **Method**: `PUT`
- **Auth Required**: Yes (Environment admin only)
- **URL Parameters**:
  - `env_id`: integer
- **Request Body**:
  ```json
  {
    "name": "string",
    "description": "string"
  }
  ```
- **Success Response**: 
  ```json
  {
    "id": "integer",
    "name": "string",
    "description": "string",
    "organization_id": "integer",
    "created_at": "datetime"
  }
  ```

#### Delete Environment

- **URL**: `/api/v1/environments/{env_id}`
- **Method**: `DELETE`
- **Auth Required**: Yes (Environment admin only)
- **URL Parameters**:
  - `env_id`: integer
- **Success Response**: 
  ```json
  {
    "message": "Environment deleted successfully"
  }
  ```

### Elements

#### Get Elements

- **URL**: `/api/v1/elements/`
- **Method**: `GET`
- **Auth Required**: Yes
- **Query Parameters**:
  - `environment_id`: integer (optional)
- **Success Response**: 
  ```json
  [
    {
      "id": "integer",
      "name": "string",
      "description": "string",
      "environment_id": "integer"
    }
  ]
  ```

#### Get Element by ID

- **URL**: `/api/v1/elements/{element_id}`
- **Method**: `GET`
- **Auth Required**: Yes
- **URL Parameters**:
  - `element_id`: integer
- **Success Response**: 
  ```json
  {
    "id": "integer",
    "name": "string",
    "description": "string",
    "environment_id": "integer"
  }
  ```

#### Create Element

- **URL**: `/api/v1/elements/`
- **Method**: `POST`
- **Auth Required**: Yes (Environment admin only)
- **Request Body**:
  ```json
  {
    "name": "string",
    "description": "string",
    "environment_id": "integer"
  }
  ```
- **Success Response**: 
  ```json
  {
    "id": "integer",
    "name": "string",
    "description": "string",
    "environment_id": "integer"
  }
  ```

#### Update Element

- **URL**: `/api/v1/elements/{element_id}`
- **Method**: `PUT`
- **Auth Required**: Yes (Environment admin only)
- **URL Parameters**:
  - `element_id`: integer
- **Request Body**:
  ```json
  {
    "name": "string",
    "description": "string"
  }
  ```
- **Success Response**: 
  ```json
  {
    "id": "integer",
    "name": "string",
    "description": "string",
    "environment_id": "integer"
  }
  ```

#### Delete Element

- **URL**: `/api/v1/elements/{element_id}`
- **Method**: `DELETE`
- **Auth Required**: Yes (Environment admin only)
- **URL Parameters**:
  - `element_id`: integer
- **Success Response**: 
  ```json
  {
    "message": "Element deleted successfully"
  }
  ```

### Groups

#### Get Groups

- **URL**: `/api/v1/groups/`
- **Method**: `GET`
- **Auth Required**: Yes
- **Query Parameters**:
  - `organization_id`: integer (optional)
- **Success Response**: 
  ```json
  [
    {
      "id": "integer",
      "name": "string",
      "description": "string",
      "organization_id": "integer"
    }
  ]
  ```

#### Get Group by ID

- **URL**: `/api/v1/groups/{group_id}`
- **Method**: `GET`
- **Auth Required**: Yes
- **URL Parameters**:
  - `group_id`: integer
- **Success Response**: 
  ```json
  {
    "id": "integer",
    "name": "string",
    "description": "string",
    "organization_id": "integer",
    "users": [
      {
        "id": "integer",
        "username": "string",
        "email": "string"
      }
    ],
    "tags": [
      {
        "id": "integer",
        "value": "string"
      }
    ]
  }
  ```

#### Create Group

- **URL**: `/api/v1/groups/`
- **Method**: `POST`
- **Auth Required**: Yes (Organization admin only)
- **Request Body**:
  ```json
  {
    "name": "string",
    "description": "string",
    "organization_id": "integer"
  }
  ```
- **Success Response**: 
  ```json
  {
    "id": "integer",
    "name": "string",
    "description": "string",
    "organization_id": "integer"
  }
  ```

#### Update Group

- **URL**: `/api/v1/groups/{group_id}`
- **Method**: `PUT`
- **Auth Required**: Yes (Organization admin only)
- **URL Parameters**:
  - `group_id`: integer
- **Request Body**:
  ```json
  {
    "name": "string",
    "description": "string"
  }
  ```
- **Success Response**: 
  ```json
  {
    "id": "integer",
    "name": "string",
    "description": "string",
    "organization_id": "integer"
  }
  ```

#### Delete Group

- **URL**: `/api/v1/groups/{group_id}`
- **Method**: `DELETE`
- **Auth Required**: Yes (Organization admin only)
- **URL Parameters**:
  - `group_id`: integer
- **Success Response**: 
  ```json
  {
    "message": "Group deleted successfully"
  }
  ```

#### Add User to Group

- **URL**: `/api/v1/groups/{group_id}/users/{user_id}`
- **Method**: `POST`
- **Auth Required**: Yes (Organization admin only)
- **URL Parameters**:
  - `group_id`: integer
  - `user_id`: integer
- **Success Response**: 
  ```json
  {
    "message": "User added to group successfully"
  }
  ```

#### Remove User from Group

- **URL**: `/api/v1/groups/{group_id}/users/{user_id}`
- **Method**: `DELETE`
- **Auth Required**: Yes (Organization admin only)
- **URL Parameters**:
  - `group_id`: integer
  - `user_id`: integer
- **Success Response**: 
  ```json
  {
    "message": "User removed from group successfully"
  }
  ```

### Tags

#### Get Tags

- **URL**: `/api/v1/tags/`
- **Method**: `GET`
- **Auth Required**: Yes
- **Success Response**: 
  ```json
  [
    {
      "id": "integer",
      "value": "string"
    }
  ]
  ```

#### Get Tag by ID

- **URL**: `/api/v1/tags/{tag_id}`
- **Method**: `GET`
- **Auth Required**: Yes
- **URL Parameters**:
  - `tag_id`: integer
- **Success Response**: 
  ```json
  {
    "id": "integer",
    "value": "string",
    "users": [
      {
        "id": "integer",
        "username": "string"
      }
    ],
    "groups": [
      {
        "id": "integer",
        "name": "string"
      }
    ],
    "policies": [
      {
        "id": "integer",
        "name": "string"
      }
    ]
  }
  ```

#### Create Tag

- **URL**: `/api/v1/tags/`
- **Method**: `POST`
- **Auth Required**: Yes (Superadmin only)
- **Request Body**:
  ```json
  {
    "value": "string"
  }
  ```
- **Success Response**: 
  ```json
  {
    "id": "integer",
    "value": "string"
  }
  ```

#### Update Tag

- **URL**: `/api/v1/tags/{tag_id}`
- **Method**: `PUT`
- **Auth Required**: Yes (Superadmin only)
- **URL Parameters**:
  - `tag_id`: integer
- **Request Body**:
  ```json
  {
    "value": "string"
  }
  ```
- **Success Response**: 
  ```json
  {
    "id": "integer",
    "value": "string"
  }
  ```

#### Delete Tag

- **URL**: `/api/v1/tags/{tag_id}`
- **Method**: `DELETE`
- **Auth Required**: Yes (Superadmin only)
- **URL Parameters**:
  - `tag_id`: integer
- **Success Response**: 
  ```json
  {
    "message": "Tag deleted successfully"
  }
  ```

### Functions

#### Get Functions

- **URL**: `/api/v1/functions/`
- **Method**: `GET`
- **Auth Required**: Yes
- **Success Response**: 
  ```json
  [
    {
      "id": "integer",
      "name": "string",
      "description": "string"
    }
  ]
  ```

#### Get Function by ID

- **URL**: `/api/v1/functions/{function_id}`
- **Method**: `GET`
- **Auth Required**: Yes
- **URL Parameters**:
  - `function_id`: integer
- **Success Response**: 
  ```json
  {
    "id": "integer",
    "name": "string",
    "description": "string"
  }
  ```

#### Create Function

- **URL**: `/api/v1/functions/`
- **Method**: `POST`
- **Auth Required**: Yes (Superadmin only)
- **Request Body**:
  ```json
  {
    "name": "string",
    "description": "string"
  }
  ```
- **Success Response**: 
  ```json
  {
    "id": "integer",
    "name": "string",
    "description": "string"
  }
  ```

#### Update Function

- **URL**: `/api/v1/functions/{function_id}`
- **Method**: `PUT`
- **Auth Required**: Yes (Superadmin only)
- **URL Parameters**:
  - `function_id`: integer
- **Request Body**:
  ```json
  {
    "name": "string",
    "description": "string"
  }
  ```
- **Success Response**: 
  ```json
  {
    "id": "integer",
    "name": "string",
    "description": "string"
  }
  ```

#### Delete Function

- **URL**: `/api/v1/functions/{function_id}`
- **Method**: `DELETE`
- **Auth Required**: Yes (Superadmin only)
- **URL Parameters**:
  - `function_id`: integer
- **Success Response**: 
  ```json
  {
    "message": "Function deleted successfully"
  }
  ```

### Policies

#### Get Policies

- **URL**: `/api/v1/policies/`
- **Method**: `GET`
- **Auth Required**: Yes
- **Query Parameters**:
  - `organization_id`: integer (optional)
- **Success Response**: 
  ```json
  [
    {
      "id": "integer",
      "name": "string",
      "description": "string",
      "access_schedule": "string",
      "organization_id": "integer"
    }
  ]
  ```

#### Get Policy by ID

- **URL**: `/api/v1/policies/{policy_id}`
- **Method**: `GET`
- **Auth Required**: Yes
- **URL Parameters**:
  - `policy_id`: integer
- **Success Response**: 
  ```json
  {
    "id": "integer",
    "name": "string",
    "description": "string",
    "access_schedule": "string",
    "organization_id": "integer",
    "users": [
      {
        "id": "integer",
        "username": "string"
      }
    ],
    "groups": [
      {
        "id": "integer",
        "name": "string"
      }
    ],
    "tags": [
      {
        "id": "integer",
        "value": "string"
      }
    ],
    "rules": [
      {
        "id": "integer",
        "function_id": "integer",
        "environment_id": "integer",
        "element_id": "integer"
      }
    ]
  }
  ```

#### Create Policy

- **URL**: `/api/v1/policies/`
- **Method**: `POST`
- **Auth Required**: Yes (Organization admin only)
- **Request Body**:
  ```json
  {
    "name": "string",
    "description": "string",
    "access_schedule": "string",
    "organization_id": "integer"
  }
  ```
- **Success Response**: 
  ```json
  {
    "id": "integer",
    "name": "string",
    "description": "string",
    "access_schedule": "string",
    "organization_id": "integer"
  }
  ```

#### Update Policy

- **URL**: `/api/v1/policies/{policy_id}`
- **Method**: `PUT`
- **Auth Required**: Yes (Organization admin only)
- **URL Parameters**:
  - `policy_id`: integer
- **Request Body**:
  ```json
  {
    "name": "string",
    "description": "string",
    "access_schedule": "string"
  }
  ```
- **Success Response**: 
  ```json
  {
    "id": "integer",
    "name": "string",
    "description": "string",
    "access_schedule": "string",
    "organization_id": "integer"
  }
  ```

#### Delete Policy

- **URL**: `/api/v1/policies/{policy_id}`
- **Method**: `DELETE`
- **Auth Required**: Yes (Organization admin only)
- **URL Parameters**:
  - `policy_id`: integer
- **Success Response**: 
  ```json
  {
    "message": "Policy deleted successfully"
  }
  ```

### Rules

#### Get Rules

- **URL**: `/api/v1/rules/`
- **Method**: `GET`
- **Auth Required**: Yes
- **Query Parameters**:
  - `policy_id`: integer (optional)
  - `environment_id`: integer (optional)
  - `element_id`: integer (optional)
  - `function_id`: integer (optional)
- **Success Response**: 
  ```json
  [
    {
      "id": "integer",
      "policy_id": "integer",
      "function_id": "integer",
      "environment_id": "integer",
      "element_id": "integer"
    }
  ]
  ```

#### Get Rule by ID

- **URL**: `/api/v1/rules/{rule_id}`
- **Method**: `GET`
- **Auth Required**: Yes
- **URL Parameters**:
  - `rule_id`: integer
- **Success Response**: 
  ```json
  {
    "id": "integer",
    "policy_id": "integer",
    "function_id": "integer",
    "environment_id": "integer",
    "element_id": "integer",
    "policy": {
      "id": "integer",
      "name": "string"
    },
    "function": {
      "id": "integer",
      "name": "string"
    },
    "environment": {
      "id": "integer",
      "name": "string"
    },
    "element": {
      "id": "integer",
      "name": "string"
    }
  }
  ```

#### Create Rule

- **URL**: `/api/v1/rules/`
- **Method**: `POST`
- **Auth Required**: Yes (Organization admin only)
- **Request Body**:
  ```json
  {
    "policy_id": "integer",
    "function_id": "integer",
    "environment_id": "integer",
    "element_id": "integer"
  }
  ```
- **Success Response**: 
  ```json
  {
    "id": "integer",
    "policy_id": "integer",
    "function_id": "integer",
    "environment_id": "integer",
    "element_id": "integer"
  }
  ```

#### Update Rule

- **URL**: `/api/v1/rules/{rule_id}`
- **Method**: `PUT`
- **Auth Required**: Yes (Organization admin only)
- **URL Parameters**:
  - `rule_id`: integer
- **Request Body**:
  ```json
  {
    "function_id": "integer",
    "environment_id": "integer",
    "element_id": "integer"
  }
  ```
- **Success Response**: 
  ```json
  {
    "id": "integer",
    "policy_id": "integer",
    "function_id": "integer",
    "environment_id": "integer",
    "element_id": "integer"
  }
  ```

#### Delete Rule

- **URL**: `/api/v1/rules/{rule_id}`
- **Method**: `DELETE`
- **Auth Required**: Yes (Organization admin only)
- **URL Parameters**:
  - `rule_id`: integer
- **Success Response**: 
  ```json
  {
    "message": "Rule deleted successfully"
  }
  ```

### Audit Logs

#### Get Audit Logs

- **URL**: `/api/v1/audit-logs/`
- **Method**: `GET`
- **Auth Required**: Yes (Superadmin only)
- **Query Parameters**:
  - `user_id`: integer (optional)
  - `action`: string (optional)
  - `from_date`: datetime (optional)
  - `to_date`: datetime (optional)
  - `skip`: integer (default: 0)
  - `limit`: integer (default: 100)
- **Success Response**: 
  ```json
  [
    {
      "id": "integer",
      "user_id": "integer",
      "action": "string",
      "details": "string",
      "timestamp": "datetime",
      "user": {
        "id": "integer",
        "username": "string"
      }
    }
  ]
  ```

## Error Responses

All endpoints return standardized error responses:

### 400 Bad Request

```json
{
  "detail": "Error message explaining the issue"
}
```

### 401 Unauthorized

```json
{
  "detail": "Not authenticated"
}
```

### 403 Forbidden

```json
{
  "detail": "Not enough permissions"
}
```

### 404 Not Found

```json
{
  "detail": "Resource not found"
}
```

### 422 Validation Error

```json
{
  "detail": [
    {
      "loc": ["body", "field_name"],
      "msg": "Error message",
      "type": "error_type"
    }
  ]
}
```

### 500 Internal Server Error

```json
{
  "detail": "Internal server error"
}
```

## Rate Limiting

API endpoints are rate-limited to prevent abuse. The current limits are:

- 100 requests per minute for authenticated users
- 20 requests per minute for unauthenticated users

When rate limits are exceeded, the API returns a 429 Too Many Requests response.
