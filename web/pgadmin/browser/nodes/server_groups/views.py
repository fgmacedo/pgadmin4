##########################################################################
#
# pgAdmin 4 - PostgreSQL Tools
#
# Copyright (C) 2013 - 2015, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################

"""Defines views for management of server groups"""

NODE_NAME = 'server-group'

NODE_PATH = '/browser/' + NODE_NAME

import traceback
from flask import Blueprint, Response, current_app, request
from flask.ext.security import current_user, login_required

from utils.ajax import make_json_response
from pgadmin.settings.settings_model import db, ServerGroup
import config

# Initialise the module
blueprint = Blueprint("NODE-" + NODE_NAME, __name__, static_folder='static',  static_url_path='', template_folder='templates', url_prefix=NODE_PATH)

@blueprint.route('/add/', methods=['POST'])
@login_required
def add():
    """Add a server group node to the settings database"""
    success = 1
    errormsg = ''
    data = { }
    
    if request.form['name'] != '':
        servergroup = ServerGroup(user_id=current_user.id, name=request.form['name'])

        try:
            db.session.add(servergroup)
            db.session.commit()
        except Exception as e:
            success = 0
            errormsg = e.message

    else:
        success = 0
        errormsg = "No server group name was specified"
            
    if success == 1:
        data['id'] = servergroup.id
        data['name'] = servergroup.name
        
    return make_json_response(success=success, 
                              errormsg=errormsg, 
                              info=traceback.format_exc(), 
                              result=request.form, 
                              data=data)

@blueprint.route('/delete/', methods=['POST'])
@login_required
def delete():
    """Delete a server group node in the settings database"""
    success = 1
    errormsg = ''

    if request.form['id'] != '':
        # There can be only one record at most
        servergroup = ServerGroup.query.filter_by(user_id=current_user.id, id=int(request.form['id'])).first()
        
        if servergroup is None:
            success = 0
            errormsg = 'The specified server group could not be found.'
        else:
            try:
                db.session.delete(servergroup)
                db.session.commit()
            except Exception as e:
                success = 0
                errormsg = e.message

    else:
        success = 0
        errormsg = "No server group  was specified."
            
    return make_json_response(success=success, 
                              errormsg=errormsg, 
                              info=traceback.format_exc(), 
                              result=request.form)

@blueprint.route('/rename/', methods=['POST'])
@login_required
def rename():
    """Rename a server group node in the settings database"""
    success = 1
    errormsg = ''

    if request.form['id'] != '':
        # There can be only one record at most
        servergroup = ServerGroup.query.filter_by(user_id=current_user.id, id=int(request.form['id'])).first()
        
        if servergroup is None:
            success = 0
            errormsg = 'The specified server group could not be found.'
        else:
            try:
                servergroup.name = request.form['name']
                db.session.commit()
            except Exception as e:
                success = 0
                errormsg = e.message

    else:
        success = 0
        errormsg = "No server group was specified."
            
    return make_json_response(success=success, 
                              errormsg=errormsg, 
                              info=traceback.format_exc(), 
                              result=request.form)