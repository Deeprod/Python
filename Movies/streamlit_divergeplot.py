import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
        
def divergeplot_movies(df_movie):
    
    column = "Rating Diff"
    top_bottom_size = 20
    figsize = (6, 10)
    df_with_diff = df_movie
    df_with_diff[column] = df_movie['JK Rating'] - df_movie['IMDB Rating']
    
    top = df_movie.nlargest(top_bottom_size, column).iloc[::-1]    #.iloc[::-1] this reverse all rows
    bottom = df_movie.nsmallest(top_bottom_size, column)
    df = pd.concat([bottom, top]).reset_index(drop=True)
    
    container = st.container(border = True)
    container.markdown("#### JK vs IMDB biggest differences")

    fig = plt.figure(figsize = figsize, facecolor='white')
    ax = fig.add_subplot()

    colors = ["red" if x < 0 else "green" for x in df[column]]
    ax.hlines(y = df["Name"], xmin = 0 , color = colors, xmax = df[column], linewidth = 1)

    # iterate over x and y 
    for x, y in zip(df[column],  df.index):
        # annotate text
        ax.text(x - 0.1 if x < 0 else x + 0.1, 
                y, 
                round(x, 2), 
                color = "red" if x < 0 else "green",  
                horizontalalignment='right' if x < 0 else 'left', 
                size = 10)
    
        ax.scatter(x, 
                    y, 
                    color = "red" if x < 0 else "green", 
                    alpha = 1)

    # set title
    ax.set_title("")
    # change x lim
    ax.set_xlim(df[column].min()-1, df[column].max()+1)

    # set labels
    ax.tick_params(colors='white')
    # ax.set_xlabel("Label 1")
    # ax.set_ylabel("Label 2")

    ax.grid(linestyle='--', alpha=0.1)
    ax.set_yticks(df.index)
    ax.set_yticklabels(df["Name"])
    ax.spines["top"].set_color("None")
    ax.spines["left"].set_color("None")
    ax.spines['right'].set_position(('data',0))
    ax.spines['right'].set_color('white')

    fig.patch.set_alpha(0)  # Makes the figure background transparent
    ax.set_facecolor('none')  # Makes the plot area transparent

    container.pyplot(fig, transparent=True)