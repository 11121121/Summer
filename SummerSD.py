import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ==========================================
# 1. 網頁基本設定
# ==========================================
st.set_page_config(
    page_title="夏季奧運歷屆獎牌互動式分析系統",
    page_icon="🏅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 定義金銀銅配色
MEDAL_COLORS = {
    '金牌': '#E5A93C',
    '銀牌': '#B0B7BD',
    '銅牌': '#CD7F32'
}

# ==========================================
# 國家顏色設定
# 日本固定紅色，其餘國家自動分配不重複顏色
# ==========================================
JAPAN_COLOR = '#E60012'

COUNTRY_COLOR_PALETTE = [
    '#1F77B4', '#FF7F0E', '#2CA02C', '#9467BD', '#8C564B',
    '#E377C2', '#7F7F7F', '#BCBD22', '#17BECF', '#393B79',
    '#637939', '#8C6D31', '#843C39', '#7B4173', '#3182BD',
    '#E6550D', '#31A354', '#756BB1', '#636363', '#9ECAE1',
    '#FDD0A2', '#A1D99B', '#BCBDDC', '#BDBDBD', '#C7E9C0',
    '#FDBF6F', '#CAB2D6', '#FFFF99', '#B15928', '#6A3D9A',
    '#B2DF8A', '#FB9A99', '#A6CEE3', '#33A02C', '#FB8072'
]

# 內建歷史事件智庫
OLYMPIC_HIST_STORIES = {
    "通用": {
        1916: "❌ 【一戰停辦】因第一次世界大戰全面爆發而被迫取消。",
        1940: "❌ 【二戰停辦】因第二次世界大戰（中日戰爭爆發）而宣布停辦。",
        1944: "❌ 【二戰停辦】因第二次世界大戰戰火蔓延，持續停辦。",
        1980: "⚠️ 【美歐大抵制】因蘇聯入侵阿富汗，美、日、韓等 60 國集體抵制莫斯科奧運！",
        1984: "⚠️ 【共產陣營報復】蘇聯、東德、古巴等集體抵制洛杉磯奧運，美國地主隊大獲全勝。",
        1992: "📉 【蘇聯解體】蘇聯解體，各國以「獨聯體」名義最後一次聯合參賽，隨後幾屆正式分裂。"
    },
    "柔道": {
        1964: "🇯🇵 【柔道初登場】柔道在東京奧運首次成為正式項目，日本展現恐怖制霸力。",
        1968: "❌ 【柔道消失之謎】因主辦國墨西哥未規劃且國際奧委會限制人數，柔道在這一屆被無情踢出奧運！直到 1972 年才回歸。",
        1980: "🥋 【日本消失之謎】日本因政治抵制缺席莫斯科奧運，導致當屆柔道總獎牌數慘烈萎縮！",
        1988: "🇰🇷 【南韓主場爆發】漢城奧運主場加持，南韓柔道隊創下隊史極佳紀錄。"
    }
}

# ==========================================
# 2. 中英文對照字典
# ==========================================
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
    'Iran': '伊朗', 'Trinidad and Tobago': '千里達及托巴哥', 'Venezuela': '委內瑞拉',
    'Bulgaria': '保加利亞', 'Lebanon': '黎巴嫩', 'Iceland': '冰島', 'Pakistan': '巴基斯坦',
    'Bahamas': '巴哈馬', 'Taiwan': '台灣 (中華台北)', 'Ethiopia': '衣索比亞',
    'Morocco': '摩洛哥', 'Ghana': '迦納', 'Iraq': '伊拉克', 'Singapore': '新加坡',
    'Tunisia': '突尼西亞', 'Kenya': '肯亞', 'Nigeria': '奈及利亞', 'Uganda': '烏干達',
    'Cameroon': '喀滅隆', 'Mongolia': '蒙古', 'Korea, North': '北韓',
    'Colombia': '哥倫比亞', 'Niger': '尼日', 'Thailand': '泰國', 'Bermuda*': '百慕達',
    'Tanzania': '坦尚尼亞', 'Guyana': '蓋亞那', 'Zimbabwe': '辛巴威', 'China': '中國',
    "Cote d'Ivoire": '象牙海岸', 'Zambia': '尚比亞', 'Dominican Republic': '多明尼加',
    'Algeria': '阿爾及利亞', 'Syria': '敘利亞', 'Suriname': '蘇利南',
    'Costa Rica': '哥斯大黎加', 'Indonesia': '印尼', 'Senegal': '塞內加爾',
    'Djibouti': '吉布地', 'Netherlands Antilles*': '荷屬安地列斯',
    'Virgin Islands*': '美屬維京群島', 'Namibia': '納米比亞', 'Qatar': '卡達',
    'Lithuania': '立宛陶', 'Malaysia': '馬來西亞', 'Croatia': '克羅埃西亞',
    'Israel': '以色列', 'Slovenia': '斯洛維尼亞', 'Russia': '俄羅斯',
    'Ukraine': '烏克蘭', 'Ecuador': '厄瓜多', 'Burundi': '蒲隆地',
    'Mozambique': '莫桑比克', 'Czech Republic': '捷克', 'Belarus': '白俄羅斯',
    'Tonga': '東加', 'Kazakhstan': '哈薩克', 'Uzbekistan': '烏茲別克',
    'Slovakia': '斯洛伐克', 'Moldova': '摩爾多瓦', 'Georgia': '喬治亞',
    'Hong Kong*': '香港', 'Armenia': '亞美尼亞', 'Azerbaijan': '亞塞拜然',
    'Barbados': '巴貝多', 'Saudi Arabia': '沙烏地阿拉伯', 'Kyrgyzstan': '吉爾吉斯',
    'Kuwait': '科威特', 'Vietnam': '越南', 'Macedonia': '北馬其頓',
    'Serbia': '塞爾維亞', 'Eritrea': '厄利垂亞', 'Paraguay': '巴拉圭',
    'United Arab Emirates': '阿拉伯聯合大公國', 'Sudan': '蘇丹',
    'Mauritius': '模里西斯', 'Togo': '多哥', 'Tajikistan': '塔吉克',
    'Afghanistan': '阿富汗', 'Bahrain': '巴林', 'Guatemala': '瓜地馬拉',
    'Grenada': '格瑞那達', 'Botswana': '波札那', 'Cyprus': '賽普勒斯',
    'Gabon': '加蓬'
}

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

