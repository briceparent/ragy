# -*- coding: utf-8 -*-
import random
import re
import string

from bottle import Bottle, route, template, run, post, redirect, request

import settings

from db import DatabaseManager


app = Bottle()


class Message:
    _texts = dict(
        error_wrong_format="Le format du lien court <strong>{}</strong> n'est pas valide.",
        error_exists="Le lien court <strong>{}</strong> est déjà attribué à une autre url",
        error_404="Le page demandée n'existe pas !",
        success="Votre lien <strong>http://ra.gy/{}</strong> a été créé avec succès !"
    )
    _types = dict(
        error_wrong_format="danger",
        error_exists="danger",
        error_404="danger",
        success="success"
    )
    _icons = dict(
        error_wrong_format="",
        error_exists="",
        error_404="",
        success="http://chart.apis.google.com/chart?chs=80x80&cht=qr&chld=Q|0&chl=http://ra.gy/{}"
    )
    message = ""
    message_type = ""
    icon = ""

    def set_message(self, message_id, code):
        self.message_type = self._types[message_id]
        self.message = self._texts[message_id].format(code)
        self.icon = self._icons[message_id].format(code)

    def unset_message(self):
        self.message_type = ""
        self.message = ""
        self.icon = ""



displayed_message = Message()


def get_unique_id():
    db = DatabaseManager()
    while True:
        page_id = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(5))
        if not db.get_one(id=page_id):
            break

    return page_id


@route('/')
def show():
    context = {'message': displayed_message, 'next_id': get_unique_id()}
    ret = template('index', context)
    displayed_message.unset_message()
    return ret


@post("/generate")
def generate_ragy():
    db = DatabaseManager()

    link = request.forms.get('link')
    page_id = request.forms.get('id')
    creator = request.environ.get('REMOTE_ADDR')

    if not re.match('^[a-zA-Z0-9]{5,10}$', page_id):
        displayed_message.set_message("error_wrong_format", page_id)
    else:
        try:
            db.create_one(id=page_id, creator=creator, link=link)
        except db.IntegrityError:
            displayed_message.set_message("error_exists", page_id)
        else:
            displayed_message.set_message("success", page_id)

    redirect('/', 302)


@route('/:id')
def show(id):
    db = DatabaseManager()

    link = db.get_one(id=id)
    if link:
        db.add_access(id=id)
        return redirect(link['link'], 301)

    displayed_message.set_message("error_404", id)
    redirect('/', 302)


# Launching the server
run(host=settings.SERVER_URL, port=settings.SERVER_PORT)
