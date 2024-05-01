import pandas as pd
import streamlit as st
import requests
import json
import os



def load_session_state():
    try:
        with open('session_state.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def save_session_state(session_state):
    with open('session_state.json', 'w') as file:
        json.dump(session_state, file)


# Function to downsample the DataFrame and interpolate missing values
def downsample_data(data, sampling_frequency):
    return data.resample(sampling_frequency).mean().interpolate(method='linear').dropna()


def set_background(color):
    hex_color = f'#{color}'
    html = f"""
        <style>
        .stApp {{
            background-color: {hex_color};
        }}
        </style>
    """
    st.markdown(html, unsafe_allow_html=True)


def card_with_modal(title, title_image, content_image, content):
    # Display the image as a hyperlink in the card title
    st.image(title_image, caption=title, use_column_width=True)

    # Display the content and expander below the image
    with st.expander("Click to view details"):
        # Display the image directly in the expander with a specified width
        st.image(content_image, caption=title, use_column_width=True, width=400)
        st.write(content)


def main():
    st.title("Stock market predictor")
    session_state = load_session_state()

    if st.query_params:
        username = st.query_params['username']
        email = st.query_params['email']
        session_state = load_session_state()
        session_state['username'] = username
        save_session_state(session_state)
    else:
        username = session_state.get('username', "")

    if username == "":
        st.write('User not logged in!')
        # Display the login button
        button_clicked = st.button("Login")
        login_url = 'http://localhost:8000/signin'
        # If the button is clicked, open the login URL in the same tab
        if button_clicked:
            st.markdown(f'<meta http-equiv="refresh" content="0;URL={login_url}">', unsafe_allow_html=True)
        exit()

    # Load first dataset
    if st.button("Logout"):
        session_state = {}
        save_session_state(session_state)
        login_url = 'http://localhost:8000/signin'
        st.markdown(f'<meta http-equiv="refresh" content="0;URL={login_url}">', unsafe_allow_html=True)
    # Load first dataset
    set_background("000000")
    data1 = pd.read_csv('finalactualvspredicted.csv')
    data1['Date'] = pd.to_datetime(data1['Date'])  # Convert 'Date' column to datetime format
    data1.set_index('Date', inplace=True)  # Set 'Date' column as index

    # Downsample first dataset to reduce data points and interpolate missing values
    data1_downsampled = downsample_data(data1, '1D')

    # Calculate support and resistance levels using rolling minimum and maximum for first dataset
    data1_downsampled['Support_Level'] = data1_downsampled['Actual_Price'].rolling(window=14).min()
    data1_downsampled['Resistance_Level'] = data1_downsampled['Actual_Price'].rolling(window=14).max()

    # Determine target value based on predicted price for first dataset
    predicted_price1 = data1_downsampled['Predicted_Price'].iloc[-1]
    target1 = predicted_price1 * 1.1  # Example: 10% increase

    # Plot the first graph for actual and predicted prices
    # st.title('Stock Prediction market')
    st.line_chart(data1_downsampled[['Actual_Price', 'Predicted_Price']])

    # Show final predicted and target prices for first dataset
    st.write(f"Target Price: {target1}")
    st.write("RMSE(Root Mean Squared Error): 3-5")

    # Create an expander
    with st.expander("Click to view RMSE image"):
        # Load and display the image
        st.image("RMSEplot.jpg", caption="RMSE Image")

    # Display support and resistance levels for first dataset
    st.write("Support Level:", data1_downsampled['Support_Level'].iloc[-1])
    st.write("Resistance Level:", data1_downsampled['Resistance_Level'].iloc[-1])

    # Load second dataset
    data2 = pd.read_csv('next 1year prediction.csv')
    data2['Date'] = pd.to_datetime(data2['Date'], format='%d-%m-%Y %H:%M')
    data2.set_index('Date', inplace=True)  # Set 'Date' column as index

    # Downsample second dataset to reduce data points and interpolate missing values
    data2_downsampled = downsample_data(data2, '1D')

    # Plot the second graph for the second dataset
    st.title('Next 1 year Prediction')
    st.line_chart(data2_downsampled['Predicted_Price'], use_container_width=True)
    # Extract the first value as the prediction for the next day
    next_day_prediction = data2_downsampled['Predicted_Price'].iloc[0]

    # Extract the last value as the prediction for the next year
    next_year_prediction = data2_downsampled['Predicted_Price'].iloc[-1]
    next_month_prediction = 18214.6156543445182
    # Display the predictions
    st.write("Prediction for the next day:", next_day_prediction)
    st.write("Prediction for the next month", next_month_prediction)
    st.write("Prediction for the next year:", next_year_prediction)

    # Display logo images and plot images in separate containers
    st.write("---")  # Add a separator

    logo_col1, plot_col1, logo_col2, plot_col2 = st.columns(4)

    cards_data = [
        {"title": "Adani", "title_image": "Adani_2012_logo.png", "content_image": "ADANIPORTS_plot.png",
         "content": "Here is the stock price and information about Adani ports."},
        {"title": "Asian paints", "title_image": "asian paints.png", "content_image": "ASIANPAINT_plot.png",
         "content": "Here is the stock price and information about Asian paints."},
        {"title": "Axis bank", "title_image": "axis bank.png", "content_image": "AXISBANK_plot.png",
         "content": "Here is the stock price and information about Axis bank."},
        {"title": "Bajaj Auto ltd", "title_image": "Bajaj Auto ltd.jpg", "content_image": "BAJAJ-AUTO_plot.png",
         "content": "Here is the stock price and information about Bajaj Auto ltd."},
        {"title": "Bajaj finserv", "title_image": "bajaj finserv.jpg", "content_image": "BAJAJFINSV_plot.png",
         "content": "Here is the stock price and information about Bajaj finserv."},
        {"title": "Bajaj Finance", "title_image": "Bajaj-Finance.png", "content_image": "BAJFINANCE_plot.png",
         "content": "Here is the stock price and information about Bajaj Finance."},
        {"title": "Bharat petroleum", "title_image": "Bharat petroleum.jpg", "content_image": "BHARTIARTL_plot.png",
         "content": "Here is the stock price and information about Bharat petroleum."},
        {"title": "britannia", "title_image": "britannia.jpg", "content_image": "BRITANNIA_plot.png",
         "content": "Here is the stock price and information about Britannia."},
        {"title": "cipla", "title_image": "cipla.png", "content_image": "CIPLA_plot.png",
         "content": "Here is the stock price and information about cipla."},
        {"title": "coal india", "title_image": "coal india.png", "content_image": "COALINDIA_plot.png",
         "content": "Here is the stock price and information about coal india."},
        # {"title": "divis", "title_image": "divis.png", "content_image": "......", "content": "Here is the stock price and information about divis."},
        {"title": "dr reddy", "title_image": "dr reddys.jpg", "content_image": "DRREDDY_plot.png",
         "content": "Here is the stock price and information about dr reddy."},
        {"title": "Eicher", "title_image": "Eicher-logo.png", "content_image": "EICHERMOT_plot.png",
         "content": "Here is the stock price and information about Eicher."},
        {"title": "Gail", "title_image": "Gail.png", "content_image": "GAIL_plot.png",
         "content": "Here is the stock price and information Gail."},
        {"title": "HCL", "title_image": "HCL-Logo-1976.png", "content_image": "HCLTECH_plot.png",
         "content": "Here is the stock price and information about HCL."},
        {"title": "HDFC Bank", "title_image": "hdfc bank.png", "content_image": "HDFCBANK_plot.png",
         "content": "Here is the stock price and information about HDFC Bank."},
        # {"title": "HDFC Life", "title_image": "hdfc life.jpg", "content_image": "", "content": "Here is the stock price and information about HDFC Life."},
        {"title": "HDFC", "title_image": "hdfc.png", "content_image": "HDFC_plot.png",
         "content": "Here is the stock price and information about HDFC."},
        {"title": "Hero", "title_image": "Hero-Logo.png", "content_image": "HEROMOTOCO_plot.png",
         "content": "Here is the stock price and information about Hero."},
        {"title": "hindalco", "title_image": "hindalco.png", "content_image": "HINDALCO_plot.png",
         "content": "Here is the stock price and information about Hindalco."},
        {"title": "icici bank", "title_image": "icici bank.png", "content_image": "ICICIBANK_plot.png",
         "content": "Here is the stock price and information about icici bank."},
        # {"title": "indian oil", "title_image": "Indian-Oil-Logo.png", "content_image": "", "content": "Here is the stock price and information about indian oil."},
        {"title": "indusind bank", "title_image": "indusind-bank-logo-01.png", "content_image": "INDUSINDBK_plot.png",
         "content": "Here is the stock price and information about indusind bank."},
        {"title": "infosys", "title_image": "infosys.png", "content_image": "INFY_plot.png",
         "content": "Here is the stock price and information about infosys."},
        {"title": "ITC", "title_image": "ITC_Limited-Logo.wine.png", "content_image": "ITC_plot.png",
         "content": "Here is the stock price and information ITC."},
        {"title": "jsw", "title_image": "jsw.png", "content_image": "JSWSTEEL_plot.png",
         "content": "Here is the stock price and information about jsw."},
        {"title": "Kotak bank", "title_image": "kotak mahindra.jpg", "content_image": "KOTAKBANK_plot.png",
         "content": "Here is the stock price and information about kotak bank."},
        {"title": "Larsen", "title_image": "Larsen-and-turbo-LT-logo.png", "content_image": "LT_plot.png",
         "content": "Here is the stock price and information about Larsen."},
        {"title": "mahindra", "title_image": "mahindra.jpg", "content_image": "MM_plot.png",
         "content": "Here is the stock price and information about mahindra."},
        {"title": "Maruti-Suzuki", "title_image": "Maruti-Suzuki-Logo-2000.png", "content_image": "MARUTI_plot.png",
         "content": "Here is the stock price and information about Maruti Suzuki."},
        {"title": "nestle", "title_image": "nestle.png", "content_image": "NESTLEIND_plot.png",
         "content": "Here is the stock price and information about nestle."},
        {"title": "ntpc", "title_image": "ntpc--600.png", "content_image": "NTPC_plot.png",
         "content": "Here is the stock price and information about ntpc."},
        {"title": "ONGC", "title_image": "ONGC_Logo.png", "content_image": "ONGC_plot.png",
         "content": "Here is the stock price and information about ONGC."},
        {"title": "power grid", "title_image": "powergrid.png", "content_image": "POWERGRID_plot.png",
         "content": "Here is the stock price and information about power grid."},
        {"title": "relaince", "title_image": "reliance.png", "content_image": "RELIANCE_plot.png",
         "content": "Here is the stock price and information about relaince."},
        {"title": "sbi", "title_image": "SBI-Logo.png", "content_image": "SBIN_plot.png",
         "content": "Here is the stock price and information about sbi."},
        {"title": "shree cement", "title_image": "shree cement.jpg", "content_image": "SHREECEM_plot.png",
         "content": "Here is the stock price and information about shree cement."},
        {"title": "sun pharma", "title_image": "sun pharma.png", "content_image": "SUNPHARMA_plot.png",
         "content": "Here is the stock price and information about sun pharma."},
        {"title": "tata motors", "title_image": "tata motors.png", "content_image": "TATAMOTORS_plot.png",
         "content": "Here is the stock price and information about tata motors."},
        {"title": "tata steel", "title_image": "tata steel.jpg", "content_image": "TATASTEEL_plot.png",
         "content": "Here is the stock price and information about tata steel."},
        # {"title": "tata teleservices", "title_image": "tata teleservices.png", "content_image": "......", "content": "Here is the stock price and information about tata teleservices."},
        # {"title": "tata", "title_image": "tata.png", "content_image": ".......", "content": "Here is the stock price and information about tata."},
        {"title": "tcs", "title_image": "Bajaj Auto ltd.jpg", "content_image": "TCS_plot.png",
         "content": "Here is the stock price and information about tcs."},
        {"title": "tech mahindra", "title_image": "tech mahindra.png", "content_image": "TECHM_plot.png",
         "content": "Here is the stock price and information about Tech mahindra."},
        {"title": "titan", "title_image": "titan.png", "content_image": "TITAN_plot.png",
         "content": "Here is the stock price and information about titan."},
        {"title": "ultratech cement", "title_image": "UltraTech Cement Limited - Aditya Birla Group Logo.jpg",
         "content_image": "ULTRACEMCO_plot.png",
         "content": "Here is the stock price and information about ultratech cement."},
        # {"title": "unilever", "title_image": "unilever-logo.jpg", "content_image": ".......", "content": "Here is the stock price and information about unilever."},
        {"title": "wipro", "title_image": "wipro.jpg", "content_image": "WIPRO_plot.png",
         "content": "Here is the stock price and information about wipro."},
    ]

    for i, card_data in enumerate(cards_data):
        if i % 2 == 0:
            with logo_col1:
                card_with_modal(card_data["title"], card_data["title_image"], card_data["content_image"],
                                card_data["content"])
        else:
            with logo_col2:
                card_with_modal(card_data["title"], card_data["title_image"], card_data["content_image"],
                                card_data["content"])

    # Feedback form
    st.write("---")
    st.header("Feedback Form")
    name = st.text_input("Name (Optional)")
    email = st.text_input("Email (Optional)")
    suggestion = st.text_area("Suggestion (Compulsory)")
    if st.button("Submit"):
        if suggestion.strip():  # Check if suggestion is not empty
            feedback_df = pd.DataFrame({"Name": [name], "Email": [email], "Suggestion": [suggestion]})
            feedback_df.to_csv("feedback.csv", mode='a', index=False, header=not os.path.exists("feedback.csv"))
            name = ""
            email = ""
            suggestion = ""
            st.success("Feedback submitted successfully!")

        else:
            st.error("Please provide a suggestion before submitting.")


if __name__ == "__main__":
    main()
