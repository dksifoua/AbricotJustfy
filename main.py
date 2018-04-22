#!flask/bin/python
# encode: utf8
import re
import uuid
from flask import Flask, request, Response, g
from flask_httpauth import HTTPBasicAuth
from text_justify import Justify

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

@app.route('/api/justify', methods = ['POST'])
def getJustifiedText() :
    if request.headers['content-type'] == 'text/plain' :
        data = request.get_data(as_text = True)
        print(type(data))
        J = Justify(data, 80)
        J.resolve()
        res = ""
        for e in J.text_justified :
            res += e + '\n'
        res = Response(response = res, content_type = 'text/plain')
        res.status_code = 200
        return res
    else :
        res = Response(response = 'Error : Bad content-type', content_type = 'text/plain')
        res.status_code = 415
        return res

@app.errorhandler(404)
def not_found(error):
    res = Response(response = 'Error : Request not found !', content_type = 'text/plain')
    res.status_code = 404
    return res


if __name__ == '__main__' :
    file = open('data.txt', 'r')
    data = ""
    line = file.readline()
    while len(line) != 0 :
        data += line
        line = file.readline()
    J = Justify(data, 80)
    J.resolve()
    excepted = ['Longtemps, je me suis couché de bonne heure. Parfois, à peine ma bougie éteinte,', 'mes  yeux  se  fermaient  si  vite  que  je n’avais pas le temps de me dire: «Je', 'm’endors.»  Et,  une  demi-heure  après, la pensée qu’il était temps de chercher', 'le  sommeil  m’éveillait;  je  voulais poser le volume que je croyais avoir dans', 'les  mains  et  souffler  ma  lumière;  je n’avais pas cessé en dormant de faire', 'des  réflexions  sur  ce  que  je  venais  de  lire, mais ces réflexions avaient', 'pris  un  tour  un  peu particulier; il me semblait que j’étais moi-même ce dont', 'parlait  l’ouvrage:  une  église,  un quatuor, la rivalité de François Ier et de', 'Charles-Quint.                                                                  ', 'Cette  croyance  survivait  pendant  quelques  secondes  à  mon  réveil; elle ne', 'choquait  pas  ma  raison,  mais  pesait  comme des écailles sur mes yeux et les', 'empêchait  de  se  rendre  compte que le bougeoir n’était plus allumé. Puis elle', 'commençait  à me devenir inintelligible, comme après la métempsycose les pensées', 'd’une  existence  antérieure;  le  sujet  du  livre se détachait de moi, j’étais', 'libre  de  m’y  appliquer  ou non; aussitôt je recouvrais la vue et j’étais bien', 'étonné de trouver autour de moi une obscurité, douce et reposante pour mes yeux,', 'mais  peut-être  plus  encore pour mon esprit, à qui elle apparaissait comme une', 'chose  sans  cause,  incompréhensible,  comme  une chose vraiment obscure. Je me', 'demandais  quelle  heure  il  pouvait être; j’entendais le sifflement des trains', 'qui,  plus ou moins éloigné, comme le chant d’un oiseau dans une forêt, relevant', 'les  distances,  me  décrivait  l’étendue  de la campagne déserte où le voyageur', 'se  hâte  vers la station prochaine; et le petit chemin qu’il suit va être gravé', 'dans  son souvenir par l’excitation qu’il doit à des lieux nouveaux, à des actes', 'inaccoutumés, à la causerie récente et aux adieux sous la lampe étrangère qui le', 'suivent encore dans le silence de la nuit, à la douceur prochaine du retour.']
    
    # Test
    assert J.text_justified == excepted, "Failure"

    app.run()
