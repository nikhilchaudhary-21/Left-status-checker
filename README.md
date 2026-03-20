# Left Status Checker

A Python script that analyzes LinkedIn job history data from a CSV file and determines whether each person is **still at the same company** or has **left**.

---

## What It Does

For each row in the input CSV, the script:

1. Detects whether the job entry is a **current role** (i.e., the time period contains "Present")
2. Builds a per-person set of their **current companies**
3. Compares every past/present job entry against those current companies using **partial name matching**
4. Labels each row with a `Status` — either `Present in same company` or `Left the company`
5. Adds an `Is_Current_Role` boolean flag for rows explicitly showing an active role

---

## Input Requirements

A CSV file with at least these three columns:

| Column | Description |
|---|---|
| `Personal Linkedin Url` | Unique identifier per person |
| `Company` | Company name for that job entry |
| `Time Period` | Employment dates (must contain `"Present"` for current roles) |

**Example rows:**

```
Personal Linkedin Url,Company,Time Period
https://linkedin.com/in/john,Acme Corp,Jan 2020 - Present
https://linkedin.com/in/john,Old Co,Jan 2018 - Dec 2019
```

---

## Output

A new CSV (`Left_status_final.csv`) with two additional columns appended:

| Column | Values | Description |
|---|---|---|
| `Status` | `Present in same company` / `Left the company` | Whether the person is still at this company |
| `Is_Current_Role` | `True` / `False` | Whether this specific row is their active/current role |

---

## Configuration

Edit these two lines at the top of the script:

```python
file_path = 'Left_1.csv'               # Path to your input CSV
output_file = 'Left_status_final.csv'  # Path for the output CSV
```

---

## How the Matching Works

Company names are **normalized** before comparison:
- Converted to lowercase
- Special characters removed (brackets, dots, dashes, etc.)
- Extra whitespace collapsed

Matching uses **partial string containment**, not just exact equality. This handles cases like:

| Stored as | Current role listed as | Result |
|---|---|---|
| `bitterpower gmbh` | `bitterpower gmbh bitterliebe` | ✅ Match |
| `acme corp` | `acme corp.` | ✅ Match |
| `old company` | `new company` | ❌ No match |

This is intentional — LinkedIn profiles sometimes list a parent company or a slightly different name for the same employer.

---

## Requirements

```
pandas
```

Install with:

```bash
pip install pandas
```

---

## Usage

```bash
python Left_status_checker.py
```

The script will print:
- Column names and a preview of the data
- A spot-check for a specific test case (Tammo)
- A summary count of `Present in same company` vs `Left the company`

---

## Notes

- The `Personal Linkedin Url` column is used as the unique person identifier — make sure it's consistent across rows for the same individual.
- The "Present" check is **case-insensitive**.
- If a person has no "Present" role at all, **all** their rows will be marked `Left the company`.
