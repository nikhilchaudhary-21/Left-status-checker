import pandas as pd
import re

# ====================== CONFIG ======================
file_path = 'Left_1.csv'                  # path to your input file
output_file = 'Left_status_final.csv'     # output file name
# ===================================================

df = pd.read_csv(file_path, encoding='utf-8')

# Clean column names (remove leading/trailing whitespace)
df.columns = df.columns.str.strip()

print("Columns in file:", df.columns.tolist())
print("\nFirst few rows:\n", df.head(2))
print("-" * 80)

person_col = 'Personal Linkedin Url'
company_col = 'Company'
time_col = 'Time Period'

# ---- Normalize company names ----
def normalize_company(name):
    if pd.isna(name):
        return ''
    name = str(name).lower()
    name = re.sub(r'[^a-z0-9\s]', '', name)  # remove special characters (brackets, dots, etc.)
    name = ' '.join(name.split())             # remove extra spaces
    return name

df['company_normalized'] = df[company_col].apply(normalize_company)

# Step 1: Check each row for "Present" in the time period
df['has_present'] = df[time_col].astype(str).str.contains('Present', case=False, na=False)

# Step 2: Build a mapping of person -> set of normalized company names where they are currently "Present"
person_present_companies = (
    df[df['has_present']]
    .groupby(person_col)['company_normalized']
    .apply(set)
    .to_dict()
)

# Step 3: Check if a given row's company matches any of the person's current "Present" companies
# Uses partial matching — e.g. "bitterpower gmbh" matches "bitterpower gmbh bitterliebe"
def check_still_here(row):
    person = row[person_col]
    comp = row['company_normalized']
    present_comps = person_present_companies.get(person, set())

    for pc in present_comps:
        if not pc or not comp:
            continue
        # Exact match or partial match (one string contained within the other)
        if pc == comp or pc in comp or comp in pc:
            return True

    return False

df['still_here'] = df.apply(check_still_here, axis=1)

# Step 4: Assign final status label to each row
df['Status'] = df['still_here'].map({
    True: 'Present in same company',
    False: 'Left the company'
})

# Step 5: Mark rows where the person is currently active (has "Present" in time period)
df['Is_Current_Role'] = df['has_present']

# Drop temporary working columns
df = df.drop(columns=['has_present', 'still_here', 'company_normalized'])

# Save the result
df.to_csv(output_file, index=False, encoding='utf-8')

print(f"\nDone! Output file saved: {output_file}")
print(f"Total Rows: {len(df)}")

# ---- Spot-check: verify a known edge case (Tammo) ----
# All rows for this person should show 'Present in same company'
tammo = df[df[person_col].str.contains('tammo', case=False, na=False)]
if not tammo.empty:
    print("\nTammo rows (all should be 'Present in same company'):")
    print(tammo[[person_col, time_col, company_col, 'Status', 'Is_Current_Role']].to_string(index=False))
else:
    print("\nNo rows found for 'Tammo' in this file.")

# ---- Print summary ----
print("\n--- Summary ---")
print(df['Status'].value_counts().to_string())
