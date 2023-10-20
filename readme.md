# Hotel API Challenges

This Hotel API was build use Django Rest Framework with learning purpose about DRF. For running this project, you must install Django and DRF First. You can follow the installation for that frameworks here.

## Requirements
1. Python
2. PIP
3. Some text editor (Atom, VS Code, etc.)

## Installation

Before you install django, you must make virtual environtment first

```bash
python -m venv env
env\scripts\activate
```

In some cases you want to deactivate the virtual environment, you can try this command

```bash
deactivate
```


Use the package manager [pip](https://pip.pypa.io/en/stable/) to install django and rest-framework.

```bash
pip install django rest-framework
```

## Running the Project

Before you run the project, make sure you have in the project folder.

After all done, you can run the project using this command.

```bash
python manage.py runserver
```

All have done, and now you can explore this project.

# API Documentation

You can try the API with some application such as Postman or you can just make some request from your favorite web browser or terminal.

## Rooms Endpoints

This API serves for GET, POST, PUT, DELETE method.

### GET

```
http://127.0.0.1:8000/api/rooms/
```

### Response

```
[
   {
      "id": 1,
      "number": 10,
      "floor": 1
   },
   {
      "id": 2,
      "number": 15,
      "floor": 1
   }
]
```

### GET

```
http://127.0.0.1:8000/api/rooms/:id/
```

### Response

```
{
   "id": :id,
   "number": 10,
   "floor": 1
}
```

### POST

```
http://127.0.0.1:8000/api/rooms/
```

### Form-Data

| Field | Type | Required |
| :-----: | :---: | :---: |
| number | integer | yes |
| floor | integer | yes |


### Response

```
{
   "id": 3,
   "number": 19,
   "floor": 1
}
```

### PUT

```
http://127.0.0.1:8000/api/rooms/:id/
```

### Form-Data

| Field | Type | Required |
| :-----: | :---: | :---: |
| number | integer | yes |
| floor | integer | yes |


### Response

```
{
   "id": :id,
   "number": 10,
   "floor": 1
}
```

### DELETE

```
http://127.0.0.1:8000/api/rooms/:id/
```

### Response

```
[]
```
/


## Guests Endpoints

This API serves for GET, POST, PUT, DELETE method.

### GET

```
http://127.0.0.1:8000/api/guests/
```

### Response

```
[
   {
      "id": 1,
      "name": "Muhammad Imron"
   },
   {
      "id": 2,
      "name": "Ahmad Jamaludin"
   }
]
```

### GET

```
http://127.0.0.1:8000/api/guests/:id/
```

### Response

```
{
   "id": :id,
   "name": "Muhammad Imron"
}
```

### POST

```
http://127.0.0.1:8000/api/guests/
```

### Form-Data

| Field | Type | Required |
| :-----: | :---: | :---: |
| name | string | yes |


### Response

```
{
   "id": 3,
   "name": "Muhammad Normian"
}
```

### PUT

```
http://127.0.0.1:8000/api/guests/:id/
```

### Form-Data

| Field | Type | Required |
| :-----: | :---: | :---: |
| name | string | yes |


### Response

```
{
   "id": :id,
   "name": "Muhammad Updated"
}
```

### DELETE

```
http://127.0.0.1:8000/api/guests/:id/
```

### Response

```
[]
```

## Bookings Endpoints

This API serves for GET, POST, PUT, DELETE method.

### GET

```
http://127.0.0.1:8000/api/bookings/
```

### Response

```
[
    {
        "id": 1,
        "start_date": "2023-10-20T09:19:00Z",
        "end_date": "2023-10-21T09:19:00Z",
        "room_id": 2,
        "room": {
            "number": 12,
            "floor": 1
        },
        "guest_id": 1,
        "guest": {
            "name": "Muhammad Imron"
        },
        "is_deleted": false,
        "deleted_at": null
    },
    {
        "id": 2,
        "start_date": "2023-10-20T09:19:00Z",
        "end_date": "2023-10-21T09:19:00Z",
        "room_id": 2,
        "room": {
            "number": 12,
            "floor": 1
        },
        "guest_id": 2,
        "guest": {
            "name": "Muhammad Normian"
        },
        "is_deleted": true,
        "deleted_at": "2023-10-20T03:40:16.648272Z"
    }
]
```

### GET

```
http://127.0.0.1:8000/api/bookings/:id/
```

### Response

```
{
    "id": :id,
    "start_date": "2023-10-20T09:19:00Z",
    "end_date": "2023-10-21T09:19:00Z",
    "room_id": 2,
    "room": {
        "number": 12,
        "floor": 1
    },
    "guest_id": 2,
    "guest": {
        "name": "Muhammad Normian"
    },
    "is_deleted": true,
    "deleted_at": "2023-10-20T03:40:16.648272Z"
}
```

### POST

```
http://127.0.0.1:8000/api/bookings/
```

### Form-Data

| Field | Type | Required |
| :-----: | :---: | :---: |
| start_date | datetime | yes |
| end_date | datetime | yes |
| room_id | fk(rooms) | yes |
| guest_id | fk(guests) | yes |

### Response

```
{
    "id": 3,
    "start_date": "2023-10-20T09:19:00Z",
    "end_date": "2023-10-21T09:19:00Z",
    "room_id": 2,
    "room": {
        "number": 12,
        "floor": 1
    },
    "guest_id": 1,
    "guest": {
        "name": "Muhammad Imron"
    },
    "is_deleted": false,
    "deleted_at": null
}
```

### PUT

```
http://127.0.0.1:8000/api/bookings/:id/
```

### Form-Data

| Field | Type | Required |
| :-----: | :---: | :---: |
| start_date | datetime | yes |
| end_date | datetime | yes |
| room_id | fk(rooms) | yes |
| guest_id | fk(guests) | yes |

### Response

```
{
    "id": :id,
    "start_date": "2023-10-20T09:19:00Z",
    "end_date": "2023-10-21T09:19:00Z",
    "room_id": 2,
    "room": {
        "number": 12,
        "floor": 1
    },
    "guest_id": 1,
    "guest": {
        "name": "Muhammad Imron"
    },
    "is_deleted": false,
    "deleted_at": null
}
```

### DELETE

This endpoint for hard delete.

```
http://127.0.0.1:8000/api/bookings/:id/
```

### Response

```
[]
```

### DELETE

This endpoint for soft delete.

```
http://127.0.0.1:8000/api/bookings/:id/?soft=true
```

### Response

```
[]
```

## Another Endpoints

### GET

This endpoint for getting bookings list for users. Booking which have soft delete marks will hidden here.

```
http://127.0.0.1:8000/api/bookings-users/
```

### Response

```
[
    {
        "id": 1,
        "start_date": "2023-10-20T09:19:00Z",
        "end_date": "2023-10-21T09:19:00Z",
        "room_id": 2,
        "room": {
            "number": 12,
            "floor": 1
        },
        "guest_id": 1,
        "guest": {
            "name": "Muhammad Imron"
        },
        "is_deleted": false,
        "deleted_at": null
    }
]
```

### GET

This endpoint for getting spesific bookings for users. Booking which have soft delete marks will hidden here.

```
http://127.0.0.1:8000/api/bookings-users/:id/
```

### Response

```
{
    "id": 1,
    "start_date": "2023-10-20T09:19:00Z",
    "end_date": "2023-10-21T09:19:00Z",
    "room_id": 2,
    "room": {
        "number": 12,
        "floor": 1
    },
    "guest_id": 1,
    "guest": {
        "name": "Muhammad Imron"
    },
    "is_deleted": false,
    "deleted_at": null
}
```