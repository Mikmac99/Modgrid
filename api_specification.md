# ModularGrid Price Monitor - API Specification

## Overview

This document outlines the RESTful API endpoints for the ModularGrid Price Monitor web application. The API is built using Flask and follows RESTful principles.

## Base URL

All API endpoints are prefixed with `/api/v1`.

## Authentication

Most endpoints require authentication using JSON Web Tokens (JWT).

- Authentication tokens are obtained via the `/api/v1/auth/login` endpoint
- Tokens must be included in the `Authorization` header as `Bearer {token}`
- Tokens expire after 24 hours

## Endpoints

### Authentication

#### Login

```
POST /api/v1/auth/login
```

Authenticates a user with ModularGrid credentials.

**Request Body:**
```json
{
  "username": "string",
  "password": "string"
}
```

**Response:**
```json
{
  "token": "string",
  "user": {
    "id": "integer",
    "username": "string",
    "email": "string"
  }
}
```

**Status Codes:**
- 200: Success
- 401: Invalid credentials

#### Logout

```
POST /api/v1/auth/logout
```

Invalidates the current authentication token.

**Response:**
```json
{
  "message": "Successfully logged out"
}
```

**Status Codes:**
- 200: Success
- 401: Unauthorized

#### Check Status

```
GET /api/v1/auth/status
```

Checks if the current authentication token is valid.

**Response:**
```json
{
  "authenticated": "boolean",
  "user": {
    "id": "integer",
    "username": "string",
    "email": "string"
  }
}
```

**Status Codes:**
- 200: Success
- 401: Unauthorized

### User Settings

#### Get Settings

```
GET /api/v1/user/settings
```

Retrieves the current user's settings.

**Response:**
```json
{
  "scan_interval": "integer",
  "default_threshold": "float",
  "regions": "string",
  "notification_email": "string",
  "email_notifications_enabled": "boolean",
  "quiet_hours_start": "string",
  "quiet_hours_end": "string"
}
```

**Status Codes:**
- 200: Success
- 401: Unauthorized

#### Update Settings

```
PUT /api/v1/user/settings
```

Updates the current user's settings.

**Request Body:**
```json
{
  "scan_interval": "integer",
  "default_threshold": "float",
  "regions": "string",
  "notification_email": "string",
  "email_notifications_enabled": "boolean",
  "quiet_hours_start": "string",
  "quiet_hours_end": "string"
}
```

**Response:**
```json
{
  "message": "Settings updated successfully",
  "settings": {
    "scan_interval": "integer",
    "default_threshold": "float",
    "regions": "string",
    "notification_email": "string",
    "email_notifications_enabled": "boolean",
    "quiet_hours_start": "string",
    "quiet_hours_end": "string"
  }
}
```

**Status Codes:**
- 200: Success
- 400: Invalid request
- 401: Unauthorized

### Watchlist

#### Get Watchlist

```
GET /api/v1/user/watchlist
```

Retrieves the current user's watchlist.

**Response:**
```json
{
  "watchlist": [
    {
      "id": "integer",
      "module": {
        "id": "integer",
        "modulargrid_id": "integer",
        "name": "string",
        "manufacturer": "string",
        "type": "string",
        "hp_width": "integer",
        "depth": "float",
        "image_url": "string"
      },
      "threshold_percentage": "float",
      "max_price": "float"
    }
  ]
}
```

**Status Codes:**
- 200: Success
- 401: Unauthorized

#### Add to Watchlist

```
POST /api/v1/user/watchlist
```

Adds a module to the current user's watchlist.

**Request Body:**
```json
{
  "module_id": "integer",
  "threshold_percentage": "float",
  "max_price": "float"
}
```

**Response:**
```json
{
  "message": "Module added to watchlist",
  "watchlist_item": {
    "id": "integer",
    "module": {
      "id": "integer",
      "modulargrid_id": "integer",
      "name": "string",
      "manufacturer": "string",
      "type": "string",
      "hp_width": "integer",
      "depth": "float",
      "image_url": "string"
    },
    "threshold_percentage": "float",
    "max_price": "float"
  }
}
```

**Status Codes:**
- 201: Created
- 400: Invalid request
- 401: Unauthorized
- 409: Module already in watchlist

#### Remove from Watchlist

```
DELETE /api/v1/user/watchlist/{id}
```

Removes a module from the current user's watchlist.

**Response:**
```json
{
  "message": "Module removed from watchlist"
}
```

