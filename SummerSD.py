import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 網頁基本設定
st.set_page_config(
    page_title="夏季奧運歷屆獎牌分析系統",
    page_icon="🏅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. 讀取資料
@st.cache_data
def load_data():
    df = pd.read_csv("SummerSD.csv")
    df['Year'] = df['Year'].astype(int)
    return df

try:
    df = load_data()
except FileNotFoundError:
    st.error("❌ 找不到 'SummerSD.csv' 檔案，請確保它與此程式碼放在同一個資料夾中。")
    st.stop()

# 3. 側邊欄控制面板
st.sidebar.header("🎯 數據篩選面板")

years = sorted(df['Year'].unique())
selected_years = st.sidebar.multiselect("選擇奧運年份 (預選全部)", options=years, default=years)

genders = df['Gender'].unique().tolist()
selected_genders = st.sidebar.multiselect("選擇性別 (預選全部)", options=genders, default=genders)

medals = ['Gold', 'Silver', 'Bronze']
selected_medals = st.sidebar.multiselect("選擇獎牌類型 (預選全部)", options=medals, default=medals)

filtered_df = df[
    (df['Year'].isin(selected_years)) &
    (df['Gender'].isin(selected_genders)) &
    (df['Medal'].isin(selected_medals))
]

# 4. 主頁面標題
st.title("🏅 夏季奧運歷屆獎牌互動式分析 Dashboard")
st.write("---")

# 5. 關鍵指標卡片
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("🏆 當前總獎牌數", f"{len(filtered_df):,}")
with col2:
    st.metric("🌍 參賽國家總數", f"{filtered_df['Country'].nunique():,}")
with col3:
    st.metric("🏃 獲獎運動員數", f"{filtered_df['Athlete'].nunique():,}")
with col4:
    st.metric("🎯 涵蓋運動項目", f"{filtered_df['Sport'].nunique():,}")

st.write("---")

# 6. 分頁設計
tab1, tab2, tab3 = st.tabs(["📊 國家獎牌榜分析", "📈 國家歷年趨勢", "📋 原始資料檢視"])

# --- Tab 1: 國家獎牌榜分析 ---
with tab1:
    st.subheader("🥇 各國獎牌分佈 Top 10")
    
    if not filtered_df.empty:
        country_counts = (
            filtered_df.groupby(['Country', 'Medal'])
            .size()
            .reset_index(name='Count')
        )
        
        top_countries = (
            filtered_df['Country'].value_counts().head(10).index.tolist()
        )
        plot_df = country_counts[country_counts['Country'].isin(top_countries)]
        
        # 修正點：確保 px 有被正確 import 才能呼叫
        fig_bar = px.bar(
            plot_df,
            x='Country',
            y='Count',
            color='Medal',
            title="前 10 大獲獎國家獎牌結構圖",
            labels={'Count': '獎牌數量', 'Country': '國家'},
            color_discrete_map={'Gold': '#FFD700', 'Silver': '#C0C0C0', 'Bronze': '#CD7F32'},
            category_orders={'Medal': ['Gold', 'Silver', 'Bronze'], 'Country': top_countries}
        )
        fig_bar.update_layout(xaxis_categoryorder='total descending')
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.warning("⚠️ 目前篩選條件下無數據，請調整左側篩選面板。")

# --- Tab 2: 國家歷年趨勢 ---
with tab2:
    st.subheader("📈 單一國家歷年獎牌走勢")
    
    all_countries = sorted(df['Country'].dropna().unique())
    target_country = st.selectbox("請選擇要分析的國家：", options=all_countries, index=all_countries.index("United States") if "United States" in all_countries else 0)
    
    country_df = df[df['Country'] == target_country]
    
    if not country_df.empty:
        trend_df = country_df.groupby(['Year', 'Medal']).size().reset_index(name='Count')
        fig_trend = px.line(
            trend_df,
            x='Year',
            y='Count',
            color='Medal',
            markers=True,
            title=f"【{target_country}】歷屆奧運獎牌數量變化趨勢",
            labels={'Count': '獎牌數', 'Year': '年份'},
            color_discrete_map={'Gold': '#FFD700', 'Silver': '#C0C0C0', 'Bronze': '#CD7F32'}
        )
        st.plotly_chart(fig_trend, use_container_width=True)
        
        st.write(f"💡 **【{target_country}】最擅長的運動項目項目 (前 5 名)**")
        sport_df = country_df['Sport'].value_counts().head(5).reset_index()
        sport_df.columns = ['運動項目', '累計獎牌數']
        
        fig_sport = px.pie(
            sport_df,
            names='運動項目',
            values='累計獎牌數',
            hole=0.4,
            color_discrete_sequence=px.colors.sequential.RdBu
        )
        st.plotly_chart(fig_sport, use_container_width=True)
    else:
        st.info("該國家在當前篩選條件下未獲得獎牌。")

# --- Tab 3: 原始資料檢視 ---
with tab3:
    st.subheader("🔍 篩選後的原始資料明細")
    
    search_query = st.text_input("搜尋關鍵字（如選手姓名、運動項目）：")
    if search_query:
        display_df = filtered_df[
            filtered_df.astype(str).apply(lambda row: row.str.contains(search_query, case=False)).any(axis=1)
        ]
    else:
        display_df = filtered_df
        
    st.dataframe(display_df, use_container_width=True)
    
    csv_data = display_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 下載當前篩選後的 CSV 資料",
        data=csv_data,
        file_name="filtered_olympic_data.csv",
        mime="text/csv"
    )