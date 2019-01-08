import json, sys, getopt, dominate
from dominate.tags import *
from dominate.util import raw
from slugify import slugify

usage="""usage: apidoc [-hadx] -i input -o output -s css

Options:
    --help          -h  Show this help menu.
    --about         -a  Show about message.
    --structure     -x  Show API description structure.
    ––dark          -d  Use dark theme only for Bootstrap CSS.
    --input=<file>  -i  JSON formatted input file.
    --output=<file> -o  HTML formatted output.
    --style=<file>  -s  Path to CSS style (can be URL).

Example:
    apidoc -i example.json -o example.html
    apidoc -i example.json -o example.html --dark
    apidoc -i example.json -o example.html  -s example.css
"""

about="""api-documenter  Copyright (C) 2018  Ivan Avalos <ivan.avalos.diaz@hotmail.com>
This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
This is free software, and you are welcome to redistribute it
under certain conditions; type `show c' for details."""

structure="""API:
    title: string
    description: string | string[] # string per line
    host: string
    requests: Request[]
    statusCodes: StatusCode[]

Request:
    title: string
    method: string
    description: string | string[]
    url: string
    parameters: Parameter[]
    examples: Example[]

Parameter:
    name: string
    type: string
    optional: boolean
    description: string

Example(request):
    description: string | string[]
    type: "request"
    protocol: string = 'HTTP/1.1'
    headers: Header[]
    body: string | string[]

Example(response):
    description: string
    type: "response"
    protocol: string = 'HTTP/1.1'
    status: string
    headers: Header[]
    body: string[]

Header:
    key: string
    value: string

StatusCode:
    code: string
    reason: string
    meaning: string
"""

css_style="""
    /* Prettify CSS styles. */
    pre {
    white-space: pre-line;
    white-space: pre-wrap;       /* Since CSS 2.1 */
    white-space: -moz-pre-wrap;  /* Mozilla, since 1999 */
    white-space: -pre-wrap;      /* Opera 4-6 */
    white-space: -o-pre-wrap;    /* Opera 7 */
    word-wrap: break-word;       /* Internet Explorer 5.5+ */
    }
    
    /* desert scheme ported from vim to google prettify */
    pre.prettyprint { 
    font-family: monospace;
    font-size: 13px;
    background-color: #1e1e1e;
    border: 0 !important;
    margin-bottom: 0px;
    }
    pre .nocode { background-color: none; color: #000 }
    pre .str { color: #ffa0a0 } /* string  - pink */
    pre .kwd { color: #f0e68c; font-weight: bold }
    pre .com { color: #87ceeb } /* comment - skyblue */
    pre .typ { color: #98fb98 } /* type    - lightgreen */
    pre .lit { color: #cd5c5c } /* literal - darkred */
    pre .pun { color: #fff }    /* punctuation */
    pre .pln { color: #fff }    /* plaintext */
    pre .tag { color: #f0e68c; font-weight: bold } /* html/xml tag    - lightyellow */
    pre .atn { color: #bdb76b; font-weight: bold } /* attribute name  - khaki */
    pre .atv { color: #ffa0a0 } /* attribute value - pink */
    pre .dec { color: #98fb98 } /* decimal         - lightgreen */
    
    /* Specify class=linenums on a pre to get line numbering */
    ol.linenums { margin-top: 0; margin-bottom: 0; color: #AEAEAE } /* IE indents via margin-left */
    li.L0,li.L1,li.L2,li.L3,li.L5,li.L6,li.L7,li.L8 { list-style-type: none }
    /* Alternate shading for lines */
    li.L1,li.L3,li.L5,li.L7,li.L9 { }
    
    @media print {
    pre.prettyprint { background-color: none }
    pre .str, code .str { color: #060 }
    pre .kwd, code .kwd { color: #006; font-weight: bold }
    pre .com, code .com { color: #600; font-style: italic }
    pre .typ, code .typ { color: #404; font-weight: bold }
    pre .lit, code .lit { color: #044 }
    pre .pun, code .pun { color: #440 }
    pre .pln, code .pln { color: #000 }
    pre .tag, code .tag { color: #006; font-weight: bold }
    pre .atn, code .atn { color: #404 }
    pre .atv, code .atv { color: #060 }
    }

    /* Other CSS styles. */
    .example {
        font-family: monospace;
    }
"""

