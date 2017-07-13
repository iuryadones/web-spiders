#-*- coding: utf-8 -*-

URL = {
    'recursos':'http://www.portaltransparencia.gov.br/PortalTransparenciaListaUFs.asp?Exercicio={}'.format
}

_TEXT = '//text()'
_HREF = '//@href'

BASE = {
    'estado': "//div[@id='listagem']/table//tr//td[1]",
    'municipio': "//div[@id='listagem']/table//tr//td[1]",
    'funcao': "//div[@id='listagem']/table//tr//td[1]",
    'acao_governamental': "//div[@id='listagem']/table//tr//td[2]",
    'linguagem_cidada': "//div[@id='listagem']/table//tr//td[3]",
    'total_no_ano': "//div[@id='listagem']/table//tr//td[4]",
}

XPATH = {
    'paginacao': "//div[@id='paginacao']/p[@class='paginaAtual']//text()",
    'estado_text': BASE['estado']+_TEXT,
    'estado_link': BASE['estado']+_HREF,
    'municipio_text': BASE['municipio']+_TEXT,
    'municipio_link': BASE['municipio']+_HREF,

    'funcao': BASE['funcao']+_TEXT,
    'acao_governamental': BASE['acao_governamental']+_TEXT,
    'linguagem_cidada': BASE['linguagem_cidada']+_TEXT,
    'total_no_ano': BASE['total_no_ano']+_TEXT,
}
