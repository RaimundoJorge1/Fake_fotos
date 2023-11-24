from Fkj import database, app
from Fkj.models import  Usuario, Foto
with app.app_context():
    database.create_all()