# ==========================================
# 3. 讀取與處理資料
# ==========================================
@st.cache_data
def load_data():
    df = pd.read_csv("SummerSD.csv")
    df['Year'] = df['Year'].astype(int)

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

# ==========================================
# 4. 側邊欄控制面板
# ==========================================
st.sidebar.markdown("## 🎯 數據篩選面板")
st.sidebar.write("調整下方條件，右側圖表將即時連動更新。")
st.sidebar.write("---")

st.sidebar.markdown("### 📅 奧運歷史區間")
min_year = int(df['Year'].min())
max_year = int(df['Year'].max())

start_year, end_year = st.sidebar.slider(
    "選擇年份範圍：",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year),
    step=4
)

selected_years = [y for y in range(start_year, end_year + 1)]

st.sidebar.markdown("### 🏃‍♂️ 賽事組別")
gender_options = ["全部"] + df['Gender'].unique().tolist()
gender_selection = st.sidebar.selectbox("選擇性別組別：", options=gender_options, index=0)

if gender_selection == "全部":
    selected_genders = df['Gender'].unique().tolist()
else:
    selected_genders = [gender_selection]

st.sidebar.markdown("### 🎯 運動項目過濾")
all_sports_chinese = sorted(list(SPORT_TRANSLATION.values()))

sport_selection = st.sidebar.multiselect(
    "選擇運動項目 (預設全部)：",
    options=all_sports_chinese,
    default=[]
)

if not sport_selection:
    selected_sports = all_sports_chinese
else:
    selected_sports = sport_selection

st.sidebar.markdown("### 🏅 獎牌種類")
medal_options = ['金牌', '銀牌', '銅牌']

