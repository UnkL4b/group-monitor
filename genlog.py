#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime

__author__ = "Danilo Vaz"
__copyright__ = "Copyright 2016, UnkL4b"
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Danilo Vaz"
__email__ = "danilovazb@gmail.com"


class GenLog(object):

    def __init__(self,):
        self.data = datetime.datetime.now().date()
        self.datahora = datetime.datetime.now()
        self.nome_arquivo = 'logs/log-{}.txt'.format(self.data)

    def gravarLog(self, erro):
        with open(self.nome_arquivo, 'a') as arquivo:
            if '\'message\'' in str(erro):
                arquivo.write(
                    "[*]LOG - %s: POST APENAS COM IMAGEM\n" % self.datahora)
            else:
                arquivo.write(
                    "[*]LOG - %s: %s\n" % (self.datahora, str(erro)))
        arquivo.close()
