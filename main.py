import pandas as pd

companies_csv = pd.read_csv('aziende_tech.csv')

print(f"Initial count: {companies_csv.shape}")
# New dataset without empty columns
new_dataset = companies_csv.dropna(axis=1, how='all')
print(f"Before: {companies_csv.shape} → After: {new_dataset.shape}")

# Keep only rows with at least N non-empty values (drops near-empty rows like "Digital Hub")
companies_clean = new_dataset.dropna(axis=0, thresh=4)

# 1. Normalize text
tipo = companies_clean['Tipo struttura'].str.strip().str.lower()

# 2. Group variants into your categories (keys = lowercase variants)
categories = {
    'azienda informatica': 'System integrator',
    'sviluppo software': 'Sviluppo Software',
    'informatica e servizi':'Riparazioni hardware e software',
    'assistenza computer':'Riparazioni hardware e software',
    'azienda informatica x settore bancario':'System integrator',
    'system integrator/ azienda informatica': 'System integrator',
    'software house (gestionali)': 'Sviluppo Software',
    'software house':'Sviluppo Software',
}
companies_clean['Tipo struttura'] = tipo.replace(categories).str.capitalize()


# 3. Check nothing slipped through
# print(companies_clean['Tipo struttura'].value_counts(dropna=False))
# Add two more series from scratch
companies_clean['ha_email'] = companies_clean['Contatto'].notna()
companies_clean['ha_pagina_carriere'] = companies_clean['Link "Lavora con noi"'].notna()

# Polish urls
col = 'Link "Lavora con noi"'
# Split divides the url in two chunks without '?' and then it rebuilds the url
companies_clean[col] = companies_clean[col].str.split('?').str[0]

# Export a 'clean' CSV with the companies I want to contact to apply
compression_opts = dict(
    method='zip',
    archive_name='companies_clean.zip',
)
dataset_without_thoughts = companies_clean[companies_clean['ha_email'] | companies_clean['ha_pagina_carriere']].drop(columns=['Pensieri'])
dataset_without_thoughts.to_csv(
    'companies_clean.zip',
    index=False,
    compression=compression_opts
)
print(f'Il file che verrà esportato è: {dataset_without_thoughts}')