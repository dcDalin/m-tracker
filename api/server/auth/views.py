#! /api/server/auth/views.py
# -*- coding: utf-8 -*-
"""This is the auth module

This module contains various routes for the auth endpoint
"""

from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView
from marshmallow import ValidationError

from api.server.auth.schema import UserSchema

# Create a blueprint
AUTH_BLUEPRINT = Blueprint('auth', __name__, url_prefix='/v1/auth')

# Instanciate marshmallow
USER_SCHEMA = UserSchema()


class RegisterAPI(MethodView):
    """User Registration resource"""

    def post(self):  # pylint: disable=R0201
        """post method"""
        # get the post data
        post_data = request.get_json()

        # check for no input i.e. {}
        if not post_data:
            response_object = {
                'status': 'fail',
                'message': 'No input data provided.'
            }
            return make_response(jsonify(response_object)), 400
        # load input to the marshmallow schema
        try:
            USER_SCHEMA.load(post_data)

        # return error object case there is any
        except ValidationError as err:
            response_object = {
                'status': 'fail',
                'message': 'Validation errors.',
                'errors': err.messages
            }
            return make_response(jsonify(response_object)), 422

        # if no validation errors
        # check if user already exists - check their email address

        response_object = {
            'status': 'success',
            'message': 'Successfully registered.'
        }
        return make_response(jsonify(response_object)), 201


# define API resources
REGISTRATION_VIEW = RegisterAPI.as_view('register_api')

# add rules for auth enpoints
AUTH_BLUEPRINT.add_url_rule(
    '/register',
    view_func=REGISTRATION_VIEW,
    methods=['POST']
)
