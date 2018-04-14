#!flask/bin/python
# encode: utf8
import uuid
from flask import Flask, request, Response, g
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
app.debug = True
auth = HTTPBasicAuth()

users = {}

@app.after_request
def after_request(res):
    res.headers.add('Access-Control-Allow-Origin', '*')
    res.headers.add('Access-Control-Allow-Headers', 'Content-Type, X-Token')
    res.headers.add('Access-Control-Allow-Methods', 'GET, POST')
    return res

@auth.get_password
def get_pwd(username) :
    if username in users :
        return users.get(username)
    return None

@auth.hash_password
def hash_pwd(password) :
    return md5(password).hexdigest()

@app.route('/api/token', methods = ['POST'])
def give_token() :
    if request.headers['content-type'] == 'application/json' :
        if not request.is_json :
            res = Response()
            res.status_code = 400
            return res
        else :
            data = request.get_json()
            if 'email' not in data.keys() : 
                res = Response(response = "Error : Bad request body !", content_type = 'text/plain')
                res.status_code = 400
                return res
            elif data['email'] in users :
                res = Response(response = "Error : The user <" + data['email'] + "> has already got a token !", content_type = 'text/plain')
                res.status_code = 400
                return res
            else :
                g.uuid = uuid.uuid1().hex
                users[data['email']] = g.uuid
                print(users)
                res = Response(response = "Your tokent is : " + g.uuid, content_type = 'text/plain')
                res.status_code = 200
                return res
    else :
        res = Response(response = 'Error : Bad content-type', content_type = 'text/plain')
        res.status_code = 415
        return res

def textJustification(words, lineLength) :
    line, index = [], 0
    for word in words :
        if line and index + len(word) > lineLength :
            if len(line) == 1 :
                yield ' '.join(line).ljust(lineLength)
            else :
                q, r = divmod(lineLength - index + 1, len(line) - 1)
                spaces = ' ' * (q + 1)
                if r == 0 : 
                    yield spaces.join(line)
                else :
                    additionnalSpaces = ' ' * (q + 2)
                    yield additionnalSpaces.join(line[:r] + [spaces.join(line[r:])])
            line, index = [], 0
        line.append(word)
        index += len(word) + 1
    if line :
        yield ' '.join(line).ljust(lineLength)

@app.route('/api/justify', methods = ['POST'])
def getJustifiedText() :
    if request.headers['content-type'] == 'text/plain' :
        result = []
        data = request.get_data(as_text = True)
        paragraphs = data.split('\n')
        for paragraph in paragraphs :
            print(type(paragraph))
            if paragraph == '\n' :
                result += '\n'
                continue
            result += textJustification(paragraph.split('\n')[0].split(), 80)
        result = '\n'.join(result)
    
        res = Response(response = result, content_type = 'text/plain')
        res.status_code = 200
        return res
    else :
        res = Response(response = 'Error : Bad content-type', content_type = 'text/plain')
        res.status_code = 415
        return res

@app.route('/')
def index() :
    return 'hello world !'

@app.errorhandler(404)
def not_found(error):
    res = Response(response = 'Error : Request not found !', content_type = 'text/plain')
    res.status_code = 404
    return res


if __name__ == '__main__' :
    app.run()
