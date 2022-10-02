import graphene
from graphene.relay import Node

from graphene_mongo import MongoengineConnectionField, MongoengineObjectType
from parliament_models import LegislativeDocuments as LegislativeDocumentsModel
from parliament_models import DocumentAttributes as DocumentAttributesModel

class DocumentAttributes(MongoengineObjectType):
    class Meta:
        model = DocumentAttributesModel
        interfaces = (Node,)
        # filter_fields = {
        #     'document_number': ['exact'],
        #     'document_ratification_date': ['exact', 'contains'],
        #     'document_promulgation_date': ['exact', 'contains'],
        #     'document_LN': ['exact'],
        #     'document_TLN': ['exact']
        # }

class LegislativeDocuments(MongoengineObjectType):
    class Meta:
        model = LegislativeDocumentsModel
        interfaces = (Node,)
        filter_fields = {
            'document_title': ['exact', 'contains']
        }


class Query(graphene.ObjectType):
    node = Node.Field()
    all_legislative_documents = MongoengineConnectionField(LegislativeDocuments)

schema = graphene.Schema(query = Query, types = [LegislativeDocuments], auto_camelcase = False)
