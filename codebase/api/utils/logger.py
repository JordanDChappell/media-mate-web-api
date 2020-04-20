import logging

def get_logger(name):
  return logging.getLogger('mediamate.{0}'.format(name))