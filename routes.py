from flask import render_template, url_for, redirect, request
from Fkj import app, database, bcrypt
from flask_login import login_required, login_user, logout_user, current_user
from Fkj.forms import Formlogin, FormCriarConta, FormFoto
from Fkj.models import Usuario, Foto
import os
from werkzeug.utils import secure_filename
#import io

@app.route("/", methods=["GET", "POST"])
def homepage():
    form_login = Formlogin()
    if form_login.validate_on_submit():
        usuario = Usuario.query.filter_by(email = form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            login_user(usuario)
            return redirect(url_for("perfil", id_usuario=usuario.id))

    return render_template("homepage.html", form=form_login)

@app.route("/criarconta", methods=["GET", "POST"])
def criarconta():
    form_criarconta = FormCriarConta()
    if form_criarconta.validate_on_submit():
        senha=bcrypt.generate_password_hash(form_criarconta.senha.data)
        #bcrypt.check_password_hash(form_criarconta.senha.data)
        usuario=Usuario(username=form_criarconta.username.data, email=form_criarconta.email.data, senha=senha)
        database.session.add(usuario)
        database.session.commit()
        login_user(usuario, remember=True)
        return redirect(url_for("perfil", id_usuario=usuario.id))
    return render_template("criarconta.html", form=form_criarconta)

@app.route("/perfil/<id_usuario>", methods=["GET", "POST"])
@login_required
def perfil(id_usuario):
    if int(id_usuario) == int(current_user.id):
       # O usuário está vendo o perfil dele
       form_foto = FormFoto()
       if form_foto.validate_on_submit():
           arquivo = form_foto.foto.data
           #filename=request.form['foto']
           nome_seguro = secure_filename(arquivo.filename)
           #print(type(nome_seguro))
           #print("Arquivo", arquivo)
           #print(nome_seguro)
           #salvar o arquivo na pasta file_post
           caminho = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                           app.config["UPLOAD_FOLDER"], nome_seguro)
           print(caminho)
           arquivo.save(caminho)
           #Registrar este arquivo no banco de dados
           foto = Foto(imagem=nome_seguro, id_usuario=current_user.id)
           database.session.add(foto)
           database.session.commit()
       return render_template("perfil.html", usuario=current_user, form=form_foto)
    else:
        usuario=Usuario.query.get(int(id_usuario))
        return render_template("perfil.html", usuario=usuario, form=None)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("homepage"))

@app.route("/feed")
@login_required
def feed():
    fotos = Foto.query.order_by(Foto.data_criacao.desc()).all()[:10]
    return render_template("feed.html", fotos=fotos)