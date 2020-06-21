# -*- coding: utf-8 -*-
#
# Copyright 2020 AllanKT.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import uuid
import json
import boto3
from boto3.dynamodb.conditions import Key
import datetime
from decimal import Decimal

class Dynamo:
    def __init__(self, credentials, tables):
        self.dynamodb = boto3.resource('dynamodb', **credentials)
        self.table = { item['tablename']: Functions(self.dynamodb, item) for item in tables }
        for (key, value) in self.table.items():
            self.__dict__[key] = value

class Functions(dict):
    def __init__(self, dynamo, table):
        self.table = table
        self.dynamodb = dynamo.Table(table['tablename'])

    def insert(self, data):
        if self.table['uuid']:
            data[self.table['uuid']] = str(uuid.uuid4())
        if self.table['timestamp']:
            data['created_at'] = data.get('created_at', datetime.datetime.now().timestamp())
            data['updated_at'] = datetime.datetime.now().timestamp()
        return data

    def replace_decimals(self, obj):
        if isinstance(obj, list):
            for i in range(len(obj)):
                obj[i] = self.replace_decimals(obj[i])
            return obj
        elif isinstance(obj, dict):
            for k in obj.keys():
                obj[k] = self.replace_decimals(obj[k])
            return obj
        elif isinstance(obj, Decimal):
            if obj % 1 == 0:
                return int(obj)
            else:
                return float(obj)
        else:
            return obj

    def query(self, data):
        variables, values, expressions = {}, {}, ""
        for pos, (key, operation) in enumerate(data['query'].items()):
            if isinstance(operation, dict):
                op, value = list(operation.keys())[0], list(operation.values())[0]
            variables[f"#{key}"] = key
            if isinstance(value, dict):
                comp, value = list(value.keys())[0], list(value.values())[0]
                if isinstance(value, list):
                    exp = []
                    for pos_v, item in enumerate(value):
                        values[f":{key}_{pos_v}"] = item
                        exp.append(f":{key}_{pos_v}")
                    if comp == 'between':
                        exp = ' and '.join(exp)
                    if comp == 'in':
                        exp = f" ( {' , '.join(exp)} ) "
                    expressions += f"{ op if pos else '' } (#{key} {comp} {exp}) "
                else:
                    values[f":{key}"] = value
                    if comp in [
                        'contains',
                        'begins_with',
                        'attribute_type',
                        'attribute_exists',
                        'attribute_not_exists',
                    ]:
                        expressions += f"{ op if pos else '' } {comp}(#{key} , :{key}) "
                    else:
                        expressions += f"{ op if pos else '' } (#{key} {comp} :{key}) "
            else:
                values[f":{key}"] = value
                if comp in [
                        'contains',
                        'begins_with',
                        'attribute_type',
                    ]:
                    expressions += f"{ op if pos else '' } {comp}(#{key} , :{key}) "
                else:
                    expressions += f"{ 'and' if pos else '' } (#{key} = :{key}) "

        response = {
            'ExpressionAttributeNames': variables,
            'ExpressionAttributeValues': values,
            'FilterExpression': expressions,
        }
        if data.get('index', False):
            response['IndexName'] = data['index']
        return response

    def scan(self, data=None):
        try:
            if data:
                data = self.query(data)
                data['response'] = self.replace_decimals(self.dynamodb.scan(**data))
                return data
            get = self.dynamodb.scan()
            return { 'response': self.replace_decimals(get) }
        except Exception as e:
            return e

    def add(self, data):
        try:
            data = json.loads(json.dumps(self.insert(data)), parse_float=Decimal, parse_int=Decimal)
            return self.dynamodb.put_item(Item = data)
        except Exception as e:
            return e

    def get(self, key):
        try:
            get = self.dynamodb.get_item(Key = key)
            return self.replace_decimals(get)
        except Exception as e:
            return e

    def delete(self, key):
        try:
            delete = self.dynamodb.delete_item(Key = key)
            return self.replace_decimals(delete)
        except Exception as e:
            return e

    def put(self, data):
        try:
            data = json.loads(json.dumps(self.insert(data)), parse_float=Decimal, parse_int=Decimal)
            return self.replace_decimals(self.dynamodb.put_item(Item = data))
        except Exception as e:
            return e

    def batch_insert(self, items):
        try:
            items = json.loads(json.dumps(items), parse_float=Decimal, parse_int=Decimal)
            with self.dynamodb.batch_writer() as batch:
                return self.replace_decimals([
                    batch.put_item(Item = item)
                    for item in items
                ])
            return []
        except Exception as e:
            return e

    def batch_delete(self, items):
        try:
            with self.dynamodb.batch_writer() as batch:
                self.replace_decimals([
                    batch.delete_item(Key = { self.table['uuid']: item })
                    for item in items
                ])
                return "Success"
            raise Exception("Error")
        except Exception as e:
            return e

    def batch_put(self, items):
        try:
            with self.dynamodb.batch_writer() as batch:
                return self.replace_decimals([
                    batch.put_item(Item = item)
                    for item in items
                ])
            return []
        except Exception as e:
            return e

    def batch_get(self, items):
        try:
            with self.dynamodb.batch_writer() as batch:
                return self.replace_decimals([
                    batch.get_item(Key = { self.table['uuid']: item })
                    for item in items
                ])
            return []
        except Exception as e:
            return e
