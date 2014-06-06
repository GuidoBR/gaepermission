# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaecookie.decorator import no_csrf
from gaepermission import facade
from gaepermission.decorator import login_not_required
from tekton import router
from web.login import pending


@login_not_required
def index(_handler, _resp, _write_tmpl, token):
    cmd = facade.login_facebook(token, _resp)
    cmd.execute()
    if cmd.pending_link:
        pending_path = router.to_path(pending.index, cmd.pending_link.key.id())
        user_email = cmd.main_user_from_email.email
        facade.send_passwordless_login_link(user_email,
                                            'https://gaepermission.appspot.com' + pending_path).execute()
        _write_tmpl('login/pending.html', {'provider': 'Facebook', 'email': user_email})
        return
    _handler.redirect('/')


@no_csrf
def form(_write_tmpl):
    app = facade.get_facebook_app_data().execute().result
    dct = {'save_app_path': router.to_path(save), 'app': app}
    _write_tmpl('login/facebook_form.html', dct)


def save(_handler, app_id, token):
    facade.save_or_update_facebook_app_data(app_id, token).execute()
    _handler.redirect('/')