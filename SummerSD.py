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

# 2. 國家中英文對照字典 (涵蓋 SummerSD.csv 中所有 129 個國家/地區)
COUNTRY_TRANSLATION = {
    'Hungary': '匈牙利', 'Austria': '奧地利', 'Greece': '希臘', 'United States': '美國', 
    'Germany': '德國', 'United Kingdom': '英國', 'France': '法國', 'Australia': '澳洲', 
    'Denmark': '丹麥', 'Switzerland': '瑞士', 'Netherlands': '荷蘭', 'Belgium': '比利時', 
    'India': '印度', 'Canada': '加拿大', 'Sweden': '瑞典', 'Norway': '挪威', 
    'Spain': '西班牙', 'Italy': '義大利', 'Cuba': '古巴', 'South Africa': '南非', 
    'Finland': '芬蘭', 'Estonia': '愛沙尼亞', 'New Zealand': '紐西蘭', 'Brazil': '巴西', 
    'Japan': '日本', 'Luxembourg': '盧森堡', 'Argentina': '阿根廷', 'Poland': '波蘭', 
    'Portugal': '葡萄牙', 'Uruguay': '烏拉圭', 'Haiti': '海地', 'Egypt': '埃及', 
    'Philippines': '菲律賓', 'Ireland': '愛爾蘭', 'Chile': '智利', 'Latvia': '拉脫維亞', 
    'Mexico': '墨西哥', 'Turkey': '土耳其', 'Panama': '巴拿馬', 'Jamaica': '牙買加', 
    'Sri Lanka': '斯里蘭卡', 'Korea, South': '南韓', 'Puerto Rico*': '波多黎各', 'Peru': '秘魯', 
    'Iran': '伊朗', 'Trinidad and Tobago': '千里達及托巴哥', 'Venezuela': '委內瑞拉', 'Bulgaria': '保加利亞', 
    'Lebanon': '黎巴嫩', 'Iceland': '冰島', 'Pakistan': '巴基斯坦', 'Bahamas': '巴哈馬', 
    'Taiwan': '台灣 (中華台北)', 'Ethiopia': '衣索比亞', 'Morocco': '摩洛哥', 'Ghana': '迦納', 
    'Iraq': '伊拉克', 'Singapore': '新加坡', 'Tunisia': '突尼西亞', 'Kenya': '肯亞', 
    'Nigeria': '奈及利亞', 'Uganda': '烏干達', 'Cameroon': '喀麥隆', 'Mongolia': '蒙古', 
    'Korea, North': '北韓', 'Colombia': '哥倫比亞', 'Niger': '尼日', 'Thailand': '泰國', 
    'Bermuda*': '百慕達', 'Tanzania': '坦尚尼亞', 'Guyana': '蓋亞那', 'Zimbabwe': '辛巴威', 
    'China': '中國', "Cote d'Ivoire": '象牙海岸', 'Zambia': '尚比亞', 'Dominican Republic': '多明尼加', 
    'Algeria': '阿爾及利亞', 'Syria': '敘利亞', 'Suriname': '蘇利南', 'Costa Rica': '哥斯大黎加', 
    'Indonesia': '印尼', 'Senegal': '塞內加爾', 'Djibouti': '吉布地', 'Netherlands Antilles*': '荷屬安地列斯', 
    'Virgin Islands*': '美屬維京群島', 'Namibia': '納米比亞', 'Qatar': '卡達', 'Lithuania': '立陶宛', 
    'Malaysia': '馬來西亞', 'Croatia': '克羅埃西亞', 'Israel': '以色列', 'Slovenia': '斯洛維尼亞', 
    'Russia': '俄羅斯', 'Ukraine': '烏克蘭', 'Ecuador': '厄瓜多', 'Burundi': '蒲隆地', 
    'Mozambique': '莫桑比克', 'Czech Republic': '捷克', 'Belarus': '白俄羅斯', 'Tonga': '東加', 
    'Kazakhstan': '哈薩克', 'Uzbekistan': '烏茲別克', 'Slovakia': '斯洛伐克', 'Moldova': '摩爾多瓦', 
    'Georgia': '喬治亞', 'Hong Kong*': '香港', 'Armenia': '亞美尼亞', 'Azerbaijan': '亞塞拜然', 
    'Barbados': '巴貝多', 'Saudi Arabia': '沙烏地阿拉伯', 'Kyrgyzstan': '吉爾吉斯', 'Kuwait': '科威特', 
    'Vietnam': '越南', 'Macedonia': '北馬其頓', 'Serbia': '塞爾維亞', 'Eritrea': '厄利垂亞', 
    'Paraguay': '巴拉圭', 'United Arab Emirates': '阿拉伯聯合大公國', 'Sudan': '蘇丹', 'Mauritius': '模里西斯', 
    'Togo': '多哥', 'Tajikistan': '塔吉克', 'Afghanistan': '阿富汗', 'Bahrain': '巴林', 
    'Guatemala': '瓜地馬拉', 'Grenada': '格瑞那達', 'Botswana': '波札那', 'Cyprus': '賽普勒斯', 
    'Gabon': '加彭'
}

