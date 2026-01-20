import requests
import pandas as pd
import pycountry

# ---------------- Step 1: WHO API URLs ----------------
urls = {
    "obesity_adults": 'https://ghoapi.azureedge.net/api/NCD_BMI_30C',
    "obesity_children": 'https://ghoapi.azureedge.net/api/NCD_BMI_PLUS2C',
    "malnutrition_adults": 'https://ghoapi.azureedge.net/api/NCD_BMI_18C',
    "malnutrition_children": 'https://ghoapi.azureedge.net/api/NCD_BMI_MINUS2C'
}

# ---------------- Step 2: Fetch JSON data ----------------
data = {k: requests.get(v).json() for k,v in urls.items()}
for k in data:
    print(f"Step 2: Sample JSON data for {k} (first 2 rows):")
    print(data[k]['value'][:2], "\n")

# ---------------- Step 3: Convert to DataFrames ----------------
df_ob_a = pd.DataFrame(data["obesity_adults"]['value'])
df_ob_c = pd.DataFrame(data["obesity_children"]['value'])
df_ma_a = pd.DataFrame(data["malnutrition_adults"]['value'])
df_ma_c = pd.DataFrame(data["malnutrition_children"]['value'])
print("Step 3: DataFrames created")
print("Obesity Adults:")
print(df_ob_a.head(), "\n")
print("Obesity Children:")
print(df_ob_c.head(), "\n")
print("Malnutrition Adults:")
print(df_ma_a.head(), "\n")
print("Malnutrition Children:")
print(df_ob_c.head(), "\n")

# ---------------- Step 4: Add age_group ----------------
df_ob_a['age_group'] = "Adult"
df_ob_c['age_group'] = "Child/Adolescent"
df_ma_a['age_group'] = "Adult"
df_ma_c['age_group'] = "Child/Adolescent"
print("Step 4: age_group added")
print("Obesity Adults:")
print(df_ob_a.head()[['Dim1','age_group']], "\n")
print("Obesity Children:")
print(df_ob_c.head()[['Dim1','age_group']], "\n")
print("Malnutrition Adults:")
print(df_ma_a.head()[['Dim1','age_group']], "\n")
print("Malnutrition Children:")
print(df_ma_c.head()[['Dim1','age_group']], "\n")

# ---------------- Step 5: Combine adults+children ----------------
df_obesity = pd.concat([df_ob_a, df_ob_c], ignore_index=True)
df_malnutrition = pd.concat([df_ma_a, df_ma_c], ignore_index=True)
print("Step 5: Adults and children combined")
print("Obesity:")
print(df_obesity.head(10)[['age_group','Dim1','NumericValue']], "\n")
print("Malnutrition:")
print(df_malnutrition.head(10)[['age_group','Dim1','NumericValue']], "\n")

# ---------------- Step 6: Filter years 2012-2022 ----------------
df_obesity = df_obesity[(df_obesity['TimeDim'] >= 2012) & (df_obesity['TimeDim'] <= 2022)]
df_malnutrition = df_malnutrition[(df_malnutrition['TimeDim'] >= 2012) & (df_malnutrition['TimeDim'] <= 2022)]
print("Step 6: Filtered years 2012-2022")
print("Obesity years:", df_obesity['TimeDim'].unique())
print("Malnutrition years:", df_malnutrition['TimeDim'].unique(), "\n")

# ---------------- Step 7: Keep necessary columns ----------------
cols = ["ParentLocation","Dim1","TimeDim","Low","High","NumericValue","SpatialDim","age_group"]
df_obesity = df_obesity[cols]
df_malnutrition = df_malnutrition[cols]
print("Step 7: Kept necessary columns")
print("Obesity:")
print(df_obesity.head(), "\n")
print("Malnutrition:")
print(df_malnutrition.head(), "\n")

# ---------------- Step 8: Rename columns ----------------
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
print("Step 8: Columns renamed")
print("Obesity:")
print(df_obesity.head(), "\n")
print("Malnutrition:")
print(df_malnutrition.head(), "\n")

# ---------------- Step 9: Standardize Gender ----------------
gender_map = {'sex_mle': 'Male', 'sex_fmle': 'Female', 'sex_btsx': 'Both'}
df_obesity['Gender'] = df_obesity['Gender'].str.lower().replace(gender_map)
df_malnutrition['Gender'] = df_malnutrition['Gender'].str.lower().replace(gender_map)
print("Step 9: Gender standardized")
print("Obesity Genders:", df_obesity['Gender'].unique())
print("Malnutrition Genders:", df_malnutrition['Gender'].unique(), "\n")

# ---------------- Step 10: Convert country codes ----------------
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
print("Step 10: Country codes converted")
print("Obesity Countries:")
print(df_obesity['Country'].head(), "\n")
print("Malnutrition Countries:")
print(df_malnutrition['Country'].head(), "\n")

# ---------------- Step 11: CI Width ----------------
df_obesity['CI_Width'] = df_obesity['UpperBound'] - df_obesity['LowerBound']
df_malnutrition['CI_Width'] = df_malnutrition['UpperBound'] - df_malnutrition['LowerBound']
print("Step 11: CI Width calculated")
print("Obesity:")
print(df_obesity[['LowerBound','UpperBound','CI_Width']].head(), "\n")
print("Malnutrition:")
print(df_malnutrition[['LowerBound','UpperBound','CI_Width']].head(), "\n")

# ---------------- Step 12: Obesity & Malnutrition levels ----------------
df_obesity['obesity_level'] = df_obesity['Mean_Estimate'].apply(lambda x: 'High' if x >=30 else 'Moderate' if 25<=x<=29.9 else 'Low')
df_malnutrition['malnutrition_level'] = df_malnutrition['Mean_Estimate'].apply(lambda x: 'High' if x>=20 else 'Moderate' if 10<=x<=19.9 else 'Low')
print("Step 12: Levels assigned")
print("Obesity:")
print(df_obesity[['Mean_Estimate','obesity_level']].head(), "\n")
print("Malnutrition:")
print(df_malnutrition[['Mean_Estimate','malnutrition_level']].head(), "\n")

# ---------------- Step 13: Save CSV ----------------
df_obesity.to_csv("df_obesity_clean.csv", index=False)
df_malnutrition.to_csv("df_malnutrition_clean.csv", index=False)
print("Step 13: CSVs saved. Data cleaning complete!")