
import streamlit as st
import pandas as pd

def top_imdb_chart(df, top_nb):
    col_rank="IMDB Rating"
    col_label="Name"
    col_jk="JK Rating"

    # Defensive copy + basic cleaning
    d = df[[col_rank, col_label, col_jk]].copy()
    d = d.dropna(subset=[col_rank, col_label, col_jk])
    d[col_rank] = pd.to_numeric(d[col_rank], errors="coerce")
    d = d.dropna(subset=[col_rank])

    # Top 10 by A, display B
    top = (
        d.sort_values([col_rank, col_label, col_jk], ascending=[False, True, False])
         .head(top_nb)
         .iloc[::-1]  # reverse for horizontal bars (largest at top after encoding)
    )

    # Optional: colour highlight top 3
    top = top.reset_index(drop=True)

    # Reverse order (top → bottom) and add rank 1..10
    display_df = (
        top[["Name", "IMDB Rating", "JK Rating"]]
        .iloc[::-1]              # reverse row order
        .reset_index(drop=True)  # clean index
    )

    display_df.insert(0, "Rank", range(1, len(display_df) + 1))

    container = st.container(border = True)
    container.markdown(f"#### Top {top_nb} IMDB")
    container.dataframe(display_df, use_container_width=True, hide_index=True)
