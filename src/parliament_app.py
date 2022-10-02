from flask import Flask
#from flask_graphql import GraphQLView
from graphql_server.flask import GraphQLView
from parliament_schema import schema
from mongoengine import connect

class DictWithQuerySet(dict):
    def __init__(self, *args, **kwargs):
        super(DictWithQuerySet, self).__init__(*args, **kwargs)
        self.queryset = None

class MyGraphQLView(GraphQLView):
    def get_context(self):
        context = super().get_context()
        return DictWithQuerySet(context)

connect(
    db = 'crawler_db',
    username = 'Marukun',
    password = 'marukun',
    host = 'localhost',
    port = 27017,
    authentication_source = 'admin',
    #host="mongodb://Marukun:marukun@localhost:27017/crawler_db"
    )

app = Flask(__name__)
app.debug = True
app.logger.debug("debug")
app.logger.info("info")
app.logger.warning("warning")
app.logger.error("error")
app.logger.critical("critical")

default_query = """
{
  all_legislative_documents {
    edges {
      node {
        document_title,
        document_attributes {
          document_number,
          document_ratification_date,
          document_promulgation_date,
          document_ruu_reference,
          document_LN,
          document_TLN
        }
      }
    }
  }
}""".strip()

app.add_url_rule(
    "/graphql", view_func=MyGraphQLView.as_view("graphql", schema=schema.graphql_schema, graphiql=True)
)

if __name__ == "__main__":
    app.run()