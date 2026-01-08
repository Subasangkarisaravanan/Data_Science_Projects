import requests
import pandas as pd
import pycountry

# WHO API URLs
urls = {
    "obesity_adults": 'https://ghoapi.azureedge.net/api/NCD_BMI_30C',
    "obesity_children": 'https://ghoapi.azureedge.net/api/NCD_BMI_PLUS2C',
    "malnutrition_adults": 'https://ghoapi.azureedge.net/api/NCD_BMI_18C',
    "malnutrition_children": 'https://ghoapi.azureedge.net/api/NCD_BMI_MINUS2C'
}

# Fetch JSON data
data = {k: requests.get(v).json() for k,v in urls.items()}

# Convert to DataFrames
df_ob_a = pd.DataFrame(data["obesity_adults"]['value'])
df_ob_c = pd.DataFrame(data["obesity_children"]['value'])
df_ma_a = pd.DataFrame(data["malnutrition_adults"]['value'])
df_ma_c = pd.DataFrame(data["malnutrition_children"]['value'])

# Add age_group
df_ob_a['age_group'] = "Adult"
df_ob_c['age_group'] = "Child/Adolescent"
df_ma_a['age_group'] = "Adult"
df_ma_c['age_group'] = "Child/Adolescent"

# Combine adults+children
df_obesity = pd.concat([df_ob_a, df_ob_c], ignore_index=True)
df_malnutrition = pd.concat([df_ma_a, df_ma_c], ignore_index=True)

# Filter years 2012-2022
df_obesity = df_obesity[(df_obesity['TimeDim'] >= 2012) & (df_obesity['TimeDim'] <= 2022)]
df_malnutrition = df_malnutrition[(df_malnutrition['TimeDim'] >= 2012) & (df_malnutrition['TimeDim'] <= 2022)]

# Keep necessary columns
cols = ["ParentLocation","Dim1","TimeDim","Low","High","NumericValue","SpatialDim","age_group"]
df_obesity = df_obesity[cols]
df_malnutrition = df_malnutrition[cols]

# Rename columns
rename_cols = {
    'TimeDim': 'Year',
    'Dim1': 'Gender',
    'NumericValue': 'Mean_Estimate',
    'Low': 'LowerBound',
    'High': 'UpperBound',
    'ParentLocation': 'Region',
    'SpatialDim': 'Country'
}
df_obesity = df_obesity.rename(columns=rename_cols)
df_malnutrition = df_malnutrition.rename(columns=rename_cols)

# Standardize Gender
gender_map = {'sex_mle': 'Male', 'sex_fmle': 'Female', 'sex_btsx': 'Both'}
df_obesity['Gender'] = df_obesity['Gender'].str.lower().replace(gender_map)
df_malnutrition['Gender'] = df_malnutrition['Gender'].str.lower().replace(gender_map)

# Convert country codes to full names
special_cases = {
    'GLOBAL': 'Global', 'WB_LMI': 'Low & Middle Income', 'WB_HI': 'High Income',
    'WB_LI': 'Low Income', 'WB_UMI': 'Upper Middle Income', 'EMR': 'Eastern Mediterranean Region',
    'EUR': 'Europe', 'AFR': 'Africa', 'SEAR': 'South-East Asia Region',
    'WPR': 'Western Pacific Region', 'AMR': 'Americas Region'
}
def convert_country(code):
    if pd.isna(code): return code
    if code in special_cases: return special_cases[code]
    c = pycountry.countries.get(alpha_3=code)
    return c.name if c else code

df_obesity['Country'] = df_obesity['Country'].apply(convert_country)
df_malnutrition['Country'] = df_malnutrition['Country'].apply(convert_country)

# CI Width
df_obesity['CI_Width'] = df_obesity['UpperBound'] - df_obesity['LowerBound']
df_malnutrition['CI_Width'] = df_malnutrition['UpperBound'] - df_malnutrition['LowerBound']

# Obesity & Malnutrition levels
df_obesity['obesity_level'] = df_obesity['Mean_Estimate'].apply(lambda x: 'High' if x >=30 else 'Moderate' if 25<=x<=29.9 else 'Low')
df_malnutrition['malnutrition_level'] = df_malnutrition['Mean_Estimate'].apply(lambda x: 'High' if x>=20 else 'Moderate' if 10<=x<=19.9 else 'Low')

# Save CSV for DB insertion
df_obesity.to_csv("df_obesity_clean.csv", index=False)
df_malnutrition.to_csv("df_malnutrition_clean.csv", index=False)
print("Data cleaning complete!")