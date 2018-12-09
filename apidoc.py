#!/usr/bin/python3
# api-documenter - The simpliest way of documenting your API
# Copyright (C) 2018  Ivan Avalos <ivan.avalos.diaz@hotmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
import json, sys
from htmldom import htmldom
from slugify import slugify

usage="""usage: {0} [--help | --about | --example] input output [css]

Options:
    --help     Show this help menu
    --about    Show about message
    --example  Show example of input

Example:
    {0} example.json example.html
    {0} example.json example.html example.css (override stylesheet)"""

about="""api-documenter  Copyright (C) 2018  Ivan Avalos <ivan.avalos.diaz@hotmail.com>
This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
This is free software, and you are welcome to redistribute it
under certain conditions; type `show c' for details."""

example="""
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
"""

# Argument validation
if len(sys.argv) == 2:
    if sys.argv[1] == '--help':
        print(usage.format(sys.argv[0]))
    elif sys.argv[1] == '--about':
        print(about)
    elif sys.argv[1] == '--example':
        print(example)
    else: print(usage.format(sys.argv[0]))
    exit()
if len(sys.argv) < 3:
    print(usage.format(sys.argv[0]))
    exit()

# Input files
input_file=open(sys.argv[1], 'r')
output_file=open(sys.argv[2], 'w')

# Input data
json_apidoc=json.loads(input_file.read())
# Output HTML DOM
html_apidoc=htmldom.HtmlDom().createDom('<html><head></head><body style="background: #f5f8fa"></body></html>')

# Base URL
if 'host' in json_apidoc:
    api_host=json_apidoc['host']
else: raise Exception('Missing API host')

dom_body = html_apidoc.find("body")
dom_head = html_apidoc.find("head")

# API Title
if 'title' in json_apidoc:
    dom_head.append("<title>"+json_apidoc['title']+"</title>")
else: raise Exception('Missing API title')

# Optionally override default stylesheet
if len(sys.argv) >= 4:
    dom_head.append('<link rel="stylesheet" href="'+sys.argv[3]+'">')
else:
    dom_head.append('''<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css"
    crossorigin="anonymous">''')

dom_body.append("<div class='container'>")
dom_container = dom_body.find("div.container")

# API Title
dom_container.append("<h1 class='mt-3'>"+json_apidoc['title']+"</h1>")
# API Description
dom_container.append("<div class='card mb-3'><div class='card-body'><p class='card-text lead'>"+json_apidoc['description']+"</p></div></div>")

# Request Index
dom_container.append("<div class='card mb-3 index'><div class='card-body'><h1>Index</h1></div>")
dom_index = dom_container.find("div.index").first()
dom_index_body = dom_index.find("div").first()
dom_index_body.append("<ol></ol>")
dom_index_list = dom_index_body.find("ol").first()

