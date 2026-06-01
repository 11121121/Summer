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

# 定義現代感金銀銅進階配色 (霧金、銀灰、古銅)
MEDAL_COLORS = {
    '金牌': '#E5A93C',  # 霧金
    '銀牌': '#B0B7BD',  # 鈦金灰
    '銅牌': '#CD7F32'   # 古銅色
}

# 2. 國家中英文對照字典
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
    'Virgin Islands*': '美屬維京群島', 'Namibia': '納米比亞', 'Qatar': '卡達', 'Lithuania': '立宛陶', 
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

# 夏季奧運運動項目中英文對照字典
SPORT_TRANSLATION = {
    'Aquatics': '水上運動', 'Athletics': '田徑', 'Rowing': '划船', 'Basketball': '籃球', 
    'Shooting': '射擊', 'Gymnastics': '體操', 'Weightlifting': '舉重', 'Fencing': '擊劍', 
    'Wrestling': '角力', 'Cycling': '自由車', 'Sailing': '帆船', 'Equestrianism': '馬術', 
    'Tennis': '網球', 'Badminton': '羽球', 'Table Tennis': '桌球', 'Volleyball': '排球', 
    'Handball': '手球', 'Archery': '射箭', 'Judo': '柔道', 'Taekwondo': '跆拳道', 
    'Boxing': '拳擊', 'Canoeing': '輕艇', 'Football': '足球', 'Hockey': '曲棍球',
    'Modern Pentathlon': '現代五項', 'Triathlon': '鐵人三項', 'Golf': '高爾夫', 
    'Rugby Sevens': '七人制橄欖球', 'Rugby': '橄欖球', 'Tug of War': '拔河', 
    'Baseball': '棒球', 'Softball': '壘球', 'Cricket': '板球', 'Polo': '馬球', 
    'Lacrosse': '袋棍球', 'Ice Hockey': '冰球', 'Figure Skating': '花式滑冰',
    'Surfing': '衝浪', 'Skateboarding': '滑板', 'Sport Climbing': '運動攀登', 
    'Karate': '空手道', 'Breaking': '霹靂舞'
}

# 3. 讀取與處理資料
@st.cache_data
def load_data():
    df = pd.read_csv("SummerSD.csv")
    df['Year'] = df['Year'].astype(int)
    
    # 欄位中文化
    df['Country'] = df['Country'].map(COUNTRY_TRANSLATION).fillna(df['Country'])
    df['Sport'] = df['Sport'].map(SPORT_TRANSLATION).fillna(df['Sport'])
    
    gender_map = {'Men': '男子組', 'Women': '女子組'}
    df['Gender'] = df['Gender'].map(gender_map).fillna(df['Gender'])
    
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

# 7. 分頁設計
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 國家獎牌榜分析", 
    "📈 國家歷年趨勢", 
    "⏳ 歷年強權動態爭霸", 
    "🔬 奧運深度專題研究", 
    "📋 原始資料檢視"
])

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
            y='Country',           
            x='數量',              
            color='Medal',
            orientation='h',       
            title="前 10 大獲獎國家獎牌結構圖",
            labels={'數量': '獎牌數量', 'Country': '國家', 'Medal': '獎牌'},
            color_discrete_map=MEDAL_COLORS, 
            category_orders={'Medal': ['金牌', '銀牌', '銅牌'], 'Country': top_countries} 
        )
        fig_bar.update_layout(
            barmode='stack',
            xaxis_title="獎牌總數量",
            yaxis_title="國家 (依總數由上至下排名)",
            legend_title="獎牌類型",
            height=450
        )
        st.plotly_chart(fig_bar, use_container_width=True)
        
        st.write("---")
        
        # 強權項目實力矩陣熱圖
        st.subheader("🌡️ 強權國家 vs 運動項目：實力對比矩陣熱圖")
        top_sports = filtered_df['Sport'].value_counts().head(15).index.tolist()
        heatmap_data = filtered_df[
            (filtered_df['Country'].isin(top_countries)) & 
            (filtered_df['Sport'].isin(top_sports))
        ]
        
        if not heatmap_data.empty:
            heatmap_pivot = heatmap_data.groupby(['Sport', 'Country']).size().reset_index(name='獎牌數')
            
            fig_heatmap = px.density_heatmap(
                heatmap_pivot,
                x="Country",
                y="Sport",
                z="獎牌數",
                text_auto=True,
                color_continuous_scale="YlOrRd",
                title="Top 10 國家在 Top 15 運動項目中的實力矩陣 (格子顏色越深代表獎牌拿越多)",
                category_orders={"Country": top_countries, "Sport": top_sports}
            )
            fig_heatmap.update_layout(
                height=550, 
                xaxis_title="獲獎國家", 
                yaxis_title="運動項目",
                coloraxis_colorbar=dict(title="獎牌數")
            )
            st.plotly_chart(fig_heatmap, use_container_width=True)
    else:
        st.warning("⚠️ 目前篩選條件下無數據，請調整左側篩選面板。")

