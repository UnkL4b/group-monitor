#!/usr/bin/python
# -*- coding: utf-8 -*-
import sqlite3
import json
from os.path import isfile, getsize

__author__ = "Danilo Vaz"
__copyright__ = "Copyright 2016, UnkL4b"
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Danilo Vaz"
__email__ = "danilovazb@gmail.com"


class BancoDados(object):

    def __init__(self,):
        with open('configs/db.json', 'r') as json_config:
            config = json.load(json_config)
        self.db_name = config['database'] + ".db"
        if '/' != config['path'][-1:]:
            self.db_path = config['path'] + "/"
        else:
            self.db_path = config['path']
        if not isfile(self.db_path + self.db_name):
            self.db_create()

    def conecta(self,):
        self.conn = sqlite3.connect(self.db_path + self.db_name)
        return self.conn.cursor()

    """
    db_create:
        - Adicionar um create table para cada modulo que desenvolver.
    """
    def db_create(self,):
        conn = sqlite3.connect(self.db_path + self.db_name)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS posts_facebook (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    created_time TEXT NOT NULL,
                    message TEXT NOT NULL,
                    post_id TEXT NOT NULL,
                    nome_comunidade TEXT NOT NULL
            );""")
        conn.close()

    def db_insert(self, query):
        cursor = self.conecta()
        cursor.execute(query)
        self.conn.commit()
        self.conn.close()

    def db_consult(self, query):
        cursor = self.conecta()
        cursor.execute(query)
        return cursor
        self.conn.close()

    """
    Ainda não implementado
    def db_delete(self, query):
    """
