# -*- coding: utf-8 -*-

def limpar_polos(polo):
    lista = [
        l.replace('\r', '').replace('\n', '').replace('\t', '')
        .replace('  ', '').strip() for l in polo]
    return list(
        filter(lambda x: False if x in ['', ' '] else True, lista))
