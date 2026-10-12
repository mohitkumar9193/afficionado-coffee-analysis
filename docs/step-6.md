# Step 6: category, product-type, and store performance

Implemented in src/categories.py and integrated into dashboard/app.py.

## Outputs

Category revenue distribution and largest-category share; product-type contributions within each category; store revenue and unit totals; category mix by store with revenue/unit-share selector and heatmap; product-type mix within each store/category. Summaries can be downloaded as CSV.

## Definitions

Revenue = sum of eligible transaction quantity × unit price. Category revenue share uses total filtered revenue. A type's within-category revenue share uses its category's filtered revenue. Store category shares use that store's filtered revenue or units. Store/type shares use that store and category's filtered revenue or units. All sidebar filters apply; Top-N does not restrict these summaries.

Category and product type are grouped together, so identical type names in different categories do not merge. Store comparison uses store_location as specified in the brief; inspect store_id/location mappings when real data arrives. Category labels come directly from eligible rows; inconsistent product metadata remains flagged by the product module.

## Interpretation

The largest category share measures dependency in the selected scope. Filtering to a single category yields 100% by construction. There is no unsupported high-risk threshold. Store sales mix is an observed pattern, not proof of preference: stock availability, prices, store traffic, and dataset coverage must be considered. No real-data category or store findings are claimed yet.

## Verification

Synthetic fixtures test reconciliation, distinct category/type pairs, overall versus parent denominators, store revenue/unit mix, filtered scopes, and empty inputs. Calculation tests and Python compilation pass. The interactive UI has not been runtime-tested because Streamlit, pandas, and Plotly are not installed in the current Python environment.

## Run

Follow the environment setup in docs/step-5.md, then run `python -m streamlit run dashboard/app.py` from the project root and upload the actual CSV or XLSX dataset.

