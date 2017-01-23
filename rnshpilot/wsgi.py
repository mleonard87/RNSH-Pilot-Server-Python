import logging

from flask import Flask
from flask_graphql import GraphQLView

from rnshpilot.graphql.schema import schema

logging.basicConfig(level=logging.ERROR)


app = Flask(__name__)

app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))