# --- Tab 2: 國家歷年趨勢 ---
with tab2:
    st.subheader("📈 單一國家歷年獎牌走勢")
    
    all_countries = sorted(df['Country'].dropna().unique())
    default_index = all_countries.index("美國") if "美國" in all_countries else 0
    target_country = st.selectbox("請選擇要分析的國家：", options=all_countries, index=default_index)
    
    country_df = df[
        (df['Country'] == target_country) &
        (df['Year'].isin(selected_years)) &
        (df['Gender'].isin(selected_genders)) &
        (df['Medal'].isin(selected_medals))
    ]
    
    if not country_df.empty:
        trend_df = country_df.groupby(['Year', 'Medal']).size().reset_index(name='數量')
        trend_df = trend_df.sort_values('Year')
        
        fig_trend = px.area(
            trend_df,
            x='Year',
            y='數量',
            color='Medal',
            title=f"【{target_country}】歷屆奧運獎牌數量變化趨勢",
            labels={'數量': '當屆獎牌數', 'Year': '年份', 'Medal': '獎牌'},
            color_discrete_map=MEDAL_COLORS,
            category_orders={'Medal': ['金牌', '銀牌', '銅牌']}
        )
        fig_trend.update_layout(
            xaxis=dict(type='category', categoryorder='category ascending'),
            yaxis_title="獲獎總數量 (外輪廓線為當屆總數)",
            hovermode="x unified",
            legend_title="獎牌類型"
        )
        st.plotly_chart(fig_trend, use_container_width=True)
        
        st.write("---")
        # 多維度交叉旭日圖
        st.subheader("🔬 獲獎結構深度探索 (點擊內圈可下鑽看男女組/獎牌細分)")
        
        top_5_sports = country_df['Sport'].value_counts().head(5).index.tolist()
        sunburst_df = country_df[country_df['Sport'].isin(top_5_sports)]
        
        fig_sunburst = px.sunburst(
            sunburst_df,
            path=['Sport', 'Gender', 'Medal'],  
            color='Medal',
            color_discrete_map=MEDAL_COLORS,
            title=f"【{target_country}】前五大擅長運動項目之交叉結構圖"
        )
        fig_sunburst.update_traces(sort=False)
        fig_sunburst.update_layout(height=550)
        st.plotly_chart(fig_sunburst, use_container_width=True)
    else:
        st.info("該國家在當前篩選條件下未獲得獎牌。")

# --- Tab 3: 歷年強權動態爭霸 ---
with tab3:
    st.subheader("⏳ 歷史強權動態爭霸戰")
    st.write("點擊圖形左下角的 **▶ Play 播放鍵**，觀看歷屆奧運各國實力版圖的興衰消長！")
    
    dynamic_df = df.groupby(['Year', 'Country', 'Medal']).size().reset_index(name='數量')
    dynamic_pivot = dynamic_df.pivot(index=['Year', 'Country'], columns='Medal', values='數量').reset_index().fillna(0)
    
    for col in ['金牌', '銀牌', '銅牌']:
        if col not in dynamic_pivot.columns:
            dynamic_pivot[col] = 0
            
    dynamic_pivot['總獎牌數'] = dynamic_pivot['金牌'] + dynamic_pivot['銀牌'] + dynamic_pivot['銅牌']
    dynamic_pivot = dynamic_pivot.sort_values('Year')
    
    fig_animation = px.scatter(
        dynamic_pivot,
        x="銀牌",           
        y="金牌",           
        animation_frame="Year",     
        animation_group="Country",   
        size="總獎牌數",             
        color="Country",             
        hover_name="Country",
        size_max=60,                 
        range_x=[-5, dynamic_pivot['銀牌'].max() + 5],  
        range_y=[-5, dynamic_pivot['金牌'].max() + 5],  
        title="歷屆奧運各國【金牌 vs 銀牌】動態消長軌跡",
        labels={'金牌': '金牌數量', '銀牌': '銀牌數量', 'Year': '年份'}
    )
    fig_animation.update_layout(showlegend=False, height=650)
    st.plotly_chart(fig_animation, use_container_width=True)

