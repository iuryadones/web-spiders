import datetime
import json

from firebase.firebase import FirebaseApplication, FirebaseAuthentication

DSN = 'https://transparenciaeducativa-1e9ca.firebaseio.com'

authentication = None
firebase = FirebaseApplication(DSN, authentication)

estados = '/estados'

results = firebase.get(
    estados,
    None,
    params={'print': 'pretty'},
    headers={'X_FANCY_HEADER': 'very fancy'}
)

for result in results:
    print('Estado: {}'.format(result['estado']))
    for result_dict in result['municipios']:
        print('Municipio: {}'.format(result_dict['municipio']))
