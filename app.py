import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta
import pytz

# Set page layout
st.set_page_config(layout="wide")

# Predefined tickers
predefined_tickers = ['SPX', 'SPY', 'NDX', 'QQQ', 'RUT', 'IWM', 
                     'AAPL', 'AMD', 'AMZN', 'MSFT', 'META', 'TSLA', 'GOOG', 'NVDA']

# Sidebar navigation
with st.sidebar:
    st.header("Ticker Selection")
    selected_tickers = []
    
    # Predefined tickers checkboxes
    st.subheader("Predefined Tickers")
    cols = st.columns(2)
    for i, ticker in enumerate(predefined_tickers):
        with cols[i % 2]:
            if st.checkbox(ticker, key=f"pre_{ticker}"):
                selected_tickers.append(ticker)
    
    # Custom ticker input
    st.subheader("Custom Ticker")
    custom_ticker = st.text_input("Enter any ticker symbol:")
    if custom_ticker:
        selected_tickers.append(custom_ticker.upper())

# Main content
if not selected_tickers:
    st.warning("Please select at least one ticker from the sidebar")
else:
    for ticker in selected_tickers:
        try:
            # Get stock data
            stock = yf.Ticker(ticker)
            hist = stock.history(period="1d")
            
            if hist.empty:
                st.error(f"No data available for {ticker}")
                continue
                
            current_price = hist['Close'].iloc[-1]
            current_time = datetime.now(pytz.timezone('US/Eastern')).strftime('%H:%M:%S')
            current_date = datetime.now(pytz.timezone('US/Eastern')).strftime('%Y-%m-%d')
            
            # Header section
            st.header(f"{ticker} - ${current_price:.2f} as of {current_time} {current_date}")
            
            # Expiration date selection
            exp_dates = stock.options
            selected_exp = st.selectbox(f"Select expiration date for {ticker}", exp_dates)
            
            # Generate mock options data (replace with real options chain)
            strikes = np.linspace(current_price * 0.7, current_price * 1.3, 20)
            calls = np.random.randint(100, 1000, size=20)
            puts = np.random.randint(100, 1000, size=20)
            
            # Calculate mock greeks (replace with real calculations)
            delta = np.linspace(-1, 1, 20)
            gamma = np.abs(np.random.normal(0.5, 0.1, 20))
            vanna = np.random.normal(0, 0.2, 20)
            charm = np.random.normal(0, 0.05, 20)
            
            # Create tabs for different metrics
            tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
                "Delta Exposure", "Gamma Exposure", "Vanna Exposure", 
                "Charm Exposure", "Open Interest", "Traded Volume"
            ])
            
            # Common plot style
            def create_bar_plot(x, y, title, y_title, current_price):
                fig = go.Figure()
                fig.add_trace(go.Bar(x=x, y=y, marker_color='rgba(55, 128, 191, 0.7)'))
                fig.add_vline(x=current_price, line_dash="dot", line_color="red", line_width=2)
                fig.update_layout(
                    title=f"{title} for {ticker} - {current_date} {current_time}",
                    xaxis_title="Strike Price",
                    yaxis_title=y_title,
                    showlegend=False
                )
                return fig
            
            with tab1:
                st.plotly_chart(create_bar_plot(
                    strikes, delta, "Delta Exposure", "Delta", current_price
                ), use_container_width=True)
                
            with tab2:
                st.plotly_chart(create_bar_plot(
                    strikes, gamma, "Gamma Exposure", "Gamma per 1% move", current_price
                ), use_container_width=True)
                
            with tab3:
                st.plotly_chart(create_bar_plot(
                    strikes, vanna, "Vanna Exposure", "Vanna per 1% IV move", current_price
                ), use_container_width=True)
                
            with tab4:
                st.plotly_chart(create_bar_plot(
                    strikes, charm, "Charm Exposure", "Charm per day till expiry", current_price
                ), use_container_width=True)
                
            with tab5:
                fig = go.Figure()
                fig.add_trace(go.Bar(x=strikes, y=calls, name='Calls', marker_color='rgba(55, 128, 191, 0.7)'))
                fig.add_trace(go.Bar(x=strikes, y=puts, name='Puts', marker_color='rgba(255, 128, 191, 0.7)'))
                fig.add_vline(x=current_price, line_dash="dot", line_color="black", line_width=2)
                fig.update_layout(
                    title=f"Open Interest for {ticker} - {current_date} {current_time}",
                    xaxis_title="Strike Price",
                    yaxis_title="Open Interest",
                    barmode='group'
                )
                st.plotly_chart(fig, use_container_width=True)
                
            with tab6:
                fig = go.Figure()
                fig.add_trace(go.Bar(x=strikes, y=calls*0.3, name='Calls Volume', marker_color='rgba(55, 128, 191, 0.7)'))
                fig.add_trace(go.Bar(x=strikes, y=puts*0.3, name='Puts Volume', marker_color='rgba(255, 128, 191, 0.7)'))
                fig.add_vline(x=current_price, line_dash="dot", line_color="black", line_width=2)
                fig.update_layout(
                    title=f"Traded Volume for {ticker} - {current_date} {current_time}",
                    xaxis_title="Strike Price",
                    yaxis_title="Volume",
                    barmode='group'
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Recommendation section
            st.subheader("Trading Recommendation")
            
            # Calculate days to expiration
            exp_date = datetime.strptime(selected_exp, "%Y-%m-%d")
            days_to_exp = (exp_date - datetime.now()).days
            
            # Generate mock recommendation (replace with real analysis)
            if days_to_exp == 0:
                expiry_type = "0DTE"
                recommendation = "Highly sensitive to gamma effects. Expect increased volatility near key strikes."
            elif days_to_exp <= 7:
                expiry_type = "Weekly"
                recommendation = "Gamma positioning will influence short-term price action."
            elif days_to_exp <= 30:
                expiry_type = "Monthly"
                recommendation = "Gamma and vanna effects important for medium-term direction."
            else:
                expiry_type = "LEAPS"
                recommendation = "Charm and vanna will have more impact than gamma."
            
            # Create recommendation box
            with st.container():
                st.markdown(f"""
                **{ticker} {expiry_type} Options Analysis ({selected_exp})**
                
                - **Current Price:** ${current_price:.2f}
                - **Expected Range:** ${current_price*0.97:.2f} to ${current_price*1.03:.2f}
                - **Key Levels:** 
                    - Support: ${current_price*0.98:.2f} (Puts heavy)
                    - Resistance: ${current_price*1.02:.2f} (Calls heavy)
                - **Bias:** {'Bullish' if np.sum(delta) > 0 else 'Bearish'}
                
                **Recommendation:**
                {recommendation}
                
                **Strategy Suggestion:**
                - Consider {'call spreads' if np.sum(delta) > 0 else 'put spreads'} for directional plays
                - Iron condors may work well given current gamma positioning
                - Key strikes to watch: ${current_price*0.98:.2f} and ${current_price*1.02:.2f}
                
                **News/Adjustments:**
                - Monitor earnings announcements or macroeconomic events
                - Watch for large block trades that could change gamma exposure
                """)
                
        except Exception as e:
            st.error(f"Error processing {ticker}: {str(e)}")