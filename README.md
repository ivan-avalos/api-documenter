# api-documenter - easiest way of document your APIs

api-documenter is a simple Python script that allows you to generate beautiful HTML documentation from a JSON file with a single command.

## Requirements
- **Python** >= 3
- **python-slugify** >= 1.2.6

## Credits
| Library | Autor | License | Website |
|---------|--------|--------|---------|
|htmldom|Bhimsen.S.Kulkarni|BSD|<https://pypi.org/project/htmldom/>|
|slugify|Val Neekman|MIT|<https://github.com/un33k/python-slugify>|

## Installation

```bash
pip3 install python-slugify
chmod +x install.sh
./install.sh
apidoc --help
```

## Structure

### API

```json
{
  "title": "API Title",
  "description": "API Description",
  "host": "http://endpoint.host",
  "requests": [], optional
}
```

### Request

```json
{
  "title": "Request title",
  "method": "Method",
  "description": "Request description",
  "url": "/api/request",
  "parameters": [], optional
  "examples":[] optional
  
}
```

### Parameter

```json
{
  "name": "parameter1",
  "type": "data type",
  "optional": false,
  "description": "Parameter description"
}
```

### Request example

```json
{
  "description": "Example request description",
  "type": "request",
  "method": "POST",
  "protocol": "HTTP/1.1", optional
  "headers": [ optional
    {
      "key": "Header key 1",
      "value": "Header value 1"
    }
  ],
  "body": [ optional
    "line 1 of body",
    "line 2 of body"
  ]
}
```

### Response example

```json
{
  "description": "Example response description",
  "type": "response",
  "protocol": "HTTP/1.1", optional
  "status": "200 OK",
  "headers": [ optional
    {
      "key": "Header key 1",
      "value": "Header value 1"
    },
  ],
  "body": [ optional
    "line 1 of body",
    "line 2 of body",
  ]
}
```

### Full structure

```json
{
  "title": "API Title",
  "description": "API Description",
  "host": "http://endpoint.host",
  "requests": [
    {
      "title": "Request title",
      "method": "Method",
      "description": "Request description",
      "url": "/api/request",
      "parameters": [
        {
          "name": "parameter1",
          "type": "data type",
          "optional": false,
          "description": "Parameter description"
        }
      ],
      "examples": [
        {
          "description": "Example request description",
          "type": "request",
          "method": "POST",
          "protocol": "HTTP/1.1",
          "headers": [
            {
              "key": "Header key 1",
              "value": "Header value1"
            }
          ],
          "body": "single line body"
        },
        {
          "description": "Example response description",
          "type": "response",
          "protocol": "HTTP/1.1",
          "status": "200 OK",
          "headers": [
            {
              "key": "Header key 1",
              "value": "Header value 1"
            }
          ],
          "body": [
            "line 1 of body",
            "line 2 of body",
            "line 3 of body"
          ]
        }
      ]
    }
  ]
}
```
