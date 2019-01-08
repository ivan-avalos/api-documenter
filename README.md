# api-documenter <small style="color: #505050">the easiest way</small>

# JSON to HTML

api-documenter is a simple script that allows you to generate beautiful HTML documentation from a JSON description file easily.

## Requirements
- Python >= 3
- python-slugify >= 1.2.6
- dominate >= 2.3.5

## Credits
| Library | Autor | License | Website |
|---------|--------|--------|---------|
|dominate|Tom Flanagan and Jake Wharton|LGPL v3.0|<https://github.com/Knio/dominate>|
|slugify|Val Neekman|MIT|<https://github.com/un33k/python-slugify>|

## Installation

```bash
pip3 install python-slugify
chmod +x install.sh
./install.sh
apidoc --help
```

## Description structure

**Note:** all the keys should be double quoted and the values should be replaced. See the example for more information.

### API <small>(root)</small>
```typescript
{
    title: string,
    description: string | string[],
    host: string,
    requests: Request[],
    statusCodes: StatusCode[]
}
```

### Request
```typescript
{
    title: string,
    method: string,
    description: string | string[],
    url: string,
    parameters: Parameter[],
    examples: Example[]
}
```

### Parameter
```typescript
{
    name: string,
    type: string,
    optional: boolean,
    description: string
}
```

### Example (request)
```typescript
{
    description: string | string[],
    type: 'request',
    protocol: string = 'HTTP/1.1',
    headers: Header[],
    body: string | string[]
}
```

### Example (response)
```typescript
{
    description: string,
    type: 'response',
    protocol: string = 'HTTP/1.1',
    status: string,
    headers: Header[],
    body: string[]
}
```

### Header
```typescript
{
    key: string,
    value: string
}
```

### StatusCode
```typescript
{
    code: number,
    reason: string,
    meaning: string
}
```

## Full structure
```typescript
{
    title: string,
    description: string,
    host: string,
    requests: [
        {
            title: string,
            method: string,
            description: string | string [],
            url: string,
            parameters: [
                {
                    name: string,
                    type: string,
                    optional: boolean,
                    description: string
                }
            ],
            examples: [
                { // request
                    description: string | string[],
                    type: 'request',
                    protocol: string = 'HTTP/1.1',
                    headers: Header[],
                    body: string | string[]
                },
                { // response
                    description: string,
                    type: 'response',
                    protocol: string = 'HTTP/1.1',
                    status: string,
                    headers: Header[],
                    body: string[]
                }
            ]
        }
    ],
    statusCodes: [
        {
            code: string,
            reason: string,
            meaning: string
        }
    ]
}
```

## License <small>(GPLv3)</small>
```
api-documenter  Copyright (C) 2018  Ivan Avalos <ivan.avalos.diaz@hotmail.com>
This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
This is free software, and you are welcome to redistribute it
under certain conditions; type `show c' for details.
```