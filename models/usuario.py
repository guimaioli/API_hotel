from sql_alchemy import banco
from flask import request, url_for
from requests import post
from key.keys import MAILGUN_API_KEY, MAILGUN_DOMAIN

DOMAIN_FOR_SEND_EMAIL = MAILGUN_DOMAIN 
KEY_FOR_SEND_EMAIL = MAILGUN_API_KEY

FROM_TITLE = 'NO-REPLY'
FROM_EMAIL = 'no-reply@maiao.com'

class UserModel(banco.Model):

	__tablename__ = 'usuarios'

	user_id = banco.Column(banco.Integer, primary_key=True)
	login = banco.Column(banco.String(40), nullable=False, unique=True)
	senha = banco.Column(banco.String(40), nullable=False)
	email = banco.Column(banco.String(80), nullable=False, unique=True)
	ativado = banco.Column(banco.Boolean, default=False)


	def __init__(self, login, senha, email, ativado):

		self.login = login
		self.senha = senha
		self.email = email
		self.ativado = ativado

	def send_confirmation_email(self):
		# http://127.0.0.1:5000/confirmacao/1
		link = request.url_root[:-1] + url_for('userconfirm', user_id=self.user_id)
				
		return post('https://api.mailgun.net/v3/{}/messages'.format(DOMAIN_FOR_SEND_EMAIL),
					auth=('api', KEY_FOR_SEND_EMAIL),
					data={  'from': '{} <{}>'.format(FROM_TITLE, FROM_EMAIL), 
							'to': self.email,
							'subject': 'Confirmação de Cadastro',
							'text': 'Confirme seu Cadastro clicando no link a seguir: {}'.format(link),
							'html': '<html><p>\
							Confirme seu Cadastro clicando no link a seguir: <a href="{}"> CONFIRMAR E-MAIL </a>\
							</p> </htm>'.format(link)
						 }
					)

	def json(self):
		return {
			'user_id': self.user_id,
			'login': self.login,
			'email': self.email,
			'ativado': self.ativado
			}

	@classmethod
	def find_user(cls, user_id):
		user = cls.query.filter_by(user_id=user_id).first() # select * from hoteis where hotelid
		if user:
			return user
		return None

	@classmethod
	def find_by_login(cls, login):
		user = cls.query.filter_by(login=login).first() 
		if user:
			return user
		return None

	@classmethod
	def find_by_email(cls, email):
		user = cls.query.filter_by(email=email).first() 
		if user:
			return user
		return None


	def save_user(self):
		banco.session.add(self)
		banco.session.commit()


	def delete_user(self):
		banco.session.delete(self)
		banco.session.commit()