selected_medals = st.sidebar.multiselect(
    "選擇獎牌 (可多選)：",
    options=medal_options,
    default=medal_options
)

st.sidebar.markdown("### ⚙️ 圖表顯示設定")
top_n_countries = st.sidebar.slider(
    "國家榜單顯示數量 (Top N)：",
    min_value=5,
    max_value=30,
    value=10,
    step=5
)

if not selected_medals:
    selected_medals = medal_options

filtered_df = df[
    (df['Year'].isin(selected_years)) &
    (df['Gender'].isin(selected_genders)) &
    (df['Sport'].isin(selected_sports)) &
    (df['Medal'].isin(selected_medals))
]

st.sidebar.write("---")

# ==========================================
# 5. 主頁面標題與 KPI 指標卡
# ==========================================
st.title("🏅 夏季奧運歷屆獎牌互動式分析 Dashboard")
st.write("---")

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

# ==========================================
# 6. 多功能分頁設計
# ==========================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 國家獎牌榜分析",
    "📈 國家歷年趨勢",
    "⏳ 歷年強權動態爭霸",
    "🔬 奧運深度專題研究",
    "📋 原始資料檢視"
])

# ==========================================
# Tab 1: 國家獎牌榜分析
# ==========================================
with tab1:
    st.subheader(f"🥇 各國獎牌分佈 Top {top_n_countries}")

    if not filtered_df.empty:
        country_counts = filtered_df.groupby(['Country', 'Medal']).size().reset_index(name='數量')
        top_countries = filtered_df['Country'].value_counts().head(top_n_countries).index.tolist()
        plot_df = country_counts[country_counts['Country'].isin(top_countries)]

        fig_bar = px.bar(
            plot_df,
            y='Country',
            x='數量',
            color='Medal',
            orientation='h',
            title=f"前 {top_n_countries} 大獲獎國家獎牌結構圖",
            labels={'數量': '獎牌數量', 'Country': '國家', 'Medal': '獎牌'},
            color_discrete_map=MEDAL_COLORS,
            category_orders={
                'Medal': ['金牌', '銀牌', '銅牌'],
                'Country': top_countries
            }
        )

        fig_bar.update_layout(
            barmode='stack',
            height=450 + (top_n_countries * 5)
        )

        st.plotly_chart(fig_bar, use_container_width=True)

        st.write("---")
        st.subheader(f"🌡️ 強權國家 vs 運動項目：Top {top_n_countries} 實力對比矩陣熱圖")

        current_top_sports = filtered_df['Sport'].value_counts().head(15).index.tolist()

        heatmap_data = filtered_df[
            (filtered_df['Country'].isin(top_countries)) &
            (filtered_df['Sport'].isin(current_top_sports))
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
                category_orders={
                    "Country": top_countries,
                    "Sport": current_top_sports
                }
            )

            fig_heatmap.update_layout(height=550)
            st.plotly_chart(fig_heatmap, use_container_width=True)

    else:
        st.warning("⚠️ 目前篩選條件下無數據，請調整左側篩選面板。")

# ==========================================
# Tab 2: 國家歷年趨勢
# ==========================================
with tab2:
    st.subheader("📈 單一國家歷年獎牌走勢")

    all_countries = sorted(df['Country'].dropna().unique())
    default_index = all_countries.index("美國") if "美國" in all_countries else 0

    target_country = st.selectbox(
        "請選擇要分析的國家：",
        options=all_countries,
        index=default_index
    )

    country_df = df[
        (df['Country'] == target_country) &
        (df['Year'].isin(selected_years)) &
        (df['Gender'].isin(selected_genders)) &
        (df['Medal'].isin(selected_medals))
    ]

    if not country_df.empty:
        trend_df = country_df.groupby(['Year', 'Medal']).size().reset_index(name='數量').sort_values('Year')

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
            hovermode="x unified"
        )

        st.plotly_chart(fig_trend, use_container_width=True)

        st.write("---")
        st.subheader("🔬 獲獎結構深度探索")

        top_5_sports = country_df['Sport'].value_counts().head(5).index.tolist()
        sunburst_df = country_df[country_df['Sport'].isin(top_5_sports)]

        if not sunburst_df.empty:
            fig_sunburst = px.sunburst(
                sunburst_df,
                path=['Sport', 'Gender', 'Medal'],
                color='Medal',
                color_discrete_map=MEDAL_COLORS,
                title=f"【{target_country}】前五大擅長運動項目之交叉結構圖"
            )

            fig_sunburst.update_traces(sort=False)
            st.plotly_chart(fig_sunburst, use_container_width=True)

    else:
        st.info("該國家在當前篩選條件下未獲得獎牌。")