**Status Codes:**
- 200: Success
- 401: Unauthorized
- 404: Watchlist item not found

### Monitoring

#### Get Status

```
GET /api/v1/monitor/status
```

Gets the current monitoring status.

**Response:**
```json
{
  "is_monitoring": "boolean",
  "last_scan": "string (ISO datetime)",
  "next_scan": "string (ISO datetime)",
  "listings_scanned": "integer",
  "deals_found": "integer"
}
```

**Status Codes:**
- 200: Success
- 401: Unauthorized

#### Start Monitoring

```
POST /api/v1/monitor/start
```

Starts the monitoring process.

**Response:**
```json
{
  "message": "Monitoring started",
  "session_id": "integer",
  "next_scan": "string (ISO datetime)"
}
```

**Status Codes:**
- 200: Success
- 401: Unauthorized
- 409: Monitoring already active

#### Stop Monitoring

```
POST /api/v1/monitor/stop
```

Stops the monitoring process.

**Response:**
```json
{
  "message": "Monitoring stopped",
  "session_summary": {
    "start_time": "string (ISO datetime)",
    "end_time": "string (ISO datetime)",
    "listings_scanned": "integer",
    "deals_found": "integer"
  }
}
```

**Status Codes:**
- 200: Success
- 401: Unauthorized
- 404: No active monitoring session

#### Run Single Scan

```
POST /api/v1/monitor/scan
```

Runs a single scan of the ModularGrid marketplace.

**Response:**
```json
{
  "message": "Scan completed",
  "listings_scanned": "integer",
  "deals_found": "integer",
  "scan_time": "string (ISO datetime)"
}
```

**Status Codes:**
- 200: Success
- 401: Unauthorized
- 429: Too many requests

### Deals

#### Get All Deals

```
GET /api/v1/deals
```

Gets all current deals.

**Query Parameters:**
- `page`: Page number (default: 1)
- `per_page`: Items per page (default: 20)
- `sort_by`: Field to sort by (default: "deal_percentage")
- `sort_dir`: Sort direction ("asc" or "desc", default: "desc")
- `min_percentage`: Minimum deal percentage (default: 0)
- `region`: Filter by region (default: all)

**Response:**
```json
{
  "deals": [
    {
      "id": "integer",
      "module": {
        "id": "integer",
        "modulargrid_id": "integer",
        "name": "string",
        "manufacturer": "string",
        "type": "string",
        "hp_width": "integer",
        "depth": "float",
        "image_url": "string"
      },
      "price": "float",
      "currency": "string",
      "condition": "string",
      "seller": "string",
      "region": "string",
      "date_listed": "string (ISO datetime)",
      "deal_percentage": "float",
      "url": "string"
    }
  ],
  "pagination": {
    "total": "integer",
    "pages": "integer",
    "current_page": "integer",
    "per_page": "integer"
  }
}
```

**Status Codes:**
- 200: Success
- 401: Unauthorized

#### Get Watchlist Deals

```
GET /api/v1/deals/watchlist
```

Gets deals for modules in the user's watchlist.

**Query Parameters:**
- `page`: Page number (default: 1)
- `per_page`: Items per page (default: 20)
- `sort_by`: Field to sort by (default: "deal_percentage")
- `sort_dir`: Sort direction ("asc" or "desc", default: "desc")

**Response:**
```json
{
  "deals": [
    {
      "id": "integer",
      "module": {
        "id": "integer",
        "modulargrid_id": "integer",
        "name": "string",
        "manufacturer": "string",
        "type": "string",
        "hp_width": "integer",
        "depth": "float",
        "image_url": "string"
      },
      "price": "float",
      "currency": "string",
      "condition": "string",
      "seller": "string",
      "region": "string",
      "date_listed": "string (ISO datetime)",
      "deal_percentage": "float",
      "url": "string",
      "watchlist_threshold": "float"
    }
  ],
  "pagination": {
    "total": "integer",
    "pages": "integer",
    "current_page": "integer",
    "per_page": "integer"
  }
}
```

**Status Codes:**
- 200: Success
- 401: Unauthorized

#### Get Deal Details

```
GET /api/v1/deals/{id}
```

Gets details for a specific deal.