# 3. 讀取與處理資料
@st.cache_data
def load_data():
    df = pd.read_csv("SummerSD.csv")
    df['Year'] = df['Year'].astype(int)
    
    # 核心改動：將英文國家對照字典轉換成中文，若字典找不到則保留原名
    df['Country'] = df['Country'].map(COUNTRY_TRANSLATION).fillna(df['Country'])
    
    # 同步把性別也翻譯一下，讓介面更精緻
    gender_map = {'Men': '男子組', 'Women': '女子組'}
    df['Gender'] = df['Gender'].map(gender_map).fillna(df['Gender'])
    
    # 同步把獎牌翻譯一下
    medal_map = {'Gold': '金牌', 'Silver': '銀牌', 'Bronze': '銅牌'}
    df['Medal'] = df['Medal'].map(medal_map).fillna(df['Medal'])
    
    return df

try:
    df = load_data()
except FileNotFoundError:
    st.error("❌ 找不到 'SummerSD.csv' 檔案，請確保它與此程式碼放在同一個資料夾中。")
    st.stop()

# 4. 側邊欄控制面板 (Sidebar Filters)
st.sidebar.header("🎯 數據篩選面板")

years = sorted(df['Year'].unique())
selected_years = st.sidebar.multiselect("選擇奧運年份 (預選全部)", options=years, default=years)

genders = df['Gender'].unique().tolist()
selected_genders = st.sidebar.multiselect("選擇性別 (預選全部)", options=genders, default=genders)

medals = ['金牌', '銀牌', '銅牌']
selected_medals = st.sidebar.multiselect("選擇獎牌類型 (預選全部)", options=medals, default=medals)

# 根據篩選條件過濾資料
filtered_df = df[
    (df['Year'].isin(selected_years)) &
    (df['Gender'].isin(selected_genders)) &
    (df['Medal'].isin(selected_medals))
]

# 5. 主頁面標題
st.title("🏅 夏季奧運歷屆獎牌互動式分析 Dashboard")
st.write("---")

# 6. 關鍵指標卡片 (KPI Metrics)
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

# 7. 分頁設計 (Tabs)
tab1, tab2, tab3 = st.tabs(["📊 國家獎牌榜分析", "📈 國家歷年趨勢", "📋 原始資料檢視"])

# --- Tab 1: 國家獎牌榜分析 ---
with tab1:
    st.subheader("🥇 各國獎牌分佈 Top 10")
    
    if not filtered_df.empty:
        country_counts = (
            filtered_df.groupby(['Country', 'Medal'])
            .size()
            .reset_index(name='數量')
        )
        
        top_countries = (
            filtered_df['Country'].value_counts().head(10).index.tolist()
        )
        plot_df = country_counts[country_counts['Country'].isin(top_countries)]
        
        fig_bar = px.bar(
            plot_df,
            x='Country',
            y='數量',
            color='Medal',
            title="前 10 大獲獎國家獎牌結構圖",
            labels={'數量': '獎牌數量', 'Country': '國家', 'Medal': '獎牌'},
            color_discrete_map={'金牌': '#FFD700', '銀牌': '#C0C0C0', '銅牌': '#CD7F32'},
            category_orders={'Medal': ['金牌', '銀牌', '銅牌'], 'Country': top_countries}
        )
        fig_bar.update_layout(xaxis_categoryorder='total descending')
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.warning("⚠️ 目前篩選條件下無數據，請調整左側篩選面板。")

# --- Tab 2: 國家歷年趨勢 ---
with tab2:
    st.subheader("📈 單一國家歷年獎牌走勢")
    
    all_countries = sorted(df['Country'].dropna().unique())
    # 預設改選「美國」
    default_index = all_countries.index("美國") if "美國" in all_countries else 0
    target_country = st.selectbox("請選擇要分析的國家：", options=all_countries, index=default_index)
    
    country_df = df[df['Country'] == target_country]
    
    if not country_df.empty:
        trend_df = country_df.groupby(['Year', 'Medal']).size().reset_index(name='數量')
        fig_trend = px.line(
            trend_df,
            x='Year',
            y='數量',
            color='Medal',
            markers=True,
            title=f"【{target_country}】歷屆奧運獎牌數量變化趨勢",
            labels={'數量': '獎牌數', 'Year': '年份', 'Medal': '獎牌'},
            color_discrete_map={'金牌': '#FFD700', '銀牌': '#C0C0C0', '銅牌': '#CD7F32'}
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
            color_discrete_sequence=px.colors.sequential.YlOrRd_r
        )
        st.plotly_chart(fig_sport, use_container_width=True)
    else:
        st.info("該國家在當前篩選條件下未獲得獎牌。")

# --- Tab 3: 原始資料檢視 ---
with tab3:
    st.subheader("🔍 篩選後的原始資料明細")
    st.write(f"當前條件下共有 {len(filtered_df)} 筆得獎紀錄：")
    
    search_query = st.text_input("搜尋關鍵字（如選手姓名、運動項目、國家）：")
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