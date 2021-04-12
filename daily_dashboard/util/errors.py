from flask import jsonify, render_template


class BaseApplicationException(Exception):
    template_path = 'error.html'

    def __init__(self, status=500, title='Unnamed Error', message=None):
        self.status = status
        self.title = title
        self.message = message

    def as_json(self):
        return jsonify({
            'error': self.title,
            'message': self.message or ''
        }), self.status

    def as_template(self):
        return render_template(self.template_path, self)
