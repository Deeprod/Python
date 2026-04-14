import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px

def ecdf(df):
    col = "IMDB Rating"  # numeric
    x = df[col].dropna()

    # Pick a reference percentile (e.g., median)
    ref_p = 0.50
    ref_value = np.quantile(x, ref_p)

    fig = px.ecdf(df, x=col, ecdfnorm="probability")
    
    # Add a vertical line at the reference percentile value
    fig.add_vline(x=ref_value, line_dash="dash", line_color="orange",
                annotation_text=f"{int(ref_p*100)}th pct = {ref_value:,.2f}",
                annotation_position="top right")
    
    container = st.container(border = True)
    container.markdown(f"#### ECDF of {col}")
    
    container.plotly_chart(fig, use_container_width=True)