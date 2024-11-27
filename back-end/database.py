from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.engine.row import Row
from enum import Enum

import json

db = SQLAlchemy()

class AlchemyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Row):
            # Convert Row objects to dictionaries
            row_dict = dict(obj._mapping)
            # Convert Enum fields (like Account.role) to their string representation
            
            for key, value in row_dict.items():
                if isinstance(value, Enum):
                    row_dict[key] = value.value  # Get the string or integer value of the Enum
            return row_dict
        return super().default(obj)