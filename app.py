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
            st.markdown(f"**{ticker} - ${current_price:.2f} as of {current_time} {current_date}**")
            
            # Expiration date selection
            exp_dates = stock.options
            selected_exp = st.selectbox(f"Select expiration date for {ticker}", exp_dates)
            
            # Timeframe selection for price chart
            timeframes = ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y']
            selected_timeframe = st.selectbox("Select timeframe for price chart", timeframes, index=2)
            
            # Get historical data for selected timeframe
            price_data = stock.history(period=selected_timeframe)
            
            # Create two columns for charts
            col1, col2 = st.columns([2, 1])
            
            with col1:
                # Price chart
                fig_price = go.Figure()
                fig_price.add_trace(go.Scatter(
                    x=price_data.index, 
                    y=price_data['Close'],
                    line=dict(color='royalblue', width=2),
                    name='Price'
                ))
                fig_price.update_layout(
                    title=f"{ticker} Price Chart",
                    xaxis_title="Date",
                    yaxis_title="Price",
                    hovermode="x unified"
                )
                st.plotly_chart(fig_price, use_container_width=True)
            
            with col2:
                # Metric selection for horizontal bar chart
                metrics = ['Open Interest', 'Traded Volume', 'Delta', 'Gamma', 'Vanna', 'Charm']
                selected_metric = st.selectbox("Select metric to display", metrics)
                
                # Generate mock options data (replace with real options chain)
                strikes = np.linspace(current_price * 0.7, current_price * 1.3, 20)
                calls = np.random.randint(100, 1000, size=20)
                puts = np.random.randint(100, 1000, size=20)
                
                # Calculate mock greeks (replace with real calculations)
                delta = np.linspace(-1, 1, 20)
                gamma = np.random.normal(0, 0.2, 20)
                vanna = np.random.normal(0, 0.1, 20)
                charm = np.random.normal(0, 0.05, 20)
                
                # Create horizontal bar chart based on selected metric
                fig_bar = go.Figure()
                
                if selected_metric == 'Open Interest':
                    fig_bar.add_trace(go.Bar(
                        y=strikes,
                        x=calls,
                        name='Calls',
                        orientation='h',
                        marker_color='rgba(55, 128, 191, 0.7)'
                    ))
                    fig_bar.add_trace(go.Bar(
                        y=strikes,
                        x=-puts,
                        name='Puts',
                        orientation='h',
                        marker_color='rgba(255, 128, 191, 0.7)'
                    ))
                    fig_bar.update_layout(barmode='relative')
                    
                elif selected_metric == 'Traded Volume':
                    fig_bar.add_trace(go.Bar(
                        y=strikes,
                        x=calls*0.3,
                        name='Calls Volume',
                        orientation='h',
                        marker_color='rgba(55, 128, 191, 0.7)'
                    ))
                    fig_bar.add_trace(go.Bar(
                        y=strikes,
                        x=-puts*0.3,
                        name='Puts Volume',
                        orientation='h',
                        marker_color='rgba(255, 128, 191, 0.7)'
                    ))
                    fig_bar.update_layout(barmode='relative')
                    
                elif selected_metric == 'Delta':
                    fig_bar.add_trace(go.Bar(
                        y=strikes,
                        x=delta,
                        orientation='h',
                        marker_color=np.where(delta > 0, 'rgba(55, 128, 191, 0.7)', 'rgba(255, 128, 191, 0.7)')
                    ))
                    
                elif selected_metric == 'Gamma':
                    fig_bar.add_trace(go.Bar(
                        y=strikes,
                        x=gamma,
                        orientation='h',
                        marker_color=np.where(gamma > 0, 'rgba(55, 128, 191, 0.7)', 'rgba(255, 128, 191, 0.7)')
                    ))
                    
                elif selected_metric == 'Vanna':
                    fig_bar.add_trace(go.Bar(
                        y=strikes,
                        x=vanna,
                        orientation='h',
                        marker_color=np.where(vanna > 0, 'rgba(55, 128, 191, 0.7)', 'rgba(255, 128, 191, 0.7)')
                    ))
                    
                elif selected_metric == 'Charm':
                    fig_bar.add_trace(go.Bar(
                        y=strikes,
                        x=charm,
                        orientation='h',
                        marker_color=np.where(charm > 0, 'rgba(55, 128, 191, 0.7)', 'rgba(255, 128, 191, 0.7)')
                    ))
                
                # Add current price line
                fig_bar.add_vline(x=0, line_width=0.5, line_color="gray")
                fig_bar.add_hline(y=current_price, line_dash="dot", line_color="black", line_width=2)
                
                fig_bar.update_layout(
                    title=f"{selected_metric} Exposure for {ticker}",
                    yaxis_title="Strike Price",
                    xaxis_title=selected_metric,
                    showlegend=selected_metric in ['Open Interest', 'Traded Volume'],
                    height=600
                )
                st.plotly_chart(fig_bar, use_container_width=True)
            
            # Recommendation section
            st.subheader("Market Maker Positioning Analysis")
            
            # Calculate days to expiration
            exp_date = datetime.strptime(selected_exp, "%Y-%m-%d")
            days_to_exp = (exp_date - datetime.now()).days
            
            # Generate recommendation based on expiration type
            with st.container():
                st.markdown(f"""
                **{ticker} Options Analysis for {selected_exp} ({days_to_exp} days to expiry)**
                
                ### Market Maker Positioning:
                - **Current Spot Price:** ${current_price:.2f}
                - **Gamma Exposure:** {'Positive' if np.sum(gamma) > 0 else 'Negative'} (${abs(np.sum(gamma)):.2f} per 1% move)
                - **Delta Exposure:** {'Long' if np.sum(delta) > 0 else 'Short'} ({abs(np.sum(delta)):.2f} contracts)
                - **Key Strike Levels:** 
                    - Gamma Flip: ${current_price * (1 + np.mean(gamma)):.2f}
                    - Max Pain: ${strikes[np.argmin(np.abs(delta))]:.2f}
                
                ### Expected Moves by Expiry Type:
                """)
                
                # 0DTE Analysis
                if days_to_exp == 0:
                    st.markdown("""
                    **0DTE Positioning:**
                    - Market makers will aggressively hedge gamma exposure
                    - Expect pinning behavior near high open interest strikes
                    - Potential for sharp moves if price breaks through gamma walls
                    - Key levels: ${0:.2f} (support), ${0:.2f} (resistance)
                    """.format(
                        current_price * 0.99,
                        current_price * 1.01
                    ))
                
                # Weekly Analysis
                elif days_to_exp <= 7:
                    st.markdown("""
                    **Weekly Positioning:**
                    - Gamma exposure will dominate price action
                    - Market makers will adjust delta hedges more frequently
                    - Expect mean-reversion toward high open interest strikes
                    - Key levels: ${0:.2f} (support), ${1:.2f} (resistance)
                    """.format(
                        current_price * 0.97,
                        current_price * 1.03
                    ))
                
                # Monthly Analysis
                elif days_to_exp <= 30:
                    st.markdown("""
                    **Monthly Positioning:**
                    - Vanna and Charm effects become more significant
                    - Market makers will adjust for volatility changes
                    - Expect gradual moves toward max pain
                    - Key levels: ${0:.2f} (support), ${1:.2f} (resistance)
                    """.format(
                        current_price * 0.95,
                        current_price * 1.05
                    ))
                
                # LEAPS Analysis
                else:
                    st.markdown("""
                    **LEAPS Positioning:**
                    - Delta hedging is primary concern for market makers
                    - Expect more gradual adjustments to positions
                    - Volatility surface changes will impact pricing
                    - Key levels: ${0:.2f} (support), ${1:.2f} (resistance)
                    """.format(
                        current_price * 0.90,
                        current_price * 1.10
                    ))
                
                st.markdown("""
                **Trading Recommendation:**
                - Monitor gamma exposure changes near key levels
                - Watch for delta hedging flows at ${0:.2f} and ${1:.2f}
                - Consider {'call skew' if np.mean(delta) > 0 else 'put skew'} strategies
                """.format(
                    current_price * 0.98,
                    current_price * 1.02
                ))
                
        except Exception as e:
            st.error(f"Error processing {ticker}: {str(e)}")
