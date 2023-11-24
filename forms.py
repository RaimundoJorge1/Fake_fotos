from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from Fkj.models import Usuario

class Formlogin(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    senha =PasswordField("Senha", validators=[DataRequired()])
    botao_confirmacao = SubmitField("Fazer login")
    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if not usuario:
            raise ValueError("Usuário inexistente, crie uma conta para continuar")

class FormCriarConta(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    username = StringField("Nome do Usuário", validators=[DataRequired()])
    senha = PasswordField("Senha", validators=[DataRequired(), Length(6,20)])
    confirmacao_senha = PasswordField("Confirmar Senha", validators=[DataRequired(), EqualTo("senha")])
    botao_confirmacao =SubmitField("Criar Conta")

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValueError("Email já foi cadastrado")

class FormFoto(FlaskForm):
    foto = FileField("Foto", validators=[DataRequired()])
    botao_confirmacao = SubmitField("Enviar")