# --- Tab 4: 奧運深度專題研究 ---
with tab4:
    st.header("🔬 數據科學專題特輯")
    research_topic = st.radio(
        "💡 請選擇你想探索的奧運數據故事：",
        options=[
            "🥇 視角一：誰是「含金量」最高的效率強權？", 
            "🤼 視角二：單一運動項目的「世界霸主興衰史」", 
            "♀️ 視角三：歷史時間軸上的「奧運女力崛起軌跡」"
        ],
        horizontal=True
    )
    st.write("---")
    
    # 專題一：含金量效率排行 (💡 這裡已經修正完成！)
    if research_topic == "🥇 視角一：誰是「含金量」最高的效率強權？":
        st.subheader("🏆 各國獎牌「含金量與結構」大對決")
        
        eff_df = df.groupby(['Country', 'Medal']).size().reset_index(name='數量')
        eff_pivot = eff_df.pivot(index='Country', columns='Medal', values='數量').fillna(0).reset_index()
        eff_pivot['總數'] = eff_pivot['金牌'] + eff_pivot['銀牌'] + eff_pivot['銅牌']
        
        eff_top20 = eff_pivot[eff_pivot['總數'] >= 50].sort_values('總數', ascending=False).head(20)
        plot_eff_df = pd.melt(eff_top20, id_vars=['Country'], value_vars=['金牌', '銀牌', '銅牌'], value_name='數量')
        
        fig_eff = px.bar(
            plot_eff_df,
            x="Country",
            y="數量",
            color="Medal",
            title="前 20 大奪牌強權的獎牌含金量百分比結構圖",
            labels={'數量': '獎牌數量', 'Country': '國家', 'Medal': '獎牌類型'},
            color_discrete_map=MEDAL_COLORS,
            category_orders={'Medal': ['金牌', '銀牌', '銅牌']}
        )
        
        # 使用 update_layout 來設定百分比轉換
        fig_eff.update_layout(
            barmode='stack',
            barnorm='percent',
            yaxis_title="獎牌佔比 (%)", 
            height=500
        )
        st.plotly_chart(fig_eff, use_container_width=True)
        st.info("💡 觀察指南：金色區塊（金牌）越高的國家，代表其奪牌效率與金牌純度越高！")

    # 專題二：運動項目霸主興衰史
    elif research_topic == "🤼 視角二：單一運動項目的「世界霸主興衰史」":
        st.subheader("👑 運動項目國際版圖演進史")
        
        all_sports = sorted(df['Sport'].dropna().unique())
        default_sport_idx = all_sports.index("柔道") if "柔道" in all_sports else 0
        target_sport = st.selectbox("請選擇你想研究的運動項目：", options=all_sports, index=default_sport_idx)
        
        sport_hist = df[df['Sport'] == target_sport]
        sport_hist_grouped = sport_hist.groupby(['Year', 'Country']).size().reset_index(name='當屆奪牌數')
        
        top_countries_in_sport = sport_hist['Country'].value_counts().head(5).index.tolist()
        sport_hist_grouped['展示國家'] = sport_hist_grouped['Country'].apply(lambda x: x if x in top_countries_in_sport else '其他國家')
        
        fig_sport_hist = px.bar(
            sport_hist_grouped,
            x="Year",
            y="當屆奪牌數",
            color="展示國家",
            title=f"【{target_sport}】歷屆奧運獎牌版圖強權推移走勢",
            labels={'當屆奪牌數': '獎牌獲得數', 'Year': '年份'},
            color_discrete_sequence=px.colors.qualitative.Dark24
        )
        fig_sport_hist.update_layout(xaxis=dict(type='category'), barmode='stack', height=550)
        st.plotly_chart(fig_sport_hist, use_container_width=True)

    # 專題三：奧運女力崛起圖
    elif research_topic == "♀️ 視角三：歷史時間軸上的「奧運女力崛起軌跡」":
        st.subheader("🏃‍♀️ 現代奧運性別平等與女力崛起趨勢")
        
        gender_hist = df.groupby(['Year', 'Gender']).size().reset_index(name='獲獎人數')
        
        fig_gender = px.line(
            gender_hist,
            x="Year",
            y="獲獎人數",
            color="Gender",
            markers=True, 
            title="歷屆夏季奧運【男子組 vs 女子組】獲獎人數趨勢交叉對比",
            labels={'獲獎人數': '得獎運動員人次', 'Year': '年份', 'Gender': '組別'},
            color_discrete_map={'男子組': '#1f77b4', '女子組': '#e377c2'} 
        )
        fig_gender.update_layout(xaxis=dict(type='category'), hovermode="x unified")
        st.plotly_chart(fig_gender, use_container_width=True)

# --- Tab 5: 原始資料檢視 ---
with tab5:
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