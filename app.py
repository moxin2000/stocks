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

# Create tabs for different views
tab1, tab2 = st.tabs(["Single Ticker Analysis", "Aggregated Exposure View"])

# First tab (existing functionality)
with tab1:
    # [Previous code for single ticker analysis goes here]
    # ... (include all the code from the previous implementation)

# New tab for aggregated exposure view
with tab2:
    st.header("Aggregated Options Exposure Analysis")
    
    # Ticker selection for this view
    selected_tickers_agg = st.multiselect(
        "Select tickers for aggregated view",
        predefined_tickers,
        default=['SPY', 'QQQ', 'IWM']
    )
    
    if not selected_tickers_agg:
        st.warning("Please select at least one ticker")
    else:
        # Time selection
        time_range = st.selectbox(
            "Time range",
            ["1d", "5d", "1mo", "3mo", "6mo"],
            index=2
        )
        
        # Generate mock aggregated data (replace with real data)
        strikes = np.linspace(0.8, 1.2, 41) * 4000  # SPX-like strikes
        gamma = np.random.normal(0, 1, len(strikes)).cumsum()
        delta = np.random.normal(0, 2, len(strikes)).cumsum()
        vanna = np.random.normal(0, 0.5, len(strikes)).cumsum()
        charm = np.random.normal(0, 0.2, len(strikes)).cumsum()
        
        # Create the main exposure chart
        fig_exposure = go.Figure()
        
        # Add traces for each metric
        fig_exposure.add_trace(go.Scatter(
            x=strikes,
            y=gamma,
            name="Gamma Exposure",
            line=dict(color='#1f77b4', width=2),
            yaxis="y1"
        ))
        
        fig_exposure.add_trace(go.Scatter(
            x=strikes,
            y=delta,
            name="Delta Exposure",
            line=dict(color='#ff7f0e', width=2),
            yaxis="y2"
        ))
        
        fig_exposure.add_trace(go.Scatter(
            x=strikes,
            y=vanna,
            name="Vanna Exposure",
            line=dict(color='#2ca02c', width=2),
            yaxis="y3"
        ))
        
        fig_exposure.add_trace(go.Scatter(
            x=strikes,
            y=charm,
            name="Charm Exposure",
            line=dict(color='#d62728', width=2),
            yaxis="y4"
        ))
        
        # Add current price line (mock)
        current_price = 4000
        fig_exposure.add_vline(
            x=current_price,
            line=dict(color="black", width=2, dash="dot"),
            annotation_text="Current Price",
            annotation_position="top right"
        )
        
        # Update layout for multi-axis
        fig_exposure.update_layout(
            title="Aggregated Options Exposure Across Strikes",
            xaxis_title="Strike Price",
            yaxis=dict(
                title="Gamma Exposure",
                titlefont=dict(color="#1f77b4"),
                tickfont=dict(color="#1f77b4"),
                side="left",
                position=0.05
            ),
            yaxis2=dict(
                title="Delta Exposure",
                titlefont=dict(color="#ff7f0e"),
                tickfont=dict(color="#ff7f0e"),
                overlaying="y",
                side="right"
            ),
            yaxis3=dict(
                title="Vanna Exposure",
                titlefont=dict(color="#2ca02c"),
                tickfont=dict(color="#2ca02c"),
                overlaying="y",
                side="right",
                position=0.85
            ),
            yaxis4=dict(
                title="Charm Exposure",
                titlefont=dict(color="#d62728"),
                tickfont=dict(color="#d62728"),
                overlaying="y",
                side="right",
                position=0.95
            ),
            hovermode="x unified",
            height=600,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        st.plotly_chart(fig_exposure, use_container_width=True)
        
        # Create OI/Volume charts in columns
        col1, col2 = st.columns(2)
        
        with col1:
            # Open Interest chart
            oi_calls = np.random.randint(0, 1000, len(strikes))
            oi_puts = np.random.randint(0, 1000, len(strikes))
            
            fig_oi = go.Figure()
            fig_oi.add_trace(go.Bar(
                x=strikes,
                y=oi_calls,
                name="Calls OI",
                marker_color='#1f77b4'
            ))
            fig_oi.add_trace(go.Bar(
                x=strikes,
                y=-oi_puts,
                name="Puts OI",
                marker_color='#d62728'
            ))
            fig_oi.add_vline(
                x=current_price,
                line=dict(color="black", width=2, dash="dot")
            )
            fig_oi.update_layout(
                title="Open Interest by Strike",
                barmode="relative",
                height=400,
                yaxis_title="Contracts",
                hovermode="x unified"
            )
            st.plotly_chart(fig_oi, use_container_width=True)
        
        with col2:
            # Volume chart
            vol_calls = (oi_calls * np.random.uniform(0.1, 0.3, len(strikes))).astype(int)
            vol_puts = (oi_puts * np.random.uniform(0.1, 0.3, len(strikes))).astype(int)
            
            fig_vol = go.Figure()
            fig_vol.add_trace(go.Bar(
                x=strikes,
                y=vol_calls,
                name="Calls Volume",
                marker_color='#1f77b4'
            ))
            fig_vol.add_trace(go.Bar(
                x=strikes,
                y=-vol_puts,
                name="Puts Volume",
                marker_color='#d62728'
            ))
            fig_vol.add_vline(
                x=current_price,
                line=dict(color="black", width=2, dash="dot")
            )
            fig_vol.update_layout(
                title="Today's Volume by Strike",
                barmode="relative",
                height=400,
                yaxis_title="Contracts",
                hovermode="x unified"
            )
            st.plotly_chart(fig_vol, use_container_width=True)
        
        # Key levels and recommendations
        st.subheader("Key Levels and Market Analysis")
        
        # Calculate key levels from mock data
        max_gamma = strikes[np.argmax(np.abs(gamma))]
        zero_gamma = strikes[np.argmin(np.abs(gamma))]
        max_oi = strikes[np.argmax(oi_calls + oi_puts)]
        
        col3, col4 = st.columns(2)
        
        with col3:
            st.markdown("""
            **Key Gamma Levels:**
            - Max Gamma: {:.0f}
            - Zero Gamma: {:.0f}
            - Current Price: {:.0f}
            
            **Open Interest:**
            - Highest OI Strike: {:.0f}
            - Call Wall: {:.0f}
            - Put Wall: {:.0f}
            """.format(
                max_gamma, zero_gamma, current_price,
                max_oi,
                strikes[np.argmax(oi_calls)],
                strikes[np.argmax(oi_puts)]
            ))
        
        with col4:
            st.markdown("""
            **Market Implications:**
            - Strong gamma resistance at {:.0f}
            - Support zone between {:.0f}-{:.0f}
            - Expected dealer hedging between {:.0f}-{:.0f}
            
            **Trading Recommendation:**
            - Consider spreads around {:.0f} gamma level
            - Watch for pinning at {:.0f} OI strike
            - Monitor delta hedging flows above {:.0f}
            """.format(
                max_gamma,
                zero_gamma - 50, zero_gamma,
                current_price - 30, current_price + 30,
                zero_gamma,
                max_oi,
                current_price + 50
            ))
