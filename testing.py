

from credit_risk.utils.main_utils import read_yaml
from credit_risk.constants import SCHEMA_FILE

data = read_yaml(SCHEMA_FILE)

ty =  data.train_columns.SeriousDlqin2yrs

print(type(ty))