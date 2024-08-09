# REST API Endpoints

## 1. Overview

### GET /profiles/overview

Get the total cost of the wall.

**Response:**

```json
{
    "day": "None",
    "cost": 32233500
}
```
  
### GET /profiles/{profile_id}/overview
Get the total cost for a specific profile.

**Response:**

```json
{
    "day": "None",
    "cost": 32233500
}
```

### GET /profiles/overview/{day_id}
Get the total cost for a specific day.

**Response:**

```json
{
    "day": "1",
    "cost": 3334500
}
```

### GET /profiles/{profile_id}/overview/{day_id}
Get the total cost for a specific profile and day.

```json
{
    "day": "1",
    "cost": 1111500
}
```

## 2. Daily Status

### GET /profiles/{profile_id}/days/{day_id}

Get the daily material status for a specific profile.

```json
{
    "day": "None",
    "ice_amount": 585
}
```