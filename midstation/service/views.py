# -*- coding: utf-8 -*-
__author__ = 'qitian'

from flask import Blueprint, redirect, request, url_for, render_template, abort, flash
from flask_login import login_required, current_user
from jinja2 import TemplateNotFound
from midstation.user.models import User, Service
from midstation.service.forms import ServiceProfileForm


service = Blueprint('service', __name__, template_folder='templates')

# services list
@service.route('/service_list')
@login_required
def service_list():
    try:
        services = current_user.services
        # user = User.get_user_by_id(1)
        # services = user.services
        return render_template('service/service_list.html', services=services)
    except TemplateNotFound:
        abort(404)


# service info
@service.route('/service_profile/<service_id>', methods=['GET', 'POST'])
@login_required
def service_profile(service_id):
    form = ServiceProfileForm(request.form)

    serv = Service.query.filter_by(id=service_id).first()
    if serv is None:
        serv = Service()
    if request.method == 'POST' and form.validate_on_submit():
        form.save_form(serv)
        flash(u'保存成功', category='success')
        return redirect(url_for('service.service_list'))

    services = current_user.services
    return render_template('service/service_profile.html',form=form, service=serv, services=services)
