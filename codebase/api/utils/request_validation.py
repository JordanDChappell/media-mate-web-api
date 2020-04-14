# file:         request_validation.py
# description:  Utility functions to verify required API request parameters

from flask import request

def required_query_params(request, parameters):
  """Validate that a set of query parameters are present in a request"""
  for expected_param in parameters:
    received_param = request.args.get(expected_param)
    if received_param is None:
      message = { 'message': 'required query parameter \'{0}\' is missing'.format(expected_param) }
      status_code = 400 # 400 status = bad request, missing parameter
      return message, status_code
