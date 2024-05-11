from http.server import BaseHTTPRequestHandler, HTTPServer
import json

from views import get_all_comments, get_comment_by_id, delete_comment,update_comment, create_comment

from views import *

from views.user_request import create_user, get_all_users, get_single_user, login_user, update_user
from urllib.parse import urlparse, parse_qs

class HandleRequests(BaseHTTPRequestHandler):
    """Handles the requests to this server"""

    def parse_url(self, path):
        """Parse the url into the resource and id"""
        parsed_url = urlparse(path)
        path_params = parsed_url.path.split('/')
        resource = path_params[1]
        if '?' in resource:
            param = resource.split('?')[1]
            resource = resource.split('?')[0]
            pair = param.split('=')
            key = pair[0]
            value = pair[1]
            return (resource, key, value)
        else:
            id = None
            try:
                id = int(path_params[2])
            except (IndexError, ValueError):
                pass
            return (resource, id)

    def _set_headers(self, status):
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response

        Args:
            status (number): the status code to return to the front end
        """
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_OPTIONS(self):
        """Sets the OPTIONS headers
        """
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods',
                         'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers',
                         'X-Requested-With, Content-Type, Accept')
        self.end_headers()

    def do_GET(self):
        self._set_headers(200)
        response = {}
        parsed = self.parse_url(self.path)

        if '?' not in self.path:
            (resource, id) = parsed

            if resource == "posts":
                if id is not None:
                    response = get_single_post(id)
                else:
                    response = get_all_posts()
                            
            elif resource == "comments":
                if id is not None:
                    response = get_comment_by_id(id)
                else:
                    response = get_all_comments()
            
            elif resource == "users":
                if id is not None:
                    response = get_single_user(id)
                else:
                    response = get_all_users()

        self.wfile.write(json.dumps(response).encode())


    def do_POST(self):
        self._set_headers(201)
        content_len = int(self.headers.get('content-length', 0))
        post_body = json.loads(self.rfile.read(content_len))
        response = ''
        resource, _ = self.parse_url(self.path)

        if resource == 'login':
            response = login_user(post_body)
        if resource == 'register':
            response = create_user(post_body)

        new_item = None

        if resource == "posts":
            new_item = create_post(post_body)

        if resource == 'comments':
            new_item = create_comment(post_body)

        self.wfile.write(json.dumps(new_item).encode())

        return response

    def do_PUT(self):
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        success = False

        
        if resource == "comments":
            success = update_comment(id, post_body)
            
        elif resource == 'posts':
            success = update_post(id, post_body)
        
        elif resource == 'users':
            success = update_user(id, post_body)
        

        if success:
            self.send_response(204)
        else:
            self.send_response(404)

        self.end_headers()
        self.wfile.write("".encode())



    def do_DELETE(self):
        self.send_response(204)
        self.end_headers()
        (resource, id) = self.parse_url(self.path)
        
        if resource == "comments":
            delete_comment(id)
        
        if resource == "posts":
            delete_post(id)
        
        self.wfile.write("".encode())



 

def main():
    """Starts the server on port 8088 using the HandleRequests class
    """
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
