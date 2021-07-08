

def make_app(environ, start_respone = None) :
    response_body = "\n".join(["{0} : {1}".format(k, environ[k]) for k in environ.keys()])
    status = "200"
    response_headers = [("Content-Type", "text/plain"),
                        ("Content-Length", str(len(response_body)))]

    if start_respone :
        start_respone(status, response_headers)

    return [response_body]




from wsgiref.simple_server import make_server

def start_response(status, respone_headers, exc_info=None) :

    print("Status : {}, respone_headers : {}".format(status, respone_headers))


from werkzeug.urls import url_decode

class MethodRewriteMiddleware(object) :
    """
        app = MethodRewriteMiddleware(app)
    """
    def __init__(self, app, input_name = "__method__") :
        self.app = app
        self.input_name = input_name

    
    def __call__(self, environ, start_response) :
        if self.input_name in environ.get("QUERY_STRING", "") :
            args = url_decode(environ["QUERY_STRING"])
            method = args.get(self.input_name)

            if method :
                method = method.encode("ascii", "replace")
                environ["REQUEST_METHOD"] = method
        
        return self.app(environ, start_response)


t = {"say" : "hello world!"}
app = make_app(t)
app = MethodRewriteMiddleware(app)
httpd = make_server('', 8000, app)
httpd.serve_forever()