**Response:**
```json
{
  "id": "integer",
  "module": {
    "id": "integer",
    "modulargrid_id": "integer",
    "name": "string",
    "manufacturer": "string",
    "type": "string",
    "hp_width": "integer",
    "depth": "float",
    "image_url": "string"
  },
  "price": "float",
  "currency": "string",
  "condition": "string",
  "seller": "string",
  "region": "string",
  "date_listed": "string (ISO datetime)",
  "deal_percentage": "float",
  "url": "string",
  "price_history": [
    {
      "price": "float",
      "currency": "string",
      "condition": "string",
      "date_sold": "string (ISO datetime)"
    }
  ],
  "average_price": "float",
  "median_price": "float"
}
```

**Status Codes:**
- 200: Success
- 401: Unauthorized
- 404: Deal not found

### Modules

#### Search Modules

```
GET /api/v1/modules/search
```

Searches for modules.

**Query Parameters:**
- `q`: Search query
- `page`: Page number (default: 1)
- `per_page`: Items per page (default: 20)
- `manufacturer`: Filter by manufacturer
- `type`: Filter by module type

**Response:**
```json
{
  "modules": [
    {
      "id": "integer",
      "modulargrid_id": "integer",
      "name": "string",
      "manufacturer": "string",
      "type": "string",
      "hp_width": "integer",
      "depth": "float",
      "image_url": "string"
    }
  ],
  "pagination": {
    "total": "integer",
    "pages": "integer",
    "current_page": "integer",
    "per_page": "integer"
  }
}
```

**Status Codes:**
- 200: Success
- 401: Unauthorized

#### Get Module Details

```
GET /api/v1/modules/{id}
```

Gets details for a specific module.

**Response:**
```json
{
  "id": "integer",
  "modulargrid_id": "integer",
  "name": "string",
  "manufacturer": "string",
  "type": "string",
  "hp_width": "integer",
  "depth": "float",
  "image_url": "string",
  "current_listings_count": "integer",
  "average_price": "float",
  "median_price": "float",
  "lowest_current_price": "float",
  "in_watchlist": "boolean"
}
```

**Status Codes:**
- 200: Success
- 401: Unauthorized
- 404: Module not found

#### Get Module Price History

```
GET /api/v1/modules/{id}/price-history
```

Gets price history for a specific module.

**Query Parameters:**
- `period`: Time period ("1m", "3m", "6m", "1y", "all", default: "6m")
- `condition`: Filter by condition ("mint", "excellent", "good", "fair", "poor", default: all)

**Response:**
```json
{
  "module": {
    "id": "integer",
    "modulargrid_id": "integer",
    "name": "string",
    "manufacturer": "string"
  },
  "price_history": [
    {
      "price": "float",
      "currency": "string",
      "condition": "string",
      "date_sold": "string (ISO datetime)"
    }
  ],
  "statistics": {
    "average_price": "float",
    "median_price": "float",
    "lowest_price": "float",
    "highest_price": "float",
    "price_trend": "float" // percentage change over period
  }
}
```

**Status Codes:**
- 200: Success
- 401: Unauthorized
- 404: Module not found

### Notifications

#### Get Notifications

```
GET /api/v1/notifications
```

Gets notifications for the current user.

**Query Parameters:**
- `page`: Page number (default: 1)
- `per_page`: Items per page (default: 20)
- `unread_only`: Filter to unread notifications only (default: false)

**Response:**
```json
{
  "notifications": [
    {
      "id": "integer",
      "message": "string",
      "is_read": "boolean",
      "created_at": "string (ISO datetime)",
      "listing_id": "integer"
    }
  ],
  "pagination": {
    "total": "integer",
    "pages": "integer",
    "current_page": "integer",
    "per_page": "integer"
  },
  "unread_count": "integer"
}
```

**Status Codes:**
- 200: Success
- 401: Unauthorized

#### Mark Notification as Read

```
PUT /api/v1/notifications/{id}/read
```

Marks a notification as read.

**Response:**
```json
{
  "message": "Notification marked as read"
}
```

**Status Codes:**
- 200: Success
- 401: Unauthorized
- 404: Notification not found

#### Mark All Notifications as Read

```
PUT /api/v1/notifications/read-all
```

Marks all notifications as read.

**Response:**
```json
{
  "message": "All notifications marked as read",
  "count": "integer"
}
```

**Status Codes:**
- 200: Success
- 401: Unauthorized

## Error Responses

All error responses follow this format:

```json
{
  "error": "string",
  "message": "string",
  "status_code": "integer"
}
```

## Rate Limiting

- API requests are limited to 100 requests per minute per user
- Exceeding this limit will result in a 429 Too Many Requests response

## Versioning

The API uses versioning in the URL path (e.g., `/api/v1/`) to ensure backward compatibility as the API evolves.
