import os
import sys

os.environ['SERVICE'] = 'aws-cd-pipeline'
os.environ['STACK'] = 'localstack'
os.environ['STAGE'] = 'localtest'

# manipulating sys.path to make importing inside tests because ¯\_(ツ)_/¯
here = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(here, '..', 'src'))
