import datetime
import json

from firebase.firebase import FirebaseApplication, FirebaseAuthentication

DSN = 'https://transparenciaeducativa-1e9ca.firebaseio.com'

authentication = None
firebase = FirebaseApplication(DSN, authentication)

#firebase.get(
#    '/',
#    None,
#    params={'print': 'pretty'},
#    headers={'X_FANCY_HEADER': 'very fancy'})

arq = open('dados_2017.json')
ler = arq.read()

datas = json.loads(ler)

for data in datas:
    DB = {}
    _id = data.pop('_id')
    _id = _id['$oid']
    acoes = data.pop('acoes') 
    acoes_DB = {}
    for i, acao in enumerate(acoes):
        acoes_DB.update({i:acao})
    data['acoes'] = acoes_DB
    DB.update({_id: data})
    firebase.patch(
        '/portal-transparencia-2017/', 
        DB)

