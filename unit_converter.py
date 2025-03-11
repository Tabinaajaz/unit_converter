import streamlit as st
import sympy as sp  # For evaluating expressions
import requests  # For currency conversion API

# Set page config with title and wide layout
st.set_page_config(page_title="Unit Converter", layout="wide")

# Apply Background Color using CSS
st.markdown(
    """
    <style>
        body {
            background-color: #f0f8ff;  /* Light Blue */
        }
        .title {
            font-size: 78px;
            font-weight: bold;
            text-align: center;
            color: #333;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Display Title at the Top
st.markdown('<p class="title">🌍 Unit Converter</p>', unsafe_allow_html=True)

# Function to evaluate mathematical expressions
def evaluate_expression(expression):
    try:
        return float(sp.sympify(expression))
    except:
        return None

# Function to get real-time currency exchange rates
def get_currency_rates(base_currency):
    url = f"https://api.exchangerate-api.com/v4/latest/{base_currency}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()["rates"]
    else:
        return None

# Sidebar for Category Selection
category = st.sidebar.selectbox("Select Conversion Category", ["Length", "Mass", "Time", "Temperature", "Currency"])

# Layout Columns
col1, col2, col3 = st.columns([3, 1, 3])

if category == "Length":
    units = {"Meter": 1, "Kilometer": 0.001, "Centimeter": 100, "Millimeter": 1000, "Mile": 0.000621371, "Foot": 3.28084}
    from_unit = col1.selectbox("From", units.keys())
    to_unit = col3.selectbox("To", units.keys())
    value = col1.text_input("Enter Value", "1")
    
    with col2:
        st.write("=")
    
    evaluated_value = evaluate_expression(value)
    if evaluated_value is not None:
        result = evaluated_value * (units[to_unit] / units[from_unit])
        col3.text_input("Converted Value", f"{result:.5f}")
    else:
        col3.warning("Invalid input!")

elif category == "Mass":  # Weight Conversion
    units = {"Kilogram": 1, "Gram": 1000, "Pound": 2.20462, "Ounce": 35.274}
    from_unit = col1.selectbox("From", units.keys())
    to_unit = col3.selectbox("To", units.keys())
    value = col1.text_input("Enter Value", "1")

    with col2:
        st.write("=")

    evaluated_value = evaluate_expression(value)
    if evaluated_value is not None:
        result = evaluated_value * (units[to_unit] / units[from_unit])
        col3.text_input("Converted Value", f"{result:.5f}")
    else:
        col3.warning("Invalid input!")

elif category == "Time":
    units = {"Second": 1, "Minute": 1/60, "Hour": 1/3600, "Day": 1/86400}
    from_unit = col1.selectbox("From", units.keys())
    to_unit = col3.selectbox("To", units.keys())
    value = col1.text_input("Enter Value", "1")

    with col2:
        st.write("=")

    evaluated_value = evaluate_expression(value)
    if evaluated_value is not None:
        result = evaluated_value * (units[to_unit] / units[from_unit])
        col3.text_input("Converted Value", f"{result:.5f}")
    else:
        col3.warning("Invalid input!")

elif category == "Temperature":
    def convert_temperature(value, from_unit, to_unit):
        if from_unit == to_unit:
            return value
        elif from_unit == "Celsius":
            return value * 9/5 + 32 if to_unit == "Fahrenheit" else value + 273.15
        elif from_unit == "Fahrenheit":
            return (value - 32) * 5/9 if to_unit == "Celsius" else (value - 32) * 5/9 + 273.15
        elif from_unit == "Kelvin":
            return value - 273.15 if to_unit == "Celsius" else (value - 273.15) * 9/5 + 32

    units = ["Celsius", "Fahrenheit", "Kelvin"]
    from_unit = col1.selectbox("From", units)
    to_unit = col3.selectbox("To", units)
    value = col1.text_input("Enter Temperature", "1")

    with col2:
        st.write("=")

    evaluated_value = evaluate_expression(value)
    if evaluated_value is not None:
        result = convert_temperature(evaluated_value, from_unit, to_unit)
        col3.text_input("Converted Value", f"{result:.2f}")
    else:
        col3.warning("Invalid input!")

elif category == "Currency":
    base_currency = col1.selectbox("From", ["USD", "EUR", "GBP", "INR", "PKR"])
    target_currency = col3.selectbox("To", ["USD", "EUR", "GBP", "INR", "PKR"])
    value = col1.text_input("Enter Amount", "1")

    with col2:
        st.write("=")

    rates = get_currency_rates(base_currency)
    evaluated_value = evaluate_expression(value)
    
    if rates and evaluated_value is not None:
        if target_currency in rates:
            result = evaluated_value * rates[target_currency]
            col3.text_input("Converted Value", f"{result:.5f}")
        else:
            col3.error("Currency rate not available!")
    else:
        col3.warning("Invalid input or API Error!")
