import pdfplumber
import pandas as pd

pdf_path = 'data/list.pdf'
# Let's use a safer approach to extract tables and construct the DataFrame
all_data = []

with pdfplumber.open(pdf_path) as pdf:
    # Extract headers from page 6
    headers = pdf.pages[5].extract_tables()[0][0]

    # Iterate over pages starting from page 6 to the end
    for page_num in range(5, 155):
        page = pdf.pages[page_num]
        tables = page.extract_tables()

        for table in tables:
            # If it's page 6, skip the header row, else consider all rows as data rows
            start_row = 1 if page_num == 5 else 0
            for row in table[start_row:]:
                all_data.append(row)

# Convert the data into a DataFrame using the extracted headers
df_all_tables = pd.DataFrame(all_data, columns=headers)
df_all_tables['ages'] = df_all_tables.iloc[:, -1].apply(lambda x: 0 if not str(x).isnumeric() else int(x))
df_all_tables.head()

df_all_tables.to_csv('data/list.csv', index=False, encoding='utf-8')