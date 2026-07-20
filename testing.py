

from credit_risk.utils.main_utils import read_yaml
from credit_risk.constants import SCHEMA_FILE

# data = read_yaml(SCHEMA_FILE)

# ty =  data.train_columns.SeriousDlqin2yrs

# print(type(ty))

# class A:

#     def __init__(self,
#                  x=10,
#                  y=20):

#         self.x = x
#         self.y = y
# B = A
# print(B.x)

# from credit_risk.model_factory.model_storage import models_dictionary

# print(models_dictionary["AdaBoostClassifier"])

data = read_yaml(SCHEMA_FILE)

# print(data.fields)

for field in data.fields:
    print(field["value"])