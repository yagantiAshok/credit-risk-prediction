
import streamlit as st
from credit_risk.pipeline.prediction_pipeline import CustomerData,CreditriskClassifier
from credit_risk.logger import logger
from credit_risk.utils.main_utils import read_yaml
from credit_risk.constants import SCHEMA_FILE
import os

st.set_page_config("Credit-Risk-Classifier",layout="centered")
st.title("Credit-Risk-Classifier")

data = read_yaml(SCHEMA_FILE)
user = { }

# user["RevolvingUtilizationOfUnsecuredLines"] = st.number_input("RevolvingUtilizationOfUnsecuredLines",min_value=0,value=0)
# user["age"] = st.number_input("age",min_value=0,value = 0)
# user["NumberOfTime30to59DaysPastDueNotWorse"] = st.number_input("NumberOfTime30to59DaysPastDueNotWorse",min_value=0,value=0)
# user["DebtRatio"] = st.number_input("DebtRatio",min_value=0,value=0)
# user["NumberOfOpenCreditLinesAndLoans"] = st.number_input("NumberOfOpenCreditLinesAndLoans",min_value=0,value=0)
# user["NumberOfTimes90DaysLate"] = st.number_input("NumberOfTimes90DaysLate",min_value=0,value=0)
# user["NumberRealEstateLoansOrLines"] = st.number_input("NumberRealEstateLoansOrLines",min_value=0,value=0)
# user["NumberOfTime60to89DaysPastDueNotWorse"] = st.number_input("NumberOfTime60to89DaysPastDueNotWorse",min_value=0,value=0)
# user["NumberOfDependents"] = st.number_input("NumberOfDependents",min_value=0,value=0)
# user["MonthlyIncome"] = st.number_input("MonthlyIncome",min_value=0,value=0)

for col in data.fields:
    user[col["name"]] = st.number_input(col["name"],min_value=col["min_value"],value=col["value"])

data = CustomerData(**user)
data_frame = data.convert_to_dataframe()

@st.cache_resource
def classifier():
    return CreditriskClassifier()
predcition = classifier()
credit_risk_class = predcition.predict(data=data_frame)[0]

if st.button("Predict"):
    if credit_risk_class == 1:
        st.error("Customer is Risky")
    else:
        st.error("Customer is not Risky")

