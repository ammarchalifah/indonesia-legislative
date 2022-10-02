from datetime import datetime
from sqlite3 import Date
from mongoengine import Document, EmbeddedDocument
from mongoengine.fields import (
    DateTimeField,
    EmbeddedDocumentField,
    StringField,
    IntField
)

class DocumentAttributes(EmbeddedDocument):
    document_number = StringField(db_field = 'Nomor')
    document_ratification_date = StringField(db_field = 'Tanggal Disahkan')
    document_promulgation_date = StringField(db_field = 'Tanggal Diundangkan')
    document_LN = StringField(db_field = 'LN')
    document_TLN = StringField(db_field = 'TLN')
    document_pdf_url = StringField(db_field = 'File')
    document_ruu_reference = StringField(db_field = 'Referensi RUU')


class LegislativeDocuments(Document):
    meta = {"collection": "crawler_coll"}
    id = IntField(primary_key = True)
    document_title = StringField(db_field = 'document_title')
    document_attributes = EmbeddedDocumentField(DocumentAttributes)
    last_modified = DateTimeField(db_field = 'lastModified')
