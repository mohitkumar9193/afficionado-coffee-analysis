# Public educational case study

Source: https://mavenanalytics.io/data-playground/coffee-shop-sales

Publisher: Maven Analytics. License stated by publisher: Public Domain.
Maven Roasters is fictional. This dataset does not contain actual Afficionado sales.
Period: 2023-01-01 through 2023-06-30. Downloaded 12 October 2026.

The gzip CSV contains all 149,116 source rows, preserves the 11 source fields,
formats dates as ISO dates and adds year derived from transaction_date.
No rows were excluded or values corrected. Balance is absent and not invented.
The original XLSX remains available from the publisher ZIP.

Source archive SHA256: be13c59c4cfdc0d1b08ceab514aea50a0cd329c916e4c3585eeef92a5b4c3a2c
Bundled gzip SHA256: e5de8d073fd865b14a8053b7307c3f492a0b9a13ccc316ca8176a404a992e20c

Reproduce: python analysis/run_case_study.py path/to/Coffee-Shop-Sales.zip
The runner reconciles the application summaries to independent integer-cent controls.

