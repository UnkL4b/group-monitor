#!/usr/bin/python
# -*- coding: utf-8 -*-
import banco
import datetime

__author__ = "Danilo Vaz"
__copyright__ = "Copyright 2016, UnkL4b"
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Danilo Vaz"
__email__ = "danilovazb@gmail.com"


class Relat(object):

    def generate(self):
        rows = banco.BancoDados().db_consult('select * from posts_facebook order by id desc;')
        relatorio = open('index.html','w')
        head = """
        <!DOCTYPE html>
        <html>
            <head>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <meta name="description" content="FaceMonitor">
                <meta name="author" content="Danilo Vaz">
                <meta http-equiv="refresh" content="1800">

                <!-- App Favicon -->
                <link rel="shortcut icon" href="assets/images/favicon.ico">

                <!-- App title -->
                <title>FaceMonitor</title>

                <!-- Switchery css -->
                <link href="assets/plugins/switchery/switchery.min.css" rel="stylesheet" />

                <!-- App CSS -->
                <link href="assets/css/style.css" rel="stylesheet" type="text/css" />


                <!-- HTML5 Shiv and Respond.js IE8 support of HTML5 elements and media queries -->
                <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
                <!--[if lt IE 9]>
                <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
                <script src="https://oss.maxcdn.com/libs/respond.js/1.3.0/respond.min.js"></script>
                <![endif]-->
                <!-- Modernizr js -->

            </head>


            <body>

                <!-- Navigation Bar-->
                <!-- End Navigation Bar-->



                <!-- ============================================================== -->
                <!-- Start right Content here -->
                <!-- ============================================================== -->
                <div>
                    <div class="container">

                        <!-- Page-Title -->
                        <div class="row">
                            <div class="col-sm-6">
                                <h4 class="page-title">Relatório</h4>
                            </div>
                            <div class="col-sm-6">
                                <h4 class="page-title">Ultima Atualização: {}</h4>
                            </div>
                        </div>


                        <div class="row">
                            <div class="col-xs-12">
                                <div class="card-box">

                                  <div class="p-20">
                                              <table class="table table-hover">
                                                  <thead>
                                                  <tr>
                                                      <th>#</th>
                                                      <th>Nome</th>
                                                      <th>Data</th>
                                                      <th>Mensagem</th>
                                                      <th>ID</th>
                                                  </tr>
                                                  </thead>
                                                  <tbody>
        """.format(datetime.datetime.today())
        relatorio.write(head)
        relatorio.close()
        relatorio = open('index.html', 'a')
        for linha in rows:
            relatorio.write("""
<tr>
    <th scope='row'>{}</th>
    <td>{}</td>
    <td>{}</td>
    <td>{}</td>
    <td>{}</td>
</tr>
    """.format(linha[0],
               linha[1].encode("utf-8"),
               linha[2].encode("utf-8"),
               linha[3].encode("utf-8"),
               linha[4].encode("utf-8")))


        relatorio.write("""</tbody>
            </table>
            </div>

            </div>
            </div><!-- end col-->

            </div>
            <!-- end row -->



<!-- Footer -->
<footer class="footer text-right">
<div class="container">
<div class="row">
<div class="col-xs-12">
2016 © Uplon.
</div>
</div>
</div>
</footer>
<!-- End Footer -->


</div> <!-- container -->


</div> <!-- End wrapper -->




<script>
var resizefunc = [];
</script>

<!-- jQuery  -->
<script src="assets/js/jquery.min.js"></script>
<script src="assets/js/tether.min.js"></script><!-- Tether for Bootstrap -->
<script src="assets/js/bootstrap.min.js"></script>
<script src="assets/js/waves.js"></script>
<script src="assets/js/jquery.nicescroll.js"></script>
<script src="assets/plugins/switchery/switchery.min.js"></script>

<!-- Chart JS -->
<script src="assets/plugins/chart.js/chart.min.js"></script>
<script src="assets/pages/chartjs.init.js"></script>

<!-- App js -->
<script src="assets/js/jquery.core.js"></script>
<script src="assets/js/jquery.app.js"></script>

</body>
</html>""")

        relatorio.close()
