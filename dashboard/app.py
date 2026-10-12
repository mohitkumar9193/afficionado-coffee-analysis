"""Run from repository root: python -m streamlit run dashboard/app.py."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
from src.products import REQUIRED, prepare, summarize
from src.categories import category_performance
from src.concentration import concentration
from src.recommendations import evaluate
from src.demo import demo_records

st.set_page_config(page_title='Afficionado | Product Intelligence', page_icon='☕', layout='wide')
st.title('☕ Afficionado Coffee Roasters')
st.caption('Product Optimization & Revenue Contribution Analysis')
st.write('Explore product performance, category dependency, and opportunities to improve the menu.')
st.sidebar.title('Analysis workspace')

upload = st.sidebar.file_uploader('Upload transaction data', type=['csv', 'xlsx'])
demo_mode = st.sidebar.checkbox('Explore synthetic demonstration data', value=False)
st.sidebar.caption('CSV or Excel. Uploads are analyzed in this session and are not saved to the project.')
if upload is None and not demo_mode:
    st.info('Upload your transaction dataset to begin. No sample sales or fabricated findings are displayed.')
    st.write('Required analysis columns: ' + ', '.join(REQUIRED))
    st.stop()

try:
    if demo_mode:
        st.warning('DEMONSTRATION ONLY — all records and results below are synthetic. They are not Afficionado sales or research findings.')
        frame = pd.DataFrame(demo_records())
    elif upload.name.lower().endswith('.csv'):
        frame = pd.read_csv(upload, dtype=str, keep_default_na=False)
    else:
        workbook = pd.ExcelFile(upload, engine='openpyxl')
        sheet = st.sidebar.selectbox('Worksheet', workbook.sheet_names)
        frame = pd.read_excel(workbook, sheet_name=sheet, dtype=str, keep_default_na=False)
    frame.columns = [str(c).strip().lower() for c in frame.columns]
    if frame.columns.duplicated().any():
        raise ValueError('Column names must be unique after trimming and lowercasing.')
    missing = sorted(set(REQUIRED) - set(frame.columns))
    if missing:
        raise ValueError('Missing required columns: ' + ', '.join(missing))
    clean, issues = prepare(frame.to_dict('records'))
except Exception as error:
    st.error(f'Unable to analyze this file: {error}')
    st.stop()

with st.expander('Data validation and analysis scope', expanded=bool(issues)):
    st.write(f'{len(frame):,} source rows · {len(clean):,} eligible rows · {len(issues):,} excluded rows')
    st.caption('Only positive whole-number quantities and positive finite prices are included. Duplicate rows are retained until transaction granularity is confirmed. Balance is not used as revenue. High values are retained for review.')
    if issues:
        st.dataframe(pd.DataFrame(issues), width='stretch')
        st.download_button('Download exclusion log', pd.DataFrame(issues).to_csv(index=False), 'exclusion-log.csv', 'text/csv')
if not clean:
    st.warning('No eligible transaction rows. Review the validation log.')
    st.stop()

st.sidebar.subheader('Filter scope')
if st.sidebar.button('Reset filters'):
    for filter_key in ('filter_store_location', 'filter_product_category', 'filter_product_type'):
        st.session_state.pop(filter_key, None)
selected = clean
for field, label in [('store_location', 'Store location'), ('product_category', 'Category'), ('product_type', 'Product type')]:
    options = sorted({r[field] for r in selected})
    filter_key = 'filter_' + field
    if filter_key in st.session_state:
        st.session_state[filter_key] = [value for value in st.session_state[filter_key] if value in options]
    choices = st.sidebar.multiselect(label, options, default=None if filter_key in st.session_state else options, key=filter_key)
    selected = [r for r in selected if r[field] in choices]
if not selected:
    st.info('No records match your filters. Select at least one value for each filter.')
    st.stop()

products = pd.DataFrame(summarize(selected))
count = len(products)
top_n = st.sidebar.slider('Top / bottom N products', 1, count, min(10, count)) if count > 1 else 1
metric = st.sidebar.radio('Rank products by', ['Units sold', 'Revenue'])
sort_field = 'units_sold' if metric == 'Units sold' else 'revenue'
total_revenue = products.revenue.sum()
cards = st.columns(4)
cards[0].metric('Total revenue', f'{total_revenue:,.2f}', help='Computed quantity × unit price, in the dataset currency.')
cards[1].metric('Units sold', f'{products.units_sold.sum():,}')
cards[2].metric('Products sold', count)
cards[3].metric('Top-N revenue share', f'{products.nlargest(top_n, "revenue").revenue.sum() / total_revenue * 100:.1f}%')
section = st.sidebar.radio('Dashboard view', ['Products', 'Categories & stores', 'Pareto & menu balance', 'Recommendations', 'Product drill-down'])
st.caption('Overall revenue shares use the full filtered dataset as their denominator. Nested shares are labeled separately. Top-N does not change these denominators. Revenue is not profit.')

if section == 'Products':
    left, right = st.columns(2)
    for column, ascending, title in [(left, False, 'Top-selling products' if metric == 'Units sold' else 'Top revenue products'), (right, True, 'Least-selling observed products' if metric == 'Units sold' else 'Lowest revenue observed products')]:
        ranked = products.sort_values([sort_field, 'product_id'], ascending=[ascending, True]).head(top_n).copy()
        ranked['product_label'] = ranked.product_detail + ' [' + ranked.product_id + ']'
        chart = px.bar(ranked, x=sort_field, y='product_label', orientation='h', hover_data=['revenue_share_pct', 'units_sold', 'revenue'], title=title, color_discrete_sequence=['#94643d'])
        chart.update_layout(yaxis={'categoryorder': 'total ascending'}, xaxis_title=metric, yaxis_title=None)
        column.plotly_chart(chart, width='stretch')

    st.subheader('Popularity versus revenue')
    scatter = px.scatter(products, x='units_sold', y='revenue', color='product_category', hover_name='product_detail', hover_data=['product_id', 'volume_rank', 'revenue_rank', 'average_selling_price', 'revenue_share_pct'])
    scatter.update_layout(xaxis_title='Units sold', yaxis_title='Revenue (dataset currency)')
    st.plotly_chart(scatter, width='stretch')

    st.subheader('Volume and revenue rank comparison')
    st.caption('A positive rank gap means a product ranks better by volume than by revenue. Equal values share a rank; Top-N ties are ordered by product ID.')
    st.dataframe(products, width='stretch', hide_index=True)
    st.download_button('Download product summary', products.to_csv(index=False), 'product-performance.csv', 'text/csv')

    st.subheader('Products to investigate')
    median_volume = products.units_sold.median()
    median_price = products.average_selling_price.median()
    popular = products[(products.units_sold >= median_volume) & (products.rank_gap > 0)]
    premium = products[(products.average_selling_price > median_price) & (products.units_sold < median_volume)]
    st.write('Popular products with a lower revenue ranking')
    st.dataframe(popular, hide_index=True, width='stretch')
    st.write('Above-median selling price with below-median unit sales')
    st.dataframe(premium, hide_index=True, width='stretch')
    st.caption('These are transparent screening rules, not removal recommendations. Units measure popularity; sales rows are not confirmed purchase frequency. Zero-selling products require a complete menu catalog.')
    if products.metadata_conflict.any():
        st.warning('Some product IDs have inconsistent descriptions, categories, or types. Review these before drawing conclusions.')



if section == 'Categories & stores':
    st.divider()
    st.header('Category, product-type & store performance')
    st.caption('All eligible categories are included. These views follow the sidebar filters and are unaffected by Top-N.')
    performance = category_performance(selected)
    categories = pd.DataFrame(performance['categories'])
    types = pd.DataFrame(performance['types'])
    stores = pd.DataFrame(performance['stores'])
    store_categories = pd.DataFrame(performance['store_categories'])
    store_types = pd.DataFrame(performance['store_types'])
    leader = categories.iloc[0]
    st.metric('Largest category revenue share', f'{leader.revenue_share_pct:.1f}%', help='Largest category revenue divided by total revenue in the filtered scope.')
    st.write(f'Leading category in the selected scope: **{leader.product_category}**. Equal shares may produce multiple leaders; see the full table.')
    category_tab, type_tab, store_tab = st.tabs(['Category distribution', 'Types within categories', 'Store comparison'])

    with category_tab:
        chart = px.bar(categories, x='product_category', y='revenue_share_pct', hover_data=['revenue', 'units_sold', 'products_sold'], color='product_category')
        chart.update_layout(xaxis_title='Category', yaxis_title='Share of filtered revenue (%)', showlegend=False)
        st.plotly_chart(chart, width='stretch')
        st.dataframe(categories.drop(columns=['parent_revenue_share_pct', 'parent_unit_share_pct']), hide_index=True, width='stretch')
        st.download_button('Download category summary', categories.to_csv(index=False), 'category-performance.csv', 'text/csv')

    with type_tab:
        focus = st.selectbox('Explore category', sorted(categories.product_category.tolist()))
        nested = types[types.product_category == focus].rename(columns={'parent_revenue_share_pct': 'within_category_revenue_pct', 'parent_unit_share_pct': 'within_category_units_pct'})
        chart = px.bar(nested, x='product_type', y='within_category_revenue_pct', hover_data=['revenue', 'units_sold', 'revenue_share_pct'], color_discrete_sequence=['#94643d'])
        chart.update_layout(xaxis_title='Product type', yaxis_title='Share of selected category revenue (%)')
        st.plotly_chart(chart, width='stretch')
        st.dataframe(nested, hide_index=True, width='stretch')
        st.caption('Within-category shares sum to 100% within the selected category and active filters. Revenue share uses total filtered revenue.')
        st.download_button('Download all category and type summaries', types.to_csv(index=False), 'product-type-performance.csv', 'text/csv')

    with store_tab:
        st.dataframe(stores.drop(columns=['parent_revenue_share_pct', 'parent_unit_share_pct']), hide_index=True, width='stretch')
        mix_measure = st.radio('Compare category mix using', ['Revenue share', 'Unit share'], horizontal=True)
        mix_column = 'parent_revenue_share_pct' if mix_measure == 'Revenue share' else 'parent_unit_share_pct'
        chart = px.bar(store_categories, x='store_location', y=mix_column, color='product_category', barmode='stack', hover_data=['revenue', 'units_sold'])
        chart.update_layout(xaxis_title='Store location', yaxis_title=f'{mix_measure} within each store (%)')
        st.plotly_chart(chart, width='stretch')
        heat = store_categories.pivot(index='product_category', columns='store_location', values=mix_column).fillna(0)
        st.plotly_chart(px.imshow(heat, text_auto='.1f', aspect='auto', labels={'color': f'{mix_measure} (%)'}, color_continuous_scale='YlOrBr'), width='stretch')
        st.caption('A missing category/store combination is shown as zero in this filtered dataset. Differences in sales mix suggest patterns to investigate; inventory, availability, pricing, traffic, and coverage can also explain them. A single selected store cannot support a cross-store comparison.')
        st.write('Product-type mix within each store and category')
        st.dataframe(store_types.rename(columns={'parent_revenue_share_pct': 'within_store_category_revenue_pct', 'parent_unit_share_pct': 'within_store_category_units_pct'}), hide_index=True, width='stretch')
        st.download_button('Download store category mix', store_categories.to_csv(index=False), 'store-category-performance.csv', 'text/csv')
        st.download_button('Download store product-type mix', store_types.to_csv(index=False), 'store-type-performance.csv', 'text/csv')



if section == 'Pareto & menu balance':
    st.divider()
    st.header('Revenue concentration & menu balance')
    pareto_result = concentration(selected, top_n)
    pareto = pd.DataFrame(pareto_result['products'])
    concentration_metrics = pareto_result['metrics']
    concentration_cards = st.columns(4)
    concentration_cards[0].metric('Products to 80%', concentration_metrics['products_to_80'], help='Minimum revenue-ordered product count reaching at least 80% of filtered revenue.')
    concentration_cards[1].metric('Menu share to 80%', f"{concentration_metrics['products_to_80_pct']:.1f}%", help='Products needed for 80% divided by the distinct sold products in the active scope.')
    concentration_cards[2].metric(f'Top {top_n} revenue share', f"{concentration_metrics['top_n_revenue_pct']:.1f}%")
    concentration_cards[3].metric('Long-tail revenue share', f"{concentration_metrics['tail_revenue_pct']:.1f}%")
    st.caption('Products are ordered by revenue across the full filtered scope. The first product crossing 80% is included. Top-N changes only the concentration ratio, not the Pareto population.')

    figure = make_subplots(specs=[[{'secondary_y': True}]])
    figure.add_trace(go.Bar(x=pareto.revenue_order, y=pareto.revenue, name='Product revenue',
                            marker_color=['#94643d' if s == 'Revenue anchor' else '#c9c3b9' for s in pareto.segment],
                            customdata=pareto[['product_id', 'product_detail']].values,
                            hovertemplate='%{customdata[1]} [%{customdata[0]}]<br>Revenue: %{y:,.2f}<extra></extra>'), secondary_y=False)
    figure.add_trace(go.Scatter(x=pareto.revenue_order, y=pareto.cumulative_revenue_pct, name='Cumulative revenue (%)', mode='lines+markers', line_color='#315b74'), secondary_y=True)
    figure.add_trace(go.Scatter(x=[1, len(pareto)], y=[80, 80], name='80% threshold', mode='lines', line={'dash': 'dash', 'color': '#777'}), secondary_y=True)
    figure.update_xaxes(title_text='Products ordered by revenue (highest first)', dtick=1 if len(pareto) <= 20 else None)
    figure.update_yaxes(title_text='Revenue (dataset currency)', secondary_y=False)
    figure.update_yaxes(title_text='Cumulative revenue (%)', range=[0, 105], secondary_y=True)
    st.plotly_chart(figure, width='stretch')
    st.write(f"The top {concentration_metrics['top_20_product_count']} products (20% of observed products, rounded up) contribute {concentration_metrics['top_20_revenue_pct']:.1f}% of filtered revenue.")
    if concentration_metrics['boundary_tie']:
        st.info('Equal-revenue products straddle the 80% boundary. Product ID breaks the tie for the minimum-count calculation; anchor status does not distinguish their performance.')
    anchor_tab, tail_tab = st.tabs(['Revenue anchors', 'Long-tail products'])
    with anchor_tab:
        st.caption('The smallest revenue-ordered set reaching at least 80% of filtered revenue.')
        st.dataframe(pareto[pareto.segment == 'Revenue anchor'], hide_index=True, width='stretch')
    with tail_tab:
        st.caption('Products remaining after the 80% boundary. Membership alone does not justify removal; review individual shares, costs, availability, and strategic role.')
        st.dataframe(pareto[pareto.segment == 'Long tail'], hide_index=True, width='stretch')
    st.download_button('Download Pareto analysis', pareto.to_csv(index=False), 'revenue-concentration.csv', 'text/csv')
    st.caption('This describes concentration within sold products and active filters. It does not establish a complete menu inventory, profit concentration, or a causal diversification risk score.')



if section == 'Recommendations':
    st.divider()
    st.header('KPIs & recommended actions')
    assessment = evaluate(selected, top_n)
    kpi_values = assessment['kpis']
    st.metric('Product Efficiency Score · revenue per SKU', f"{kpi_values['revenue_per_sku']:,.2f}", help='Total filtered revenue divided by distinct sold product IDs. Dataset currency per SKU; this is not margin or operating efficiency.')
    with st.expander('The five KPI formulas', expanded=True):
        st.dataframe(pd.DataFrame(assessment['formulas']), hide_index=True, width='stretch')
        st.caption('Product contribution and volume are shown in the product summary; category shares in the category summary; CR-N in the concentration cards. Revenue per SKU is shown above. All use the active filters; Top-N affects CR-N only.')
    recommendations = pd.DataFrame(assessment['recommendations'])
    st.write('Product action plan')
    st.caption('Comparisons use product medians within the active filters. Rules are exclusive and applied in priority order: data review, insufficient scope, hero, promotion, revenue yield review, redesign review, monitor. Hero candidates exceed median units and revenue and belong to the 80% anchor set. Promotion candidates have below-median units, above-median selling price, and at-least-median revenue. Review/redesign candidates are below both medians and in the long tail.')
    labels = sorted(recommendations.recommendation.unique().tolist())
    chosen_labels = st.multiselect('Show recommendation groups', labels, default=labels)
    visible_recommendations = recommendations[recommendations.recommendation.isin(chosen_labels)]
    st.dataframe(visible_recommendations[['product_id', 'product_detail', 'recommendation', 'evidence', 'suggested_action']], hide_index=True, width='stretch')
    st.download_button('Download complete product action plan', recommendations.to_csv(index=False), 'product-recommendations.csv', 'text/csv')
    with st.expander('Evidence required before menu removal'):
        st.write('Verify product cost and margin, stock availability, comparable sales exposure, menu completeness, preparation effort, customer feedback, and strategic role. Trial changes and assess their effect before a permanent decision. Revenue-only data does not justify automatic removal.')
        st.caption('Current suggestions are revenue-based screening outputs, not proven interventions. There are no actual business findings until real transaction data is supplied and validated.')


if section == 'Product drill-down':
    st.header('Product drill-down')
    names = {r.product_id: f'{r.product_detail} [{r.product_id}]' for r in products.itertuples()}
    product_id = st.selectbox('Choose a product', sorted(names), format_func=lambda value: names[value])
    detail = products[products.product_id == product_id].iloc[0]
    columns = st.columns(4)
    columns[0].metric('Units sold', f'{detail.units_sold:,}')
    columns[1].metric('Revenue', f'{detail.revenue:,.2f}')
    columns[2].metric('Revenue contribution', f'{detail.revenue_share_pct:.2f}%')
    columns[3].metric('Average selling price', f'{detail.average_selling_price:,.2f}')
    st.caption(f'Volume rank: {detail.volume_rank} · Revenue rank: {detail.revenue_rank}. Contribution uses all filtered products as its denominator.')
    product_rows = [r for r in selected if r['product_id'] == product_id]
    by_store = pd.DataFrame(category_performance(product_rows)['stores'])
    chart = px.bar(by_store, x='store_location', y='revenue', hover_data=['units_sold'], color_discrete_sequence=['#94643d'])
    chart.update_layout(xaxis_title='Store location', yaxis_title='Product revenue (dataset currency)')
    st.plotly_chart(chart, width='stretch')
    st.dataframe(by_store, hide_index=True, width='stretch')
    st.caption('Shares in the store table are within this product, across selected stores.')
    action = next(r for r in evaluate(selected, top_n)['recommendations'] if r['product_id'] == product_id)
    st.info(action['recommendation'] + ': ' + action['suggested_action'])
    transaction_view = pd.DataFrame([{k: float(v) if k in ('price', 'revenue') else v for k,v in row.items()} for row in product_rows])
    with st.expander('Eligible source rows for this product'):
        st.dataframe(transaction_view, hide_index=True, width='stretch')
    st.download_button('Download product source rows', transaction_view.to_csv(index=False), 'product-drilldown.csv', 'text/csv')

st.divider()
st.caption('Afficionado · Product intelligence | Revenue = quantity × unit price | ' + ('Synthetic demonstration results — not business findings.' if demo_mode else 'Uploaded data is retained only in the active session.'))

