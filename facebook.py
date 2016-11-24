#!/usr/bin/python
# -*- coding: utf-8 -*-
from selenium.webdriver.common.keys import Keys
#from pyvirtualdisplay import Display
from selenium import webdriver
from facepy import GraphAPI
from genlog import GenLog
import datetime
import argparse
import time
import os
import json
import banco as db
import relat

#try:
#    display = Display(visible=0, size=(800, 600))
#    display.start()
#except OSError as erro:
#    GenLog().gravarLog(erro)
#    print("""
#        [-] Instalar xvfb
#            Debian: apt-get install xvfb
#        """)

"""
=== MELHORIAS ===
- insert em blocos
- consulta em blocas
"""

__title__ = "Facebook Group Monitor"
__author__ = "Danilo Vaz"
__copyright__ = "Copyright 2016, UnkL4b"
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Danilo Vaz"
__email__ = "danilovazb@gmail.com"
__status__ = "Beta"


class FaceGroupMonitor(object):

    os.system('cls' if os.name == 'nt' else 'clear')
    print("""
               .-. \_/ .-.
               \.-\/=\/.-/
            '-./___|=|___\.-'    Facebook Group Monitor v1.0
           .--| \|/`"`\|/ |--.
          (((_)\  .---.  /(_)))
           `\ \_`-.   .-'_/ /`_
             '.__       __.'(_))
                 /     \     //
                |       |__.'/
                \       /--'`
            .--,-' .--. '----.
           '----`--'  '--`----'
    """)

    def __init__(self,):
        parser = argparse.ArgumentParser("""Facebook group monitor v1.0\n\n""")
        parser.add_argument(
           '-u',
           '--user',
           metavar='seu@e-mail.com',
           help='Seu e-mail do facebook'
           )
        parser.add_argument(
            '-p',
            '--password',
            metavar='suasenha',
            help='Sua senha do facebook')
        parser.add_argument(
            '-i',
            '--id',
            metavar='1624234151177377',
            help='ID do grupo no facebook')
        parser.add_argument(
            '-f',
            '--filter',
            metavar='geradas,lara,cc',
            help='Filtro de conteúdo')
        args = parser.parse_args()

        if args.user is None and args.password is None:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    parser.print_help()
                    exit()

        self.user_mail = args.user
        self.user_pass = args.password
        self.filter = args.filter
        self.inicio = 1
        self.data_token = 0
        self.timestamp1 = ""
        self.timestamp2 = ""
        self.bancodados = db.BancoDados()
        self.nome_comunidade = ""

    def espera(self, tempo):
        time.sleep(tempo)

    def browser(self,):
        driver = webdriver.PhantomJS()
        return driver

    def tokenGenerator(self,):
        print("[+] Etapa 0/6")
        gen_browser = self.browser()
        gen_browser.get('https://www.facebook.com/login/?next=https%3A%2F%2Fdevelopers.facebook.com%2Ftools%2Fexplorer')
        set_email = gen_browser.find_element_by_id('email')
        set_email.send_keys(self.user_mail)
        set_senha = gen_browser.find_element_by_id('pass')
        set_senha.send_keys(self.user_pass)
        set_senha.send_keys(Keys.RETURN)
        self.espera(10)
        get_token = gen_browser.find_elements_by_class_name('_55pe')
        get_token[1].click()
        print("[+] Etapa 1/6 concluída!")
        self.espera(5)
        get_useracc = gen_browser.find_element_by_class_name('_2nax')
        get_useracc.click()
        print("[+] Etapa 2/6 concluída!")
        self.espera(3)
        get_versao = gen_browser.find_elements_by_class_name('_55pe')
        get_versao[len(get_versao)-1].click()
        print("[+] Etapa 3/6 concluída!")
        self.espera(3)
        set_versao = gen_browser.find_element_by_link_text('v2.3')
        set_versao.click()
        print("[+] Etapa 4/6 concluída!")
        self.espera(2)
        set_user_group = gen_browser.find_element_by_name('user_groups')
        set_user_group.click()
        gen_token = gen_browser.find_elements_by_class_name('_4jy0')
        gen_token[len(gen_token)-3].click()
        print("[+] Etapa 5/6 concluída!")
        self.espera(2)
        token = gen_browser.find_elements_by_class_name('_58al')
        access_token = token[1].get_attribute('value')
        self.timestamp1 = datetime.datetime.now()
        gen_browser.close()
        print("[+] Etapa 6/6 concluída!")
        print("\n[+] Consultando grupos...")
        print("\n[+] Token: %s" % access_token)
        return access_token

    def verify(self, post_id):
        q_insert = """
            SELECT EXISTS ( SELECT post_id from posts_facebook
            WHERE post_id like "{}" );
            """.format(post_id)
        result = self.bancodados.db_consult(q_insert)
        for linha in result.fetchall():
            if linha[0] == 1:
                return True
            else:
                return False

    def parser(self, resultado):
        if 'feed' in resultado:
            data = resultado['feed']['data']
            self.nome_comunidade = resultado['name']
            self.nome_comunidade = self.nome_comunidade.encode('utf-8')
            for i in range(len(data)):
                self.consulta(data[i]['id'])
        else:
            try:
                nome = resultado['from']['name'].encode('utf-8')
                data_create = resultado['created_time']
                msg = resultado['message'].encode('utf-8')
                post_id = resultado['id']
                if self.filter is None:
                    if self.verify(post_id) is True:
                        pass
                    else:
                        q_insert = """
                            INSERT INTO posts_facebook
                            (nome,
                            created_time,
                            message,
                            post_id,
                            nome_comunidade)
                            VALUES ("{}","{}","{}","{}","{}");
                            """.format(
                                nome,
                                data_create,
                                msg,
                                post_id,
                                self.nome_comunidade
                            )
                        self.bancodados.db_insert(q_insert)
