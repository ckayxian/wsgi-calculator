"""
For your homework this week, you'll be creating a wsgi application of
your own.

You'll create an online calculator that can perform several operations.

You'll need to support:

  * Addition
  * Subtractions
  * Multiplication
  * Division

Your users should be able to send appropriate requests and get back
proper responses. For example, if I open a browser to your wsgi
application at `http://localhost:8080/multiple/3/5' then the response
body in my browser should be `15`.

Consider the following URL/Response body pairs as tests:

```
  http://localhost:8080/multiply/3/5   => 15
  http://localhost:8080/add/23/42      => 65
  http://localhost:8080/subtract/23/42 => -19
  http://localhost:8080/divide/22/11   => 2
  http://localhost:8080/               => <html>Here's how to use this page...</html>
```

To submit your homework:

  * Fork this repository (Session03).
  * Edit this file to meet the homework requirements.
  * Your script should be runnable using `$ python calculator.py`
  * When the script is running, I should be able to view your
    application in my browser.
  * I should also be able to see a home page (http://localhost:8080/)
    that explains how to perform calculations.
  * Commit and push your changes to your fork.
  * Submit a link to your Session03 fork repository!


"""
import traceback


def home_page():
    body = """<html>
    <head>
    <tite><h1>Welcome to the WSGI-Calculator</h1></title>
    </head>
    <body>
    <p>This calculator supports the following operations:</p>
    <p style="text-indent: 25px; font-family:'Courier'">Add</p>
    <p style="text-indent: 25px; font-family:'Courier'">Subtract</p>
    <p style="text-indent: 25px; font-family:'Courier'">Multiply</p>
    <p style="text-indent: 25px; font-family:'Courier'">Divide</p>
    <p>Each operation can be used by navigating to that location from this home page. The operations for each operation must be supplied as additional fields in the uri.</p>
    <p>For example: </p>
    <p style="text-indent: 25px; font-family:'Courier'">[this page]/multiply/3/5   => 15</p>
    <p style="text-indent: 25px; font-family:'Courier'">[this page]/add/23/42      => 65</p>
    <p style="text-indent: 25px; font-family:'Courier'">[this page]/subtract/23/42 => -19</p>
    <p style="text-indent: 25px; font-family:'Courier'">[this page]/divide/22/11   => 2</p>
    </body>
    </html>"""

    return body

def add(*args):
    """ Returns a STRING with the sum of the arguments """

    num_1, num_2 = [*args]
    try:
        sum = int(num_1) + int(num_2)
        sum = str(sum)
    except ValueError:
        raise NameError

    return sum

def subtract(*args):
    """ Return a string with the difference of the arguments """
    num_1, num_2 = [*args]
    try:
        difference = int(num_1) - int(num_2)
        difference = str(difference)
    except ValueError:
        raise NameError

    return difference

def multiply(*args):
    """ Return a string with the product of the arguments """
    num_1, num_2 = [*args]
    try:
        product = int(num_1) * int(num_2)
        product = str(product)
    except ValueError:
        raise NameError

    return product

def divide(*args):
    """ Return a string with the quotitent of the arguments """
    num_1, num_2 = [*args]
    try:
        quotient = int(num_1) / int(num_2)
        quotient = str(quotient)
    except ValueError:
        raise NameError
    except ZeroDivisionError:
        quotient = "Division by zero"

    return quotient

def resolve_path(path):
    """
    Should return two values: a callable and an iterable of
    arguments.
    """

    # TODO: Provide correct values for func and args. The
    # examples provide the correct *syntax*, but you should
    # determine the actual values of func and args using the
    # path.
    funcs = {
        '': home_page,
        'add': add,
        'subtract': subtract,
        'multiply': multiply,
        'divide': divide,
    }
    path = path.strip('/').split('/')

    func_name = path[0]
    args = path[1:]

    if func_name in funcs:
        func = funcs[func_name]
    else:
        raise NameError

    return func, args

def application(environ, start_response):
    headers = [('Content-type', 'text/html')]
    try:
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError
        func, args = resolve_path(path)
        body = func(*args)
        status = "200 OK"
    except NameError:
        status = "404 Not Found"
        body = "<h1>Not Found</h1>"
    except Exception:
        status = "500 Internal Server Error"
        body = "<h1>Internal Server Error</h1>"
        print(traceback.format_exc())
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf-8')]

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    server = make_server('localhost', 8080, application)
    server.serve_forever()
