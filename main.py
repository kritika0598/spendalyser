import json
import pandas

with open("data.json", "r") as json_file:
    conversion_dict = json.load(json_file)

excel_data_df = pandas.read_excel('records.xlsx')

json_str = excel_data_df.to_json(orient='records')
json_str = json.loads(json_str)

amount = {"extra": 0}
for key, value in conversion_dict.items():
    amount[value] = 0

for data in json_str:
    debit_amount = data["Debit"]
    if isinstance(debit_amount, str):
        debit_amount = debit_amount.replace(',', '')
    credit_amount = data["Credit"]
    if isinstance(credit_amount, str):
        credit_amount = float(credit_amount.replace(',', ''))
    if credit_amount is None:
        credit_amount = 0
    if debit_amount is None:
        debit_amount = 0
    assigned = False
    for key, value in conversion_dict.items():
        if key.lower() in data["Description"].lower():
            amount[value] = amount[value] - debit_amount + credit_amount
            assigned = True
            break
    if not assigned:
        amount['extra'] = amount['extra'] - debit_amount + credit_amount

print(amount)