# API Requests
for i in json_apidoc['requests']:
    # Index
    dom_index_list.append("<li><a href='#"+slugify(i['title'])+"'>"+i['title']+"</a></li>")
    
    dom_container.append("<div class='card mb-3 mt-3' id='"+slugify(i['title'])+"'></div>")
    dom_request_card = dom_container.find('div.card').last()
    # Request Title
    if 'title' in i: dom_request_card.append("<h1 class='display-4 card-header'>"+i['title']+"</h1>")
    else: raise Exception('Missing request title')
    
    dom_request_card.append("<div class='card-body'></div>")
    dom_request_card_body = dom_request_card.find('div.card-body').last()
    
    # Request Description
    if 'description' in i: dom_request_card_body.append("<p class='card-text lead'>"+i['description']+"</p>")
    else: raise Exception('Missing request description')
    # Request URL
    if 'method' in i:
        dom_request_card_body.append("<h5>URL:</h5> <p><code><b>"+i['method']+"</b> "+api_host+i['url']+"</code></p>")
    else: raise Exception('Missing request method')

    # Request Parameters
    dom_request_card_body.append("<h5>Parameters</h5>")
    dom_request_card_body.append("<div class='table-responsive-sm parameters'><table class='table table-striped table-bordered parameters'></table></div>")
    dom_parameter_table = dom_container.find('div.parameters').last().find('table.parameters').last()
    dom_parameter_table.append("<thead class='thead-dark'><tr><th>Name</th><th>Type</th><th>Optional</th><th>Description</th></tr></thead>")
    dom_parameter_table.append("<tbody></tbody>")
    dom_parameter_tbody = dom_parameter_table.find('tbody')
    if 'parameters' in i:
        for j in i['parameters']:
            dom_parameter_tbody.append("<tr></tr>")
            dom_parameter_tr = dom_parameter_tbody.find('tr').last()
            # Parameter Name
            if 'name' in j: dom_parameter_tr.append("<td>"+j['name']+"</td>")
            else: raise Exception('Missing parameter name')
            # Parameter Type
            if 'type' in j: dom_parameter_tr.append("<td>"+j['type']+"</td>")
            else: raise Exception('Missing parameter type')
            # Parameter Optional
            if 'optional' in j: dom_parameter_tr.append("<td>"+str(j['optional'])+"</td>")
            else: raise Exception('Missing parameter optional')
            # Parameter Description
            if 'description' in j: dom_parameter_tr.append("<td>"+j['description']+"</td>")
            else: raise Exception('Missing parameter description')

    # Request Examples
    if 'examples' in i:
        dom_request_card_body.append("<h5>Examples:</h5>")
        for j in i['examples']:
            # Example Description
            if 'description' in j:
                dom_request_card_body.append("<p>"+j['description']+"</p>")
            else: raise Exception('Missing example description')
            
            dom_request_card_body.append("<table style='font-family: monospace' class='table table-sm table-borderless table-dark example'></table>")
            dom_example_table = dom_container.find('table.example').last()
            if 'type' in j:
                if j['type'] == 'request':
                    # Example Method and Protocol for Request
                    if 'method' in j and 'protocol' in j:
                        dom_example_table.append("<tr><td>"+j['method']+" <b>"+i['url']+"</b> "+j['protocol']+"</td></tr>")
                    elif 'method' in j:
                        dom_example_table.append("<tr><td>"+j['method']+" <b>"+i['url']+"</b></td></tr>")
                    else: raise Exception('Missing example method')
                elif j['type'] == 'response':
                    # Example Method, Protocol and Status for Response
                    if 'protocol' in j and 'status' in j:
                        dom_example_table.append("<tr><td>"+j['protocol']+" "+j['status']+"</td></tr>")
                    elif 'status' in j:
                        dom_example_table.append("<tr><td>"+j['status']+"</td></tr>")
                    else: raise Exception('Missing example status '+i['title'])
                else: raise Exception('Invalid response type of example, must be "request" or "response"')
            else: raise Exception('Missing example type')
            
            # Example Headers
            if 'headers' in j:
                for k in j['headers']:
                    # Header Key and Value
                    dom_example_table.append("<tr><td>"+k['key']+": "+k['value']+"</td></tr>")
            
            # Example Body
            if 'body' in j:
                if type(j['body']) is str:
                    dom_example_table.append("<tr><td><code style='display:block; white-space: pre-line;'>"+j['body']+"</code></td></tr>")
                elif type(j['body']) is list:
                    body = ''
                    for i in j['body']:
                        body += i + '\n'
                    body = body[:-1]
                    dom_example_table.append("<tr><td><code style='display:block; white-space: pre-line;'>"+body+"</code></td></tr>")

# Footer
dom_body.append('''<footer><div class="container py-5">
            <p class="mb-0 text-uppercase font-weight-bold small text-justify"><a href="https://github.com/ivan-avalos/api-documenter" class="text-muted float-right" rel="noopener">Documentation generated with api-documenter</a></p></footer>''')

# Print DOM and write it to output file
#print(html_apidoc.find('html').html())
output_file.write(html_apidoc.find('html').html())
