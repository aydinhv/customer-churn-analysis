import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import numpy as np

# Sample Data Preparation
from faker import Faker
fake = Faker()

np.random.seed(42)
num_customers = 1000
data = {
    'customer_id': range(1, num_customers + 1),
    'gender': np.random.choice(['Male', 'Female'], num_customers),
    'senior_citizen': np.random.choice([0, 1], num_customers),
    'partner': np.random.choice(['Yes', 'No'], num_customers),
    'dependents': np.random.choice(['Yes', 'No'], num_customers),
    'tenure': np.random.randint(1, 73, num_customers),
    'phone_service': np.random.choice(['Yes', 'No'], num_customers),
    'multiple_lines': np.random.choice(['Yes', 'No', 'No phone service'], num_customers),
    'internet_service': np.random.choice(['DSL', 'Fiber optic', 'No'], num_customers),
    'online_security': np.random.choice(['Yes', 'No', 'No internet service'], num_customers),
    'online_backup': np.random.choice(['Yes', 'No', 'No internet service'], num_customers),
    'device_protection': np.random.choice(['Yes', 'No', 'No internet service'], num_customers),
    'tech_support': np.random.choice(['Yes', 'No', 'No internet service'], num_customers),
    'streaming_tv': np.random.choice(['Yes', 'No', 'No internet service'], num_customers),
    'streaming_movies': np.random.choice(['Yes', 'No', 'No internet service'], num_customers),
    'contract': np.random.choice(['Month-to-month', 'One year', 'Two year'], num_customers),
    'paperless_billing': np.random.choice(['Yes', 'No'], num_customers),
    'payment_method': np.random.choice(['Electronic check', 'Mailed check', 'Bank transfer (automatic)', 'Credit card (automatic)'], num_customers),
    'monthly_charges': np.round(np.random.uniform(18.25, 118.75, num_customers), 2),
    'total_charges': lambda x: np.round(x['monthly_charges'] * x['tenure'] * np.random.uniform(0.8, 1.2), 2),
    'churn': np.random.choice(['Yes', 'No'], num_customers)
}

df = pd.DataFrame(data)
df['total_charges'] = df.apply(data['total_charges'], axis=1)

# Additional Data Preparation
df_churn_contract = df.groupby('contract').agg(
    total_customers=pd.NamedAgg(column='customer_id', aggfunc='count'),
    churned_customers=pd.NamedAgg(column='churn', aggfunc=lambda x: (x == 'Yes').sum())
).reset_index()

df_avg_charges_internet = df.groupby('internet_service').agg(
    avg_monthly_charges=pd.NamedAgg(column='monthly_charges', aggfunc='mean')
).reset_index()

df_tenure_distribution = df.groupby('tenure').agg(
    customer_count=pd.NamedAgg(column='customer_id', aggfunc='count')
).reset_index()

# Customer Demographics Analysis
fig_gender_distribution = px.pie(
    df,
    names='gender',
    title='Gender Distribution',
    color='gender'
)

fig_senior_citizen_distribution = px.pie(
    df,
    names='senior_citizen',
    title='Senior Citizen Distribution',
    labels={'senior_citizen': 'Senior Citizen'},
    color='senior_citizen'
)

# Service Usage Patterns
fig_multiple_lines_usage = px.bar(
    df,
    x='multiple_lines',
    title='Multiple Lines Usage',
    labels={'multiple_lines': 'Multiple Lines Usage'},
    color='multiple_lines'
)

fig_internet_service_types = px.pie(
    df,
    names='internet_service',
    title='Internet Service Types',
    color='internet_service'
)

# Payment Method Preferences
fig_payment_methods = px.pie(
    df,
    names='payment_method',
    title='Payment Method Preferences',
    color='payment_method'
)

# Churn Rate by Contract Type (Pie Chart)
fig_churn_contract_pie = px.pie(
    df_churn_contract,
    names='contract',
    values='churned_customers',
    title='Churn Rate by Contract Type',
    color='contract'
)

# Average Monthly Charges by Internet Service Type (Line Chart)
fig_avg_charges_internet_line = px.line(
    df_avg_charges_internet,
    x='internet_service',
    y='avg_monthly_charges',
    title='Average Monthly Charges by Internet Service Type',
    markers=True,
    line_shape='spline'
)

# Distribution of Tenure (Box Plot)
fig_tenure_distribution_box = px.box(
    df,
    x='tenure',
    y='monthly_charges',
    color='churn',
    title='Distribution of Tenure vs Monthly Charges',
    points='all'
)

# Churn vs Monthly Charges Scatter Plot (Enhanced)
fig_churn_monthly_enhanced = px.scatter(
    df,
    x='monthly_charges',
    y='total_charges',
    color='churn',
    title='Churn vs Monthly Charges',
    labels={'monthly_charges': 'Monthly Charges', 'total_charges': 'Total Charges'},
    hover_data=['tenure', 'contract', 'payment_method'],
    size='tenure',
    size_max=15
)

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the app layout
app.layout = html.Div([
    html.H1("Customer Churn Analysis Dashboard"),
    
    dcc.Tabs([
        dcc.Tab(label='Churn Rate by Contract Type', children=[
            dcc.Graph(id='churn-contract-graph', figure=fig_churn_contract_pie)
        ]),
        dcc.Tab(label='Avg Monthly Charges by Internet Service Type', children=[
            dcc.Graph(id='avg-charges-internet-graph', figure=fig_avg_charges_internet_line)
        ]),
        dcc.Tab(label='Distribution of Tenure vs Monthly Charges', children=[
            dcc.Graph(id='tenure-distribution-graph', figure=fig_tenure_distribution_box)
        ]),
        dcc.Tab(label='Churn vs Monthly Charges', children=[
            dcc.Graph(id='churn-monthly-graph', figure=fig_churn_monthly_enhanced)
        ]),
        dcc.Tab(label='Customer Demographics', children=[
            dcc.Graph(id='gender-distribution-graph', figure=fig_gender_distribution),
            dcc.Graph(id='senior-citizen-distribution-graph', figure=fig_senior_citizen_distribution)
        ]),
        dcc.Tab(label='Service Usage Patterns', children=[
            dcc.Graph(id='multiple-lines-usage-graph', figure=fig_multiple_lines_usage),
            dcc.Graph(id='internet-service-types-graph', figure=fig_internet_service_types)
        ]),
        dcc.Tab(label='Payment Method Preferences', children=[
            dcc.Graph(id='payment-methods-graph', figure=fig_payment_methods)
        ])
    ])
])

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
