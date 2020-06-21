# python-dynamo

[![Build Status](https://api.travis-ci.org/truly-systems/dynamodb.svg?branch=master)](https://travis-ci.org/AllanKT/dynamodb)
![PyPi version](https://img.shields.io/pypi/v/dynamodb.svg)

DynamoDB SDK AWS implementation in Python developed by AllanKT.

## Description

This SDK was written to assist the development of applications that use the AWS DynamoDB service, to management CRUD operations.

## Install

You can install **dynamodb** with pip:

* PyPi:

```bash
pip install dynamodb
```

## Usage

First to first, set your credentials AMI in a dict object:

```python
credentials = {
    'region_name': '<REGION_NAME>',
    'aws_access_key_id': '<ACCESS_KEY>',
    'aws_secret_access_key': '<SECRET_KEY>'
}
```

Then define your tables configurations:

* **tablename**: (required) Name to your table;
* **uuid**: (optional) Set this field if you want it to be automatically filled with a uuid4, with its value as the name of the table's primaryKey;
* **timestamp**: (optional) Set this field if you want createdAt and updateAt columns to be filled in automatically;

```python
tables = [
    {
        'tablename': 'teste1',
        'uuid': 'id',
        'timestamp': True,
    },
    {
        'tablename': 'teste2',
        'uuid': 'my_id',
    },
    {
        'tablename': 'teste3',
    }
]
```

Import **dynamodb** in your code and create a connection with database:

```python
from dynamodb import Dynamo

dynamo = Dynamo(credentials, tables)
``` 

### **Use tables**

```python
dynamo.teste1
dynamo.table['teste1']
```

### **Insert**

```python
dynamo.teste1.insert({'x': 'teste', 'y': 1, 'z': 'A'})

{
    'id': 'ac38f1...591e14d',
    'x': 'teste',
    'y': 1,
    'z': 'A',
    'updated_at': 1592697324.910402,
    'created_at': 1592697324.910402,
}
```

### **Get**

```python
d.teste1.get('ac38f1...591e14d')

{
    'id': 'ac38f1...591e14d',
    'x': 'teste',
    'y': 1,
    'z': 'A',
    'updated_at': 1592697324.910402,
    'created_at': 1592697324.910402,
}
```

### **Delete**

```python
d.teste1.delete('ac38f1...591e14d')
```

### **Batch Insert**

```python
datas = [
    {
        'x': 'teste1',
        'y': 1,
        'z': 'A',
    },
    {
        'x': 'teste2',
        'y': 2,
        'z': 'B',
    },
    {
        'x': 'teste3',
        'y': 3,
        'z': 'C',
    }
]

dynamo.table1.batch_insert(datas)
```

### **Batch_get**

```python
dynamo.table1.batch_get(['ac38f1...591e14d', '0be3f5...59104ad'])

[
    {
        'id': 'ac38f1...591e14d'
        'x': 'teste1',
        'y': 1,
        'z': 'A',
        'updated_at': 1592697324.910402,
        'created_at': 1592697324.910402,
    },
    {
        'id': '0be3f5...59104ad',
        'x': 'teste2',
        'y': 2,
        'z': 'B',
        'updated_at': 1592697324.910402,
        'created_at': 1592697324.910402,
    }
]
```

### **Batch_delete**

```python
dynamo.table1.batch_delete(['ac38f1...591e14d', '0be3f5...59104ad'])
```

### **Scan**

```python
dynamo.teste1.scan({
    'index': 'z-index', # optional
    'query': {
        'x': {
            'and': {
                'begins_with': '1'
            }
        },
        'y': {
            'and': {
                'between': [1, 2]
            }
        },
        'z': {
            'or': {
                'in': ['A', 'B']
            }
        }
    }
})
```

* Operations usade:

```python
'column_name': {
    'operator': {
        'expression_operator ': 'value'
    }
}
```

* **Operators**:

| Operator | Description |
| ------ | ------ |
| and | AND conditional operator |
| or | OR conditional operator |
| < | Less Than operator |
| <= | Less Than or Equal To operator |
| > | Greater than operator |
| >= | Greater Than or Equal To operator |
| = | Equal Than operator |
| != | Different conditional operator |

* **Expression Operators**:

| Expression Operator | Description |
| ------ | ------ |
| between | Key between two values |
| in | Key is contant in a list |
| begins_with | Key begin with the value |
| attribute_type | ??? |
| contains | ??? |


## Implementation Details

### Supported Python Versions

* Python 3.5
* Python 3.6
* Python 3.7

### License

python-dynamo is licensed under the Apache License version 2. See ./LICENSE.rst.
