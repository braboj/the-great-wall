# REST API Reference

## A. Overview API Endpoints

### GET /profiles/overview

#### Description

```text
Get the total cost of the wall.
```

#### Success Response

```json
{
    "day": "None",
    "cost": 32233500
}
```

#### Error Response

```text
HTTP/1.1 500 Internal Server Error
```

#### Examples

```powershell
PS C:\> Invoke-WebRequest -Uri "http://localhost:8080/profiles/overview" -Method Get

StatusCode        : 200
StatusDescription : OK
Content           : {"day": null, "cost": 32233500}
```
  
### GET /profiles/overview/{day_id}

#### Description

```text
Get the total cost for a specific profile.
```

#### Success Response

```json
{
    "day": "None",
    "cost": 32233500
}
```

#### Error Response

```text
HTTP/1.1 500 Internal Server Error
```

#### Examples

```powershell
PS C:\> Invoke-WebRequest -Uri "http://localhost:8080/profiles/overview/1" -Method Get

StatusCode        : 200
StatusDescription : OK
Content           : {"day": 1, "cost": 3334500}
```

### GET /profiles/{profile_id}/overview/{day_id}

#### Description

```text
Get the total cost for a specific profile and day.
```

#### Success Response

```json
{
    "day": "1",
    "cost": 1111500
}
```

#### Error Response

```text
HTTP/1.1 500 Internal Server Error
```


#### Examples

```powershell
PS C:\> Invoke-WebRequest -Uri "http://localhost:8080/profiles/1/overview/1" -Method Get

StatusCode        : 200
StatusDescription : OK
Content           : {"day": 1, "cost": 1111500}
```

## B. Daily Status API Endpoints

### GET /profiles/{profile_id}/days/{day_id}

#### Description

```text
Get the daily material status for a specific profile.
```

#### Success Response

```json
{
    "day": "None",
    "ice_amount": 585
}
```

#### Error Response

```text
HTTP/1.1 500 Internal Server Error
```

#### Examples

```powershell
PS C:\> Invoke-WebRequest -Uri "http://localhost:8080/profiles/1/days/1" -Method Get
StatusCode        : 200
StatusDescription : OK
Content           : {"day": 1, "ice": 585}
```

## C. Configuration API Endpoints

### GET /profiles/config

#### Description

```text
Get the configuration parameters to construct the wall.
```

#### Success Response

```json
{
  "volume_ice_per_foot": 195,
  "cost_per_volume": 1900,
  "target_height": 30,
  "max_section_count": 2000,
  "build_rate": 1,
  "num_teams": 20,
  "cpu_worktime": 0.01,
  "profiles": [
    [21, 25, 28],
    [17],
    [17, 22, 17, 19, 17]
  ]
}
```

#### Error Response

```text
HTTP/1.1 500 Internal Server Error
```

#### Examples

```powershell
PS C:\> Invoke-WebRequest -Uri "http://localhost:8080/profiles/config" -Method Get

StatusCode        : 200
StatusDescription : OK
Content           : {"volume_ice_per_foot": 195, "cost_per_volume": 1900, "target_height": 30, "max_section_count":
                    2000, "build_rate": 1, "num_teams": 20, "cpu_worktime": 0.01, "profiles": [[21, 25, 28], [17],
                    [17, 22, ...
```

### POST /profiles/config

#### Description

```text
Set the configuration parameter to construct the wall.

{
  "volume_ice_per_foot": 195,
  "cost_per_volume": 1900,
  "target_height": 30,
  "max_section_count": 2000,
  "build_rate": 1,
  "num_teams": 20,
  "cpu_worktime": 0.01,
  "profiles": [
    [21, 25, 28],
    [17],
    [17, 22, 17, 19, 17]
  ]
}
```

#### Success Response

```text
{"status": "success"}
```

#### Error Response

```text
HTTP/1.1 400 Bad Request
```

#### Examples

```powershell
PS C:\> PS C:\> Invoke-WebRequest -Uri "http://localhost:8080/profiles/config/" -Method Post -ContentType "application/json" -Body '{"num_teams": 20, "profiles": [[1, 1, 1], [2, 2, 2]]}'

StatusCode        : 200
StatusDescription : OK
Content           : {"status": "success"}
```


## D. Logs API Endpoints

### GET /profiles/logs

#### Description

```text
Get the logs for the wall construction process.
```

#### Success Response

```text
{"status": "success"}
```

#### Error Response

```text
HTTP/1.1 500 Internal Server Error
```

#### Examples

```powershell
PS C:\> Invoke-WebRequest -Uri "http://localhost:8080/profiles/logs" -Method Get

StatusCode        : 200
StatusDescription : OK
Content           : {"logs": ["2024-08-11 14:23:43,316 INFO     Worker-108      - Added 1 foot to section 0 to reach 22 feet on day 1\n",
                    "2024-08-11 14:23:43,341 INFO     Worker-108      - Added 1 foot to section 2 to r...
                    
```