# Argument parsing
try:
    opts, args = getopt.getopt(sys.argv[1:], 
        "haxdi:o:s:", [
            "help", 
            "about", 
            "structure", 
            "dark", 
            "input=", 
            "output=", 
            "style="
        ])
except getopt.GetoptError as err:
    print(str(err))
    print(usage)
    sys.exit(2)

input = None
output = None
style = None
dark = False

for o, _a in opts:
    if o in ('-h', '--help'):
        print (usage)
        sys.exit(0)
    elif o in ('-a', '--about'):
        print (about)
        sys.exit(0)
    elif o in ('-x', '--structure'):
        print (structure)
        sys.exit(0)
    elif o in ('-i', '--input'):
        input = _a
    elif o in ('-o', '--output'):
        output = _a
    elif o in ('-s', '--style'):
        style = _a
    elif o in ('-d', '--dark'):
        dark = True
    else:
        print (usage)
        sys.exit(2)

# Input and output are required
if input is None or output is None:
    print ('Input and output required')
    sys.exit(2)
    
# Open files
input_file = open(input, 'r')
output_file = open(output, 'w')

# Parse JSON input
json_api = json.loads(input_file.read())

def get(json, abskey, options=None):
    key = abskey.split('.')[-1]
    if key in json:
        #check if value matches with any option
        if isinstance(options, list):
            if json[key] in options:
                return json[key]
            else:
                raise Exception('Parameter "' + abskey + '" must be in ' + str(options))
        return json[key]
    else:
        raise Exception('Missing "' + abskey + '"')

def get_multiline(json, abskey):
    get(json, abskey)
    key = abskey.split('.')[-1]
    if isinstance(json[key], str): #single line description
        return json[key]
    elif isinstance(json[key], list): #multi line description
        return ' '.join(json[key])
    else: raise Exception('Parameter "' + abskey + '" should be of type str or list')

def get_code(json, abskey):
    get_multiline(json, abskey)
    key = abskey.split('.')[-1]
    if isinstance(json[key], str): #single line code
        return json[key]
    elif isinstance(json[key], list): #multi line code
        return '\n'.join(json[key])

# CSS Styles
bootstrap_css = 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css'
external_styles = [
    'https://raw.githubusercontent.com/google/code-prettify/master/styles/desert.css'
]
external_scripts = [
    'https://cdn.rawgit.com/google/code-prettify/master/loader/run_prettify.js'
]
css_style += ("""
    body {
    background: #252526;
    color: white;
    }
    .card {
    -webkit-box-shadow: 0px 2px 4px 0px rgba(0,0,0,1);
    -moz-box-shadow: 0px 2px 4px 0px rgba(0,0,0,1);
    box-shadow: 0px 2px 4px 0px rgba(0,0,0,1);
    }
""" if dark else """
    body {
    background: #f8fafc;
    color: black;
    }
    .card {
    -webkit-box-shadow: 0px 2px 4px 0px rgba(191,191,191,1);
    -moz-box-shadow: 0px 2px 4px 0px rgba(191,191,191,1);
    box-shadow: 0px 2px 4px 0px rgba(191,191,191,1);
    }
""")

# CSS Classes
card = 'card border-0 mb-3 bg-dark' if dark else 'card border-0 mb-3'
_a = 'text-white' if dark else ''
_table = \
'table table-dark table-striped table-bordered' if dark else  \
'table table-striped table-bordered'
http_table = 'table table-sm table-borderless table-dark example'

