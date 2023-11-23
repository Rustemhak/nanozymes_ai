# Importing required libraries again
import re
import ast
from pprint import pprint
import pandas as pd
# Let's try reading the uploaded log file again
file_path = 'auto_metric.log'

with open(file_path, 'r', encoding='utf-8') as f:
    log_data = f.read()

# Displaying the first 500 characters to get a glimpse of the data
# print(log_data[:500])

# Updated Regular expressions
article_re = re.compile(r"article='(https://doi\.org/[^']+)'")
km_re = re.compile(r"WARNING - ({'Km': .*?})\n", re.DOTALL)
assessment_re = re.compile(r"Assessment: (\d+ out of \d+)")



# Re-run Parsing for all types of data
articles = article_re.findall(log_data)
km_raw_data = km_re.findall(log_data)
assessments = assessment_re.findall(log_data)


# Re-run Filtering and Parsing for 'Km'
km_data = []
for km in km_raw_data:
    try:
        km_data.append(ast.literal_eval(km))
    except SyntaxError:
        # Skip this entry if it's not a valid Python literal
        pass

# Re-run Data transformation
parsed_data = []
for article, km, assessment in zip(articles, km_data, assessments):
    parsed_data.append({
        'Article': article,
        'Km': km,
        'Assessment': assessment
    })

# Displaying the first 3 records for review
pprint(parsed_data)

