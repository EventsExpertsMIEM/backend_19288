from flask import Blueprint, jsonify, request, make_response
from flask_login import (login_required, login_user, logout_user,
                         login_fresh, current_user)

import bcrypt

from . import *
from .. import auth, users_logic, events_logic

from ..exceptions import NotJsonError, NoData
from sqlalchemy.exc import IntegrityError


bp = Blueprint('users', __name__)


@bp.route('/register', methods=['POST'])
def register():
    try:
        if current_user.is_authenticated:
            return make_400('User is currently authenticated')
        else:
            args = request.get_json()
            if not args:
                return make_400('Expected json')

            pw = bcrypt.hashpw(str(args['password']).encode('utf-8'),
                               bcrypt.gensalt())
            users_logic.register_user(args['mail'], args['name'],
                                      args['surname'], pw.decode('utf-8'))
            return make_ok('User was registered')
    except KeyError as e:
        return make_400('KeyError - \n{}'.format(str(e)))
    except IntegrityError:
        return make_400('User with this login already exists')


@bp.route('/confirm', methods=['POST'])
def confirm():
    try:
        args = request.get_json()
        if not args:
            return make_400('Expected json')
        users_logic.confirm_user(args['link'])
        return make_ok('User was confirmed')
    except Exception as e:
        return make_400('Problem. {}'.format(str(e)))


@bp.route('/profile', methods=['GET'])
@login_required
def profile():
    try:
        as_creator, as_presenter, as_participant = events_logic.get_user_stat(current_user.id)
        return jsonify(creator=as_creator, presenter=as_presenter,
                       participant=as_participant)
    except Exception as e:
        return make_400('Problem. {}'.format(str(e)))


@bp.route('/join', methods=['POST'])
@login_required
def join():
    try:
        args = request.get_json()
        if not args:
            return make_400('Expected json')

        if events_logic.event_exist(int(args['event_id'])):
            join = events_logic.join_event(current_user.id,
                                        int(args['event_id']), args['role'])
            if join:
                return make_400(join)
            return make_ok('Guest joined event')
        else:
            return make_400('No such event')
    except Exception as e:
        return make_400('Problem.\n{}'.format(str(e)))


@bp.route('/users', methods=['GET'])
def users():
    try:
        return jsonify(users_logic.get_users())
    except Exception as e:
        return make_400('Problem.\n{}'.format(str(e)))


#-------------------------- CHECK --------------------------

@bp.route('/update_profile', methods=['POST'])
@login_required
def update_profile():
    try:
        args = request.get_json()
        if not args:
            return make_400('Expected json')

        users_logic.update_profile(current_user.id, args)
        return make_ok('Profile info successfully updated.')
    except Exception as e:
        return make_400('Problem. {}'.format(str(e)))


@bp.route('/update_password', methods=['POST'])
@login_required
def update_password():
    try:
        args = request.get_json()
        if not args:
            return make_400('Expected json')

        if current_user.change_password(args['old_password'],
                                        args['new_password']):
            return make_ok('Password changed successfully.')
        else:
            return make_400('Incorrect old password!')
    except Exception as e:
        return make_400('Problem. {}'.format(str(e)))