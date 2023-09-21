from redbird.templates import templaterepo
from .pydamo_models import Users

class PynamoDBRepo(TemplateRepo):
    def __init__(self, model):
        super().__init__(model=model)
        # Created model in database
        self.model.create_table(wait=True)

    def insert(self, item):
        # Insert an element to database
        instance = self.model(**item)
        instance.save()

    def query_data(self, query):
        # Retrieving data from a database based on a query
        for item in self.model.scan():
            include_item = all(
                query_value == getattr(item, key)
                for key, query_value in query.items()
            )
            if include_item:
                yield item.attribute_values

    def query_update(self, query, values):
        # Update items in the database that match the query with the specified values
        for item in self.model.scan():
            update_item = all(
                query_value == getattr(item, key)
                for key, query_value in query.items()
            )
            if update_item:
                for key, updated_value in values.items():
                    setattr(item, key, updated_value)
                item.save()

    def query_delete(self, query):
        # Removing items from the database that match the query
        for item in self.model.scan():
            delete_item = all(
                query_value == getattr(item, key)
                for key, query_value in query.items()
            )
            if delete_item:
                item.delete()
