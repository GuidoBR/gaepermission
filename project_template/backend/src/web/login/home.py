# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.api import users
from config.tmpl_middleware import TemplateResponse
from gaecookie.decorator import no_csrf
from gaepermission import facade
from gaepermission.decorator import login_not_required
from tekton import router
from web.login import google, facebook
from web.login.passwordless import send_email


@login_not_required
@no_csrf
def index(ret_path='/'):
    g_path = router.to_path(google.index, ret_path=ret_path)
    dct = {'login_google_path': users.create_login_url(g_path),
           'login_passwordless_path': router.to_path(send_email, ret_path=ret_path),
           'login_facebook_path': router.to_path(facebook.index, ret_path=ret_path),
           'faceapp': facade.get_facebook_app_data().execute().result}
    return TemplateResponse(dct)