# ==========================================
# Tab 3: 歷年強權動態爭霸
# ==========================================
with tab3:
    st.subheader("📈 歷史對照印證：跨越百年的「奧運生命線」與地緣政治衝擊")
    st.write("這張圖表幫你即時對照歷史上所有停辦年與抵制年。")

    all_possible_years = sorted(list(range(1896, 2013, 4)))

    yearly_totals = df.groupby('Year').size().reset_index(name='總獲獎人數')

    full_year_df = pd.DataFrame({'Year': all_possible_years})
    line_df = pd.merge(full_year_df, yearly_totals, on='Year', how='left').fillna(0)

    fig_line_verify = go.Figure()

    fig_line_verify.add_trace(go.Scatter(
        x=line_df['Year'],
        y=line_df['總獲獎人數'],
        mode='lines+markers',
        name='每屆總獲獎人次',
        line=dict(color='#A30000', width=3),
        fill='tozeroy',
        fillcolor='rgba(163, 0, 0, 0.1)'
    ))

    annotations_main = [
        dict(
            x=1916,
            y=0,
            text="💥 1916 一戰停辦",
            showarrow=True,
            arrowhead=2,
            arrowcolor="black",
            xref="x",
            yref="y",
            ay=-40,
            font=dict(size=11),
            bgcolor="white",
            bordercolor="gray"
        ),
        dict(
            x=1942,
            y=0,
            text="💥 1940/1944 二戰停辦",
            showarrow=True,
            arrowhead=2,
            arrowcolor="black",
            xref="x",
            yref="y",
            ay=-80,
            font=dict(size=11),
            bgcolor="white",
            bordercolor="gray"
        ),
        dict(
            x=1980,
            y=yearly_totals[yearly_totals['Year'] == 1980]['總獲獎人數'].values[0] if 1980 in yearly_totals['Year'].values else 1000,
            text="⚠️ 1980 莫斯科大抵制<br>(美日藍營缺席)",
            showarrow=True,
            arrowhead=1,
            ax=-60,
            ay=-60,
            xref="x",
            yref="y",
            font=dict(size=10),
            bgcolor="#fff3cd",
            bordercolor="#ffeeba"
        ),
        dict(
            x=1984,
            y=yearly_totals[yearly_totals['Year'] == 1984]['總獲獎人數'].values[0] if 1984 in yearly_totals['Year'].values else 1200,
            text="⚠️ 1984 洛杉磯抵制<br>(蘇聯紅營報復)",
            showarrow=True,
            arrowhead=1,
            ax=60,
            ay=-110,
            xref="x",
            yref="y",
            font=dict(size=10),
            bgcolor="#fff3cd",
            bordercolor="#ffeeba"
        ),
        dict(
            x=1992,
            y=yearly_totals[yearly_totals['Year'] == 1992]['總獲獎人數'].values[0] if 1992 in yearly_totals['Year'].values else 1300,
            text="📉 1992 蘇聯解體<br>(獨聯體最後合體)",
            showarrow=True,
            arrowhead=1,
            ax=50,
            ay=-30,
            xref="x",
            yref="y",
            font=dict(size=11),
            bgcolor="white",
            bordercolor="gray"
        )
    ]

    fig_line_verify.update_layout(
        title="【數據印證】歷史大事件引發的奧運參賽人數雪崩與震盪",
        xaxis=dict(title="年份 (西元)", tickmode='linear', dtick=8),
        yaxis=dict(title="當屆獲獎總人數 (人次)"),
        annotations=annotations_main,
        height=380,
        margin=dict(t=50, b=50)
    )

    st.plotly_chart(fig_line_verify, use_container_width=True)

    st.write("---")

    st.subheader("⏳ 歷年強權動態爭霸戰 (金牌 vs 銀牌 追逐戰)")
    st.write("💡 請按下方的 ▶ Play 播放鍵，觀察各國奪牌變化。")

    dynamic_df = df.groupby(['Year', 'Country', 'Medal']).size().reset_index(name='數量')

    dynamic_pivot = dynamic_df.pivot(
        index=['Year', 'Country'],
        columns='Medal',
        values='數量'
    ).reset_index().fillna(0)

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
        range_x=[-5, dynamic_pivot['銀牌'].max() + 10],
        range_y=[-5, dynamic_pivot['金牌'].max() + 10],
        title="歷屆奧運各國奪牌效率動態消長軌跡",
        labels={
            '銀牌': '該屆銀牌總數',
            '金牌': '該屆金牌總數',
            '總獎牌數': '當屆總獎牌數'
        }
    )

    fig_animation.update_layout(showlegend=False, height=550)
    st.plotly_chart(fig_animation, use_container_width=True)