# Start creating HTML output
html_output = html()
with html_output:
    with head():
        meta(charset='utf-8')
        meta(name='viewport', content='width=device-width, initial-scale=1, shrink-to-fit=no')

        # api.title
        title(get(json_api, 'api.title'))

        # css
        link(rel='stylesheet', type='text/css', href=style if style else bootstrap_css)
        for s in external_styles: 
            link(type='text/css', href=s)
        raw('\n<style>' + css_style + '</style>\n')
    # api
    with body():
        with div(_class='container'):
            # api.title
            h1(raw(get(json_api, 'api.title')), _class='display-4 mt-3')

            index_root = div(_class=card)
            index_body = index_root.add(div(_class='card-body'))
            with index_body:
                # api.description
                p(raw(get_multiline(json_api, 'api.description')), _class='card-text lead')
                # api.statusCodes
                h1('Status codes')
                with table(_class=_table):
                    with thead():
                        with tr():
                            th('Status code')
                            th('Reason')
                            th('Meaning')
                    with tbody():
                        for status in json_api['statusCodes']:
                            with tr():
                                td(get(status, 'code'))
                                td(get(status, 'reason'))
                                td(get(status, 'meaning'))
                # index
                h1('Index')
            index = index_body.add(ol())

            # api.requests
            for i, request in enumerate(get(json_api, 'api.requests')):
                # add to index
                index += li(a(raw(get(request, 'api.request.title')),
                    href='#' + str(i), _class=_a), __pretty=False)
                
                with div(_class=card, id=i):
                    with div(_class='card-header'):
                        # api.request.title
                        h1(raw(get(request, 'api.request.title')), _class='display-5')
                    with div(_class='card-body'):
                        # api.request.description
                        p(raw(get_multiline(request, 'api.request.description')), _class='card-text lead')
                        # api.request.url
                        h3('URL')
                        with p():
                            with code():
                                b(get(request, 'api.request.method'))
                                span(get(request, 'api.request.url'))
                        # api.request.parameters (optional)
                        if 'parameters' in request and len(request['parameters']) > 0:
                            h3('Parameters')
                            with div(_class='table-responsive-sm'):
                                with table(_class=_table):
                                    with thead():
                                        with tr():
                                            th('Name')
                                            th('Type')
                                            th('Optional')
                                            th('Description')
                                    with tbody():
                                        for param in request['parameters']:
                                            with tr():
                                                td(get(param, 'name'))
                                                td(get(param, 'type'))
                                                td('Yes' if get(param, 'optional') else '')
                                                td(get(param, 'description'))
                        # api.request.examples (optional)
                        if 'examples' in request and len(request['examples']) > 0:
                            h3('Examples')
                            for example in request['examples']:
                                # api.request.example.type
                                if get(example, 'api.request.example.type', options=['request', 'response']):
                                    if example['type'] == 'request':
                                        span('Request', _class='card-text lead')
                                    elif example['type'] == 'response':
                                        span('Response', _class='card-text lead')
                                # api.request.example.description
                                if 'description' in example:
                                    p(raw(get_multiline(example, 'api.request.example.description')))

                                with table(_class=http_table):
                                    with tr():
                                        with td():
                                            # api.request.example.protocol (optional)
                                            if 'protocol' in example:
                                                span(example['protocol'])
                                            else: 
                                                span('HTTP/1.1')
                                            
                                            # api.request.example.{method, url}
                                            if example['type'] == 'request':
                                                b(request['method'])
                                                b(request['url'])
                                            # api.request.example.{status}
                                            elif example['type'] == 'response':
                                                span(get(example, 'status'))
                                    # api.request.example.headers (optional)
                                    if 'headers' in example:
                                        for header in example['headers']:
                                            tr(td(get(header, 'key') + ': ' + get(header, 'value')))
                                    # api.request.example.body (optional)
                                    if 'body' in example:
                                        with tr():
                                            with td():
                                                code(pre(get_code(example, 'body'),  _class='prettyprint'))
        # footer
        with footer():
            with div(_class='container py-5'):
                with p(_class='mb-0 text-uppercase font-weight-bold small text-justify'):
                    a('Documentation generated with api-documenter', 
                        href='https://github.com/ivan-avalos/api-documenter', 
                        _class='text-muted float-right',
                        rel='noopener')

        # external scripts
        for js in external_scripts:
            script(src=js)

output_file.write(html_output.render())
