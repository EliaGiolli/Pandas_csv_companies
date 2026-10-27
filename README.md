# Tech Companies Cleanup (Python + pandas)

A small data-cleaning script I wrote to turn my hand-made spreadsheet of tech companies around Pisa, Empoli and Navacchio into a clean list of the ones I can actually contact for a job application.

## What it does

Starting from `aziende_tech.csv` (33 rows × 26 columns, exported from a spreadsheet), `main.py`:

1. **Drops empty columns.** Spreadsheet leftovers (`Colonna 1` … `Colonna 19`) are removed: 26 → 7 columns.
2. **Drops near-empty rows.** Rows with fewer than 4 non-empty values are discarded (e.g. a half-filled "Digital Hub" row): 33 → 32 rows.
3. **Normalizes `Tipo struttura`.** Values are stripped and lowercased, then the spelling variants are grouped into three categories with a mapping dictionary:
   - `System integrator`
   - `Sviluppo software`
   - `Riparazioni hardware e software`
4. **Adds two boolean columns:** `ha_email` and `ha_pagina_carriere`, true when the company has a contact and a "Lavora con noi" link.
5. **Cleans the careers URLs** by cutting everything after `?`, which removes tracking parameters such as `_gl=...`.
6. **Exports** only the companies with an email or a careers page (28 of 32), without my private `Pensieri` (notes) column, as a zipped CSV.

## Usage

```bash
pip install pandas
python main.py
```

Put `aziende_tech.csv` in the same folder as `main.py`. The script prints the shape of the data before and after the cleanup, then the table it exports, and writes `companies_clean.zip`.

Tested with Python 3 and pandas 3.0.

## Files

| File | Description |
| --- | --- |
| `main.py` | the cleaning script |
| `aziende_tech.csv` | input data |
| `companies_clean.zip` | output: companies to contact, as CSV (generated) |

## Pandas features used

`read_csv`, `dropna` (`axis`, `how`, `thresh`), the `.str` accessor (`strip`, `lower`, `split`, `capitalize`), `replace` with a mapping dict, boolean columns with `notna`, boolean filtering, `drop` and `to_csv` with zip compression.

## Known limitations

- The category mapping is written by hand. A new spelling of `Tipo struttura` is left unmapped, so check the output (a commented-out `value_counts` line in the script helps with that).
- `Azienda informatica` is mapped to `System integrator`, which is a simplification: those companies do more than one thing.
- `Contatto` sometimes holds a website instead of an email, or two emails in one cell, so `ha_email` means "has a contact", not "has a valid email address".