#                        """ ===== DEBUG =====
                        print(
                            "Nome:{}\nData:{}\nMsg:{}\n".format(
                                nome, data_create, msg)
                        )
 #                       """
                else:
                    if self.verify(post_id) is True:
                        pass
                    else:
                        filtro = self.filter.split(',')
                        for i in range(len(filtro)):
                            if filtro[i].upper().strip() in msg.upper():
                                q_insert = """
                                    INSERT INTO posts_facebook
                                    (nome,
                                    created_time,
                                    message,
                                    post_id,
                                    nome_comunidade)
                                    VALUES ("{}","{}","{}","{}","{}");
                                    """.format(
                                        nome,
                                        data_create,
                                        msg,
                                        post_id,
                                        self.nome_comunidade
                                    )
                                self.bancodados.db_insert(q_insert)
                                #""" ===== DEBUG =====
                                print(
                                    "Nome:{}\nData:{}\nMsg:{}\n".format(
                                        nome,
                                        data_create,
                                        msg.replace(
                                            filtro[i].upper(),
                                            '\033[1;91m{}\033[0m'.format(
                                                filtro[i].upper()
                                            )
                                        )
                                    )
                                )
                                #"""
            except Exception as erro:
                GenLog().gravarLog(erro)
                pass

    def consulta(self, query):
        if self.inicio == 1:
            print("[+] Gerando Token de acesso...")
            self.graph = GraphAPI(self.tokenGenerator())
            self.inicio = 0
        self.timestamp2 = datetime.datetime.now()
        verifica = self.timestamp2 - self.timestamp1
        if verifica.total_seconds() >= 1800:
            self.inicio = 1
        result = self.graph.get(query)
        self.parser(result)

    def main(self,):
        while True:
            with open('configs/config.json') as json_config:
                query = json.load(json_config)
            for i in range(len(query['facebook'])):
                search_string = query['facebook'][i]['id']
                search_string = search_string + '?fields=name,feed{application}'
                try:
                    self.consulta(search_string)
                except Exception as erro:
                    print(erro)
                    GenLog().gravarLog(erro)
                    pass
            relat.Relat().generate()        
            self.espera(7200)

if __name__ == "__main__":
    try:
        FaceGroupMonitor().main()
    except KeyboardInterrupt:
        print("\n[+] Exit")
