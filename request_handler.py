import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from posts import get_all_posts, get_post_by_id, get_posts_by_user, create_post, delete_post, update_post
from users import login_check, add_user, get_all_users
from categories import get_all_categories, get_single_category, create_category, delete_category, update_category
from comments import get_comments_by_post_id, create_comment, delete_comment

class HandleRequests(BaseHTTPRequestHandler):
    def _set_headers(self, status):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_GET(self):
        self._set_headers(200)

        response = {}

        parsed = self.parse_url(self.path)

        if len(parsed) == 2:
            (resource, id) = parsed

            if resource == "posts":
                if id is not None:
                    response = f"{get_post_by_id(id)}"
                else:
                    response = f"{get_all_posts()}"
            elif resource == "categories":
                if id is not None:
                    response = f"{get_single_category(id)}"
                else:
                    response = f"{get_all_categories()}"
            elif resource == "users":
                if id is not None:
                    response = f"{get_all_users()}"
                else:
                    response = f"{get_all_users()}"
        elif len(parsed) == 3:
            (resource, key, value) = parsed
            
            if key == "user_id" and resource == "posts":
                print("i made it")
                response = get_posts_by_user(value)
            elif key == "post_id" and resource == "comments":
                print("comments by post_id")
                response = get_comments_by_post_id(value)

        self.wfile.write(response.encode())

    def do_POST(self):
        self._set_headers(201)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        
        post_body = json.loads(post_body)
        
        (resource, _) = self.parse_url(self.path)

        response = None

        if resource == "login":
            returned_item = login_check(post_body)
            self.wfile.write(returned_item.encode())
        elif resource == "register":
            returned_item = add_user(post_body)
            self.wfile.write(returned_item.encode())
        elif resource == "posts":
            # new_post = None
            # new_post = create_post(post_body)
            # self.wfile.write(f"{new_post}".encode())
            response = create_post(post_body)
            self.wfile.write(f"{response}".encode())
        elif resource == "categories":
            new_category = None
            new_category = create_category(post_body)
            self.wfile.write(f"{new_category}".encode())
        elif resource == "comments":
            response = create_comment(post_body)
            self.wfile.write(f"{response}".encode())

    def do_DELETE(self):
        self._set_headers(204)

        (resource, id) = self.parse_url(self.path)

        if resource == 'posts':
                delete_post(id)
        elif resource == 'categories':
                delete_category(id)
        elif resource == "comments":
            delete_comment(id)

        self.wfile.write("".encode())

    def do_PUT(self):
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        (resource, id) = self.parse_url(self.path)
    
        success = False

        if resource == "posts":
            success = update_post(id, post_body)
        elif resource == "categories":
            success = update_category(id, post_body)
        if success:
            self._set_headers(204)
        else:
            self._set_headers(404)

        self.wfile.write("".encode())

        

    def parse_url(self, path):
        path_params = path.split("/")
        resource = path_params[1]

        if "?" in resource:
            param = resource.split("?")[1]
            resource = resource.split("?")[0]
            pair = param.split("=")
            key = pair[0]
            value = pair[1]

            return ( resource, key, value )

        else:
            id = None

            try:
                id = int(path_params[2])
            except IndexError:
                pass
            except ValueError:
                pass

            return (resource, id)   

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type')
        self.end_headers()
 

def main():
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()

if __name__ == "__main__":
    main()
