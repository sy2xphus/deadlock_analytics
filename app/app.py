import streamlit as st
import pandas as pd
import plotly.express as px
import os
import sys

# Add project root to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.analysis.analytics import DeadlockAnalyzer

# Page Config
st.set_page_config(
    page_title="Deadlock Meta Analyzer",
    page_icon="🎮",
    layout="wide"
)

# Initialize Analyzer
@st.cache_resource
def get_analyzer():
    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'deadlock.db'))
    return DeadlockAnalyzer(db_path)

try:
    analyzer = get_analyzer()
except Exception as e:
    st.error(f"Failed to connect to database: {e}")
    st.stop()

# Title
st.title("🧙‍♂️ Deadlock Meta Analyzer")
st.markdown("Data-driven insights into the current patch meta.")

# Sidebar
st.sidebar.header("Configuration")
min_duration = st.sidebar.slider("Min Match Duration (mins)", 0, 60, 10, help="Filter out turbo games/stomps")

st.sidebar.markdown("---")
st.sidebar.subheader("📢 Analyst's Corner")
my_take = st.sidebar.text_area("My Take", "Write your observation here...", height=200)
if my_take != "Write your observation here...":
    st.sidebar.info(f"📝 **Note**: {my_take}")

# Main Tabs
tab1, tab2, tab3 = st.tabs(["📊 General Meta", "🦸 Hero Analysis", "💾 Raw Data"])

# --- TAB 1: GENERAL META ---
with tab1:
    st.header("Meta Overview")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💰 Snowball Effect")
        st.markdown("Does a Net Worth lead guarantee victory?")
        try:
            df_snowball = analyzer.get_net_worth_correlation()
            fig_snowball = px.box(
                df_snowball, 
                x='is_winner', 
                y='avg_team_net_worth', 
                color='is_winner',
                labels={'is_winner': 'Winner (1=Yes, 0=No)', 'avg_team_net_worth': 'Average Team Net Worth'},
                color_discrete_map={0: '#EF553B', 1: '#00CC96'} 
            )
            st.plotly_chart(fig_snowball, use_container_width=True)
        except Exception as e:
            st.error(f"Error loading Snowball data: {e}")

    with col2:
        st.subheader("🏆 Meta Tier List")
        st.markdown("Pick Rate vs. Win Rate Correlation")
        try:
            df_meta = analyzer.get_meta_rating()
            fig_meta = px.scatter(
                df_meta, 
                x='pick_rate', 
                y='win_rate', 
                size='meta_score', 
                color='meta_score', 
                hover_data=['hero_id'],
                color_continuous_scale=px.colors.sequential.Viridis,
                labels={'pick_rate': 'Pick Rate', 'win_rate': 'Win Rate'}
            )
            st.plotly_chart(fig_meta, use_container_width=True)
        except Exception as e:
            st.error(f"Error loading Meta data: {e}")

# --- TAB 2: HERO ANALYSIS ---
with tab2:
    st.header("Hero Deep Dive")
    
    try:
        df_duration = analyzer.get_winrate_by_duration()
        all_heroes = sorted(df_duration['hero_id'].unique())
        
        selected_hero = st.selectbox("Select Hero ID", all_heroes)
        
        st.subheader(f"⏱️ Late Game Potential: Hero {selected_hero}")
        st.markdown(f"How does Hero {selected_hero}'s winrate change as the game gets longer?")
        
        # Filter for selected hero and compare with average
        hero_data = df_duration[df_duration['hero_id'] == selected_hero]
        
        # Calculate global average winrate per bucket for comparison
        avg_data = df_duration.groupby('duration_bucket')['winrate'].mean().reset_index()
        avg_data['Type'] = 'Average'
        hero_data = hero_data.copy()
        hero_data['Type'] = f'Hero {selected_hero}'
        
        combined_data = pd.concat([hero_data[['duration_bucket', 'winrate', 'Type']], avg_data[['duration_bucket', 'winrate', 'Type']]])
        
        fig_duration = px.line(
            combined_data, 
            x='duration_bucket', 
            y='winrate', 
            color='Type', 
            markers=True,
            category_orders={'duration_bucket': ['0-15m', '15-25m', '25-40m', '40m+']},
            color_discrete_map={'Average': 'gray', f'Hero {selected_hero}': '#636EFA'}
        )
        st.plotly_chart(fig_duration, use_container_width=True)
        
    except Exception as e:
        st.error(f"Error loading Hero data: {e}")

# --- TAB 3: RAW DATA ---
with tab3:
    st.header("Raw Data Explorer")
    st.markdown("Inspect the underlying data.")
    
    with st.expander("Matches Table"):
        conn = analyzer.get_connection()
        matches_df = pd.read_sql_query("SELECT * FROM matches LIMIT 100", conn)
        st.dataframe(matches_df)
        conn.close()
        
    with st.expander("Player Stats Table"):
        conn = analyzer.get_connection()
        stats_df = pd.read_sql_query("SELECT * FROM player_stats LIMIT 100", conn)
        st.dataframe(stats_df)
        conn.close()