# ==========================================
# Tab 4: 奧運深度專題研究
# ==========================================
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

    if research_topic == "🥇 視角一：誰是「含金量」最高的效率強權？":
        st.subheader("🏆 各國獎牌「含金量與結構」大對決")

        eff_df = df.groupby(['Country', 'Medal']).size().reset_index(name='數量')

        eff_pivot = eff_df.pivot(
            index='Country',
            columns='Medal',
            values='數量'
        ).fillna(0).reset_index()

        for col in ['金牌', '銀牌', '銅牌']:
            if col not in eff_pivot.columns:
                eff_pivot[col] = 0

        eff_pivot['總數'] = eff_pivot['金牌'] + eff_pivot['銀牌'] + eff_pivot['銅牌']

        eff_top20 = eff_pivot[eff_pivot['總數'] >= 50].sort_values('總數', ascending=False).head(20)

        plot_eff_df = pd.melt(
            eff_top20,
            id_vars=['Country'],
            value_vars=['金牌', '銀牌', '銅牌'],
            value_name='數量'
        )

        fig_eff = px.bar(
            plot_eff_df,
            x="Country",
            y="數量",
            color="Medal",
            title="前 20 大奪牌強權的獎牌含金量百分比結構圖",
            color_discrete_map=MEDAL_COLORS
        )

        fig_eff.update_layout(
            barmode='stack',
            barnorm='percent',
            yaxis_title="獎牌佔比 (%)"
        )

        st.plotly_chart(fig_eff, use_container_width=True)

    elif research_topic == "🤼 視角二：單一運動項目的「世界霸主興衰史」":
        st.subheader(f"👑 運動項目國際版圖演進史 (當前動態展示前 {top_n_countries} 大強權)")

        all_sports = sorted(df['Sport'].dropna().unique())
        default_sport_idx = all_sports.index("柔道") if "柔道" in all_sports else 0

        target_sport = st.selectbox(
            "請選擇你想研究的運動項目：",
            options=all_sports,
            index=default_sport_idx
        )

        sport_hist = df[
            (df['Sport'] == target_sport) &
            (df['Medal'].isin(['金牌', '銀牌', '銅牌']))
        ]

        if not sport_hist.empty:
            # 先整理出每一年、每個國家的金銀銅數量
            medal_detail = sport_hist.groupby(
                ['Year', 'Country', 'Medal']
            ).size().reset_index(name='數量')

            sport_hist_grouped = medal_detail.pivot_table(
                index=['Year', 'Country'],
                columns='Medal',
                values='數量',
                aggfunc='sum',
                fill_value=0
            ).reset_index()

            # 確保金銀銅欄位都存在
            for col in ['金牌', '銀牌', '銅牌']:
                if col not in sport_hist_grouped.columns:
                    sport_hist_grouped[col] = 0

            # 計算每一年、每個國家的總獎牌數
            sport_hist_grouped['當屆奪牌數'] = (
                sport_hist_grouped['金牌'] +
                sport_hist_grouped['銀牌'] +
                sport_hist_grouped['銅牌']
            )

            sport_hist_grouped = sport_hist_grouped.sort_values('Year')

            # 找出該運動項目前 N 名國家，其餘歸類為其他國家
            top_countries_in_sport = (
                sport_hist['Country']
                .value_counts()
                .head(top_n_countries)
                .index
                .tolist()
            )

            sport_hist_grouped['展示國家'] = sport_hist_grouped['Country'].apply(
                lambda x: x if x in top_countries_in_sport else '其他國家'
            )

            # 其他國家重新加總
            sport_hist_grouped = sport_hist_grouped.groupby(
                ['Year', '展示國家'],
                as_index=False
            )[['金牌', '銀牌', '銅牌', '當屆奪牌數']].sum()

            color_order = top_countries_in_sport + ['其他國家']

            # ==========================================
            # 自動產生不重複國家顏色
            # 日本固定紅色
            # ==========================================
            country_color_map = {}
            palette_index = 0

            for country in color_order:
                if country == '日本':
                    country_color_map[country] = JAPAN_COLOR
                else:
                    # 跳過和日本一樣的紅色
                    while COUNTRY_COLOR_PALETTE[palette_index % len(COUNTRY_COLOR_PALETTE)] == JAPAN_COLOR:
                        palette_index += 1

                    country_color_map[country] = COUNTRY_COLOR_PALETTE[
                        palette_index % len(COUNTRY_COLOR_PALETTE)
                    ]
                    palette_index += 1

            # ==========================================
            # 重點：
            # 1. 用 go.Bar 才能穩定顯示 hover 金銀銅
            # 2. marker_color 使用 country_color_map，避免顏色重複
            # ==========================================
            fig_sport_hist = go.Figure()

            for country in color_order:
                country_data = sport_hist_grouped[
                    sport_hist_grouped['展示國家'] == country
                ].copy()

                if country_data.empty:
                    continue

                fig_sport_hist.add_trace(go.Bar(
                    x=country_data['Year'],
                    y=country_data['當屆奪牌數'],
                    name=country,
                    marker_color=country_color_map.get(country),
                    customdata=country_data[
                        ['金牌', '銀牌', '銅牌', '當屆奪牌數']
                    ].values,
                    hovertemplate=(
                        "<b>%{fullData.name}</b><br>" +
                        "年份：%{x}<br>" +
                        "金牌：%{customdata[0]} 面<br>" +
                        "銀牌：%{customdata[1]} 面<br>" +
                        "銅牌：%{customdata[2]} 面<br>" +
                        "總獎牌數：%{customdata[3]} 面" +
                        "<extra></extra>"
                    )
                ))

            fig_sport_hist.update_layout(
                title=f"【{target_sport}】歷屆奧運獎牌版圖強權推移走勢（日本固定紅色，其餘國家不重複）",
                xaxis=dict(
                    title="年份",
                    type='linear',
                    tickmode='linear',
                    dtick=4,
                    range=[1962, 2014]
                ),
                yaxis=dict(title="真正獎牌數 (面)"),
                legend_title_text="國家/地區",
                barmode='stack',
                height=550,
                hovermode='closest'
            )

            st.plotly_chart(fig_sport_hist, use_container_width=True)

            st.markdown("### 🔍 歷史顯微鏡：解密大事件背景與數據起伏原因")
            st.write("下方選單已過濾並只顯示停辦與重大地緣政治事件年，點選即可查看背後原因：")

            story_years = list(OLYMPIC_HIST_STORIES["通用"].keys())

            if target_sport in OLYMPIC_HIST_STORIES:
                story_years += list(OLYMPIC_HIST_STORIES[target_sport].keys())

            only_critical_years = sorted(list(set(story_years)))

            selected_inspect_year = st.selectbox(
                "🗺️ 選擇關鍵歷史年份：",
                options=only_critical_years,
                index=only_critical_years.index(1968) if 1968 in only_critical_years else 0
            )

            story_text = ""

            if (
                target_sport in OLYMPIC_HIST_STORIES and
                selected_inspect_year in OLYMPIC_HIST_STORIES[target_sport]
            ):
                story_text += f"{OLYMPIC_HIST_STORIES[target_sport][selected_inspect_year]}\n\n"

            if selected_inspect_year in OLYMPIC_HIST_STORIES["通用"]:
                story_text += f"{OLYMPIC_HIST_STORIES['通用'][selected_inspect_year]}"

            st.info(story_text)

            st.markdown("#### 📉 該項目歷史事件與數據起伏印證圖表")
            st.write(
                f"以下折線圖單獨抽離出【{target_sport}】項目的歷屆獲獎總數。"
                f"你可以直接對照上方選擇的【{selected_inspect_year}年】事件。"
            )

            sport_yearly = sport_hist.groupby('Year').size().reset_index(name='該項獲獎總數')

            sport_line_df = pd.merge(
                pd.DataFrame({'Year': all_possible_years}),
                sport_yearly,
                on='Year',
                how='left'
            ).fillna(0)

            fig_micro_verify = go.Figure()

            fig_micro_verify.add_trace(go.Scatter(
                x=sport_line_df['Year'],
                y=sport_line_df['該項獲獎總數'],
                mode='lines+markers',
                name=f'{target_sport}歷屆獎牌數',
                line=dict(color='#005B94', width=3),
                fill='tozeroy',
                fillcolor='rgba(0, 91, 148, 0.1)'
            ))

            current_year_val = sport_line_df[
                sport_line_df['Year'] == selected_inspect_year
            ]['該項獲獎總數'].values

            if len(current_year_val) > 0:
                fig_micro_verify.add_trace(go.Scatter(
                    x=[selected_inspect_year],
                    y=[current_year_val[0]],
                    mode='markers',
                    name='當前檢視年份',
                    marker=dict(color='red', size=12, symbol='triangle-up')
                ))

            fig_micro_verify.update_layout(
                title=f"【歷史顯微鏡對照】{target_sport} 歷年真正獎牌起伏趨勢",
                xaxis=dict(
                    title="年份",
                    tickmode='linear',
                    dtick=4,
                    range=[1960, 2014]
                ),
                yaxis=dict(title="真實獎牌總數 (面)"),
                height=300,
                showlegend=False,
                margin=dict(t=40, b=40)
            )

            st.plotly_chart(fig_micro_verify, use_container_width=True)

        else:
            st.info("該運動項目無相關歷史獲獎數據。")

    elif research_topic == "♀️ 視角三：歷史時間軸上的「奧運女力崛起軌跡」":
        st.subheader("🏃‍♀️ 現代奧運性別平等與女力崛起趨勢")

        gender_hist = df.groupby(['Year', 'Gender']).size().reset_index(name='獲獎人數')

        fig_gender = px.line(
            gender_hist,
            x="Year",
            y="獲獎人數",
            color="Gender",
            markers=True,
            color_discrete_map={
                '男子組': '#1f77b4',
                '女子組': '#e377c2'
            }
        )

        fig_gender.update_layout(
            xaxis=dict(type='category'),
            hovermode="x unified"
        )

        st.plotly_chart(fig_gender, use_container_width=True)

# ==========================================
# Tab 5: 原始資料檢視
# ==========================================
with tab5:
    st.subheader("🔍 篩選後的原始資料明細")

    search_query = st.text_input("搜尋關鍵字：")

    if search_query:
        display_df = filtered_df[
            filtered_df.astype(str).apply(
                lambda row: row.str.contains(search_query, case=False)
            ).any(axis=1)
        ]
    else:
        display_df = filtered_df

    st.dataframe(display_df, use_container_width=True)