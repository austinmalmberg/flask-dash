import os
from datetime import timedelta

from flask import session

from wtforms import Form
from wtforms.csrf.session import SessionCSRF


class CSRF_Form(Form):
    class Meta:
        csrf = True  # Enable CSRF
        csrf_class = SessionCSRF
        csrf_secret = bytearray(os.environ['csrf_secret'], 'utf-8')
        csrf_time_limit = timedelta(minutes=20)

        @property
        def csrf_context(self):
            return session
