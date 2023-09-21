# Red-Bird-PynamoDB-DynamoDB
Red-Bird-PynamoDB-DynamoDB

# Using PynamoDB and Repository for Database Interaction

## Introduction

This document describes how to interact with a database using the PynamoDB library and a repository RED-Bird created based on the TemplateRepo class.

### Prerequisites

1. **Install Required Libraries:** Make sure you have the required libraries installed, such as pynamodb and dotenv.

2. **Fill in the .env File:** To access AWS and the database, ensure that the .env file contains the necessary environment variables, such as DATABASE_DYNAMO, AWS_ACCESS_KEY_ID, and AWS_SECRET_ACCESS_KEY.

## pynamodb_models.py File

This file contains data model definitions and database connection configuration.

### Data Model

The `Users` class represents the data model for the "Users" table. It consists of three attributes: id, name, and email.

### Connection Configuration

The `ModelConfig` class stores the database connection configuration, including information such as the host, access key, and secret access key.

```python
import os, sys
from dotenv import load_dotenv
from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, ".env"))
sys.path.append(BASE_DIR)


class ModelConfig:
    host = os.environ["DATABASE_DYNAMO"]
    aws_access_key_id = os.environ["AWS_ACCESS_KEY_ID"]
    aws_secret_access_key = os.environ["AWS_SECRET_ACCESS_KEY"]


```

## pynamodb_repo.py

This file contains the `PynamoDBRepo` class, which inherits from the `TemplateRepo` class and enables interaction with the database.

### Repository Initialization

In the `PynamoDBRepo` constructor, an instance of the model passed as an argument is created, and then the corresponding table is created in the database.

### Database Operations

- `insert(item)`: This method allows adding new records to the database based on the provided item.

- `query_data(query)`: This method is used to retrieve data from the database based on a defined query. It returns records that match the criteria.

- `query_update(query, values)`: It allows updating records in the database that meet the query conditions with the specified values.

- `query_delete(query)`: Deletes records from the database that match the query.

```python
from redbird.templates import templaterepo
from app.pydamo_models import Users

class PynamoDBRepo(TemplateRepo):
    def __init__(self, model):
        super().__init__(model=model)
        # Created model in the database
        self.model.create_table(wait=True)

    def insert(self, item):
        # Insert an element into the database
        instance = self.model(**item)
        instance.save()

    def query_data(self, query):
        # Retrieving data from the database based on a query
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
```

## Usage Examples

Here are some usage examples illustrating how to interact with the database using the PynamoDB and repository:

```python
# Creating a repository instance for the Users model
repo = PynamoDBRepo(model=Users)

# Adding new records to the database
repo.insert({'name': 'Ewa1', 'email': "30", "id": "12"})
repo.insert({'name': 'Ola', 'email': "dddd", "id": "2"})

# Retrieving data based on a condition
results = repo.query_data({'name': "James"})
for item in results:
    print(item)

# Retrieving the first matching record using a filter
print(repo.filter_by(name="James").first())

# Updating records in the database
repo.query_update({"id": "8", "name": "James"}, {'email': "wp@wp.pl"})

# Deleting records from the database
repo.query_delete({'name': 'John'})

```

## Summary

This code enables convenient interaction with a database using the PynamoDB model and repository Red-Bird. With these tools, you can easily add, retrieve, update, and delete data from the database in an automated and organized manner.

Feel free to utilize this code and the provided examples to streamline your database operations and maintain data integrity efficiently.
