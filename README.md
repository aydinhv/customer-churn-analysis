# Customer Churn Analysis Dashboard

## Overview
This project analyzes customer churn data to identify patterns and factors contributing to customer churn. The interactive dashboard created using Dash and Plotly provides insights through various visualizations.

## Features
- **Churn Rate by Contract Type**: Pie chart showing the distribution of churned customers by contract type.
- **Average Monthly Charges by Internet Service Type**: Line chart showing average monthly charges across different internet service types.
- **Distribution of Tenure vs Monthly Charges**: Box plot displaying the distribution of tenure against monthly charges.
- **Churn vs Monthly Charges**: Scatter plot visualizing the relationship between monthly charges and total charges, with churn status indicated.
- **Customer Demographics**: Pie charts showing gender and senior citizen distribution.
- **Service Usage Patterns**: Bar chart and pie chart showing multiple lines usage and internet service types.
- **Payment Method Preferences**: Pie chart showing the distribution of different payment methods.

## How to Run
1. Clone the repository:
    ```sh
    git clone https://github.com/aydinhv/customer-churn-analysis.git
    cd customer-churn-analysis
    ```

2. Install required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

3. Run the Dash application:
    ```sh
    python app.py
    ```

## Dataset
The dataset used in this project is generated synthetically for demonstration purposes.

## Requirements
- Python 3.x
- Dash
- Plotly
- Pandas
- Numpy
- Faker

## License
This project is licensed under the MIT License.
