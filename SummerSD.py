import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# =========================
# 頁面設定
# =========================
st.set_page_config(
    page_title="夏季奧運獎牌視覺化分析",
    page_icon="🏅",
    layout="wide"
)

# =========================
# 中文對照表
# =========================
sport_name_map = {
    "Aquatics": "水上運動",
    "Archery": "射箭",
    "Athletics": "田徑",
    "Badminton": "羽球",
    "Baseball": "棒球",
    "Basketball": "籃球",
    "Basque Pelota": "巴斯克回力球",
    "Boxing": "拳擊",
    "Canoe": "輕艇",
    "Canoe / Kayak": "輕艇／皮艇",
    "Cricket": "板球",
    "Croquet": "槌球",
    "Cycling": "自由車",
    "Equestrian": "馬術",
    "Fencing": "擊劍",
    "Football": "足球",
    "Golf": "高爾夫",
    "Gymnastics": "體操",
    "Handball": "手球",
    "Hockey": "曲棍球",
    "Ice Hockey": "冰上曲棍球",
    "Jeu de paume": "室內網球",
    "Judo": "柔道",
    "Lacrosse": "袋棍球",
    "Modern Pentathlon": "現代五項",
    "Polo": "馬球",
    "Rackets": "拍牆球",
    "Roque": "羅克球",
    "Rowing": "划船",
    "Rugby": "橄欖球",
    "Sailing": "帆船",
    "Shooting": "射擊",
    "Skating": "滑冰",
    "Softball": "壘球",
    "Table Tennis": "桌球",
    "Taekwondo": "跆拳道",
    "Tennis": "網球",
    "Triathlon": "鐵人三項",
    "Tug of War": "拔河",
    "Volleyball": "排球",
    "Water Motorsports": "水上摩托運動",
    "Weightlifting": "舉重",
    "Wrestling": "角力"
}

gender_name_map = {
    "Men": "男性",
    "Women": "女性",
    "Mixed": "混合"
}

medal_name_map = {
    "Gold": "金牌",
    "Silver": "銀牌",
    "Bronze": "銅牌"
}

country_name_map = {
    "Afghanistan": "阿富汗",
    "Algeria": "阿爾及利亞",
    "Argentina": "阿根廷",
    "Armenia": "亞美尼亞",
    "Australia": "澳洲",
    "Austria": "奧地利",
    "Azerbaijan": "亞塞拜然",
    "Bahamas": "巴哈馬",
    "Bahrain": "巴林",
    "Barbados": "巴貝多",
    "Belarus": "白俄羅斯",
    "Belgium": "比利時",
    "Bermuda*": "百慕達",
    "Botswana": "波札那",
    "Brazil": "巴西",
    "Bulgaria": "保加利亞",
    "Burundi": "蒲隆地",
    "Cameroon": "喀麥隆",
    "Canada": "加拿大",
    "Chile": "智利",
    "China": "中國",
    "Colombia": "哥倫比亞",
    "Costa Rica": "哥斯大黎加",
    "Cote d'Ivoire": "象牙海岸",
    "Croatia": "克羅埃西亞",
    "Cuba": "古巴",
    "Cyprus": "賽普勒斯",
    "Czech Republic": "捷克",
    "Denmark": "丹麥",
    "Djibouti": "吉布地",
    "Dominican Republic": "多明尼加",
    "Ecuador": "厄瓜多",
    "Egypt": "埃及",
    "Eritrea": "厄利垂亞",
    "Estonia": "愛沙尼亞",
    "Ethiopia": "衣索比亞",
    "Finland": "芬蘭",
    "France": "法國",
    "Gabon": "加彭",
    "Georgia": "喬治亞",
    "Germany": "德國",
    "Ghana": "迦納",
    "Greece": "希臘",
    "Grenada": "格瑞那達",
    "Guatemala": "瓜地馬拉",
    "Guyana": "蓋亞那",
    "Haiti": "海地",
    "Hong Kong*": "香港",
    "Hungary": "匈牙利",
    "Iceland": "冰島",
    "India": "印度",
    "Indonesia": "印尼",
    "Iran": "伊朗",
    "Iraq": "伊拉克",
    "Ireland": "愛爾蘭",
    "Israel": "以色列",
    "Italy": "義大利",
    "Jamaica": "牙買加",
    "Japan": "日本",
    "Jordan": "約旦",
    "Kazakhstan": "哈薩克",
    "Kenya": "肯亞",
    "Korea, North": "北韓",
    "Korea, South": "南韓",
    "Kuwait": "科威特",
    "Kyrgyzstan": "吉爾吉斯",
    "Latvia": "拉脫維亞",
    "Lebanon": "黎巴嫩",
    "Liechtenstein": "列支敦斯登",
    "Lithuania": "立陶宛",
    "Luxembourg": "盧森堡",
    "Macedonia": "北馬其頓",
    "Malaysia": "馬來西亞",
    "Mauritius": "模里西斯",
    "Mexico": "墨西哥",
    "Moldova": "摩爾多瓦",
    "Mongolia": "蒙古",
    "Montenegro": "蒙特內哥羅",
    "Morocco": "摩洛哥",
    "Mozambique": "莫三比克",
    "Namibia": "納米比亞",
    "Netherlands": "荷蘭",
    "Netherlands Antilles*": "荷屬安地列斯",
    "New Zealand": "紐西蘭",
    "Niger": "尼日",
    "Nigeria": "奈及利亞",
    "Norway": "挪威",
    "Pakistan": "巴基斯坦",
    "Panama": "巴拿馬",
    "Paraguay": "巴拉圭",
    "Peru": "秘魯",
    "Philippines": "菲律賓",
    "Poland": "波蘭",
    "Portugal": "葡萄牙",
    "Puerto Rico*": "波多黎各",
    "Qatar": "卡達",
    "Russia": "俄羅斯",
    "Saudi Arabia": "沙烏地阿拉伯",
    "Senegal": "塞內加爾",
    "Serbia": "塞爾維亞",
    "Singapore": "新加坡",
    "Slovakia": "斯洛伐克",
    "Slovenia": "斯洛維尼亞",
    "South Africa": "南非",
    "Spain": "西班牙",
    "Sri Lanka": "斯里蘭卡",
    "Sudan": "蘇丹",
    "Suriname": "蘇利南",
    "Sweden": "瑞典",
    "Switzerland": "瑞士",
    "Syria": "敘利亞",
    "Taiwan": "臺灣",
    "Tajikistan": "塔吉克",
    "Tanzania": "坦尚尼亞",
    "Thailand": "泰國",
    "Togo": "多哥",
    "Tonga": "東加",
    "Trinidad and Tobago": "千里達及托巴哥",
    "Tunisia": "突尼西亞",
    "Turkey": "土耳其",
    "Uganda": "烏干達",
    "Ukraine": "烏克蘭",
    "United Arab Emirates": "阿拉伯聯合大公國",
    "United Kingdom": "英國",
    "United States": "美國",
    "Uruguay": "烏拉圭",
    "Uzbekistan": "烏茲別克",
    "Venezuela": "委內瑞拉",
    "Vietnam": "越南",
    "Virgin Islands*": "美屬維京群島",
    "Zambia": "尚比亞",
    "Zimbabwe": "辛巴威",
    "Soviet Union": "蘇聯",
    "East Germany": "東德",
    "West Germany": "西德",
    "Yugoslavia": "南斯拉夫",
    "Czechoslovakia": "捷克斯洛伐克",
    "Unified Team": "獨聯體",
    "Australasia": "澳大拉西亞",
    "Bohemia": "波希米亞",
    "Mixed Team": "混合代表隊",
    "Independent Olympic Participants": "獨立奧林匹克參賽者",
    "British West Indies": "英屬西印度群島",
    "Unknown": "未知國家",
    "Unknown Country": "未知國家",
    "未知國家": "未知國家"
}

code_to_country_chinese = {
    "AFG": "阿富汗",
    "ALG": "阿爾及利亞",
    "ARG": "阿根廷",
    "ARM": "亞美尼亞",
    "ANZ": "澳大拉西亞",
    "AUS": "澳洲",
    "AUT": "奧地利",
    "AZE": "亞塞拜然",
    "BAH": "巴哈馬",
    "BRN": "巴林",
    "BAR": "巴貝多",
    "BLR": "白俄羅斯",
    "BEL": "比利時",
    "BER": "百慕達",
    "BOT": "波札那",
    "BRA": "巴西",
    "BUL": "保加利亞",
    "BDI": "蒲隆地",
    "CMR": "喀麥隆",
    "CAN": "加拿大",
    "CHI": "智利",
    "CHN": "中國",
    "COL": "哥倫比亞",
    "CRC": "哥斯大黎加",
    "CIV": "象牙海岸",
    "CRO": "克羅埃西亞",
    "CUB": "古巴",
    "CYP": "賽普勒斯",
    "CZE": "捷克",
    "DEN": "丹麥",
    "DJI": "吉布地",
    "DOM": "多明尼加",
    "ECU": "厄瓜多",
    "EGY": "埃及",
    "ERI": "厄利垂亞",
    "EST": "愛沙尼亞",
    "ETH": "衣索比亞",
    "FIN": "芬蘭",
    "FRA": "法國",
    "GAB": "加彭",
    "GEO": "喬治亞",
    "GER": "德國",
    "GDR": "東德",
    "FRG": "西德",
    "GHA": "迦納",
    "GRE": "希臘",
    "GRN": "格瑞那達",
    "GUA": "瓜地馬拉",
    "GUY": "蓋亞那",
    "HAI": "海地",
    "HKG": "香港",
    "HUN": "匈牙利",
    "ISL": "冰島",
    "IND": "印度",
    "INA": "印尼",
    "IRI": "伊朗",
    "IRQ": "伊拉克",
    "IRL": "愛爾蘭",
    "ISR": "以色列",
    "ITA": "義大利",
    "JAM": "牙買加",
    "JPN": "日本",
    "JOR": "約旦",
    "KAZ": "哈薩克",
    "KEN": "肯亞",
    "KOR": "南韓",
    "PRK": "北韓",
    "KUW": "科威特",
    "KGZ": "吉爾吉斯",
    "LAT": "拉脫維亞",
    "LIB": "黎巴嫩",
    "LTU": "立陶宛",
    "LUX": "盧森堡",
    "MKD": "北馬其頓",
    "MAS": "馬來西亞",
    "MRI": "模里西斯",
    "MEX": "墨西哥",
    "MDA": "摩爾多瓦",
    "MGL": "蒙古",
    "MNE": "蒙特內哥羅",
    "MAR": "摩洛哥",
    "MOZ": "莫三比克",
    "NAM": "納米比亞",
    "NED": "荷蘭",
    "AHO": "荷屬安地列斯",
    "NZL": "紐西蘭",
    "NIG": "尼日",
    "NGR": "奈及利亞",
    "NOR": "挪威",
    "PAK": "巴基斯坦",
    "PAN": "巴拿馬",
    "PAR": "巴拉圭",
    "PER": "秘魯",
    "PHI": "菲律賓",
    "POL": "波蘭",
    "POR": "葡萄牙",
    "PUR": "波多黎各",
    "QAT": "卡達",
    "RUS": "俄羅斯",
    "RU1": "俄羅斯",
    "KSA": "沙烏地阿拉伯",
    "SEN": "塞內加爾",
    "SRB": "塞爾維亞",
    "SIN": "新加坡",
    "SGP": "新加坡",
    "SVK": "斯洛伐克",
    "SLO": "斯洛維尼亞",
    "RSA": "南非",
    "ESP": "西班牙",
    "SRI": "斯里蘭卡",
    "SUD": "蘇丹",
    "SUR": "蘇利南",
    "SWE": "瑞典",
    "SUI": "瑞士",
    "SYR": "敘利亞",
    "TPE": "臺灣",
    "TJK": "塔吉克",
    "TAN": "坦尚尼亞",
    "THA": "泰國",
    "TOG": "多哥",
    "TGA": "東加",
    "TRI": "千里達及托巴哥",
    "TTO": "千里達及托巴哥",
    "TUN": "突尼西亞",
    "TUR": "土耳其",
    "UGA": "烏干達",
    "UKR": "烏克蘭",
    "UAE": "阿拉伯聯合大公國",
    "GBR": "英國",
    "USA": "美國",
    "URU": "烏拉圭",
    "UZB": "烏茲別克",
    "VEN": "委內瑞拉",
    "VIE": "越南",
    "ISV": "美屬維京群島",
    "ZAM": "尚比亞",
    "ZIM": "辛巴威",
    "URS": "蘇聯",
    "YUG": "南斯拉夫",
    "TCH": "捷克斯洛伐克",
    "EUA": "獨聯體",
    "EUN": "獨聯體",
    "ZZX": "混合代表隊",
    "BOH": "波希米亞",
    "IOP": "獨立奧林匹克參賽者",
    "BWI": "英屬西印度群島"
}

# =========================
# 獎牌顏色
# =========================
medal_colors = {
    "金牌": "#FFD700",
    "銀牌": "#1F77B4",
    "銅牌": "#D95F02"
}

plot_config = {
    "displayModeBar": False
}

# =========================
# 歷史事件與背景說明
# =========================
event_data = pd.DataFrame({
    "年份": [1896, 1900, 1916, 1940, 1944, 1964, 1980, 1984, 1992, 2000, 2012],
    "事件類型": [
        "奧運發展",
        "性別參與",
        "重大事件",
        "重大事件",
        "重大事件",
        "項目加入",
        "政治事件",
        "政治事件",
        "項目加入",
        "性別參與",
        "性別參與"
    ],
    "事件說明": [
        "第一屆現代夏季奧運舉行，早期項目與參賽國家數較少。",
        "女性首次參加奧運，但參賽人數與項目仍然有限。",
        "因第一次世界大戰影響，原訂奧運取消。",
        "因第二次世界大戰影響，原訂奧運取消。",
        "因第二次世界大戰影響，原訂奧運取消。",
        "柔道在東京奧運成為正式競賽項目，增加新的獎牌來源。",
        "莫斯科奧運受到部分國家抵制，影響當年參賽與獎牌分布。",
        "洛杉磯奧運受到部分國家抵制，影響當年參賽與獎牌分布。",
        "女子柔道成為正式奧運項目，女性獎牌機會增加。",
        "女子舉重成為正式奧運項目，女性競賽項目持續增加。",
        "倫敦奧運女性參與程度提高，女性運動發展更加受到重視。"
    ],
    "對獎牌資料的可能影響": [
        "早期獎牌資料量較少，國家與項目分布較集中。",
        "早期女性獎牌資料較少，導致整體男性獎牌數明顯較多。",
        "該年沒有獎牌資料，會造成時間序列中斷。",
        "該年沒有獎牌資料，會造成時間序列中斷。",
        "該年沒有獎牌資料，會造成時間序列中斷。",
        "新增項目後，相關國家開始有新的獎牌機會。",
        "部分國家缺席，可能造成特定國家獎牌數下降或其他國家上升。",
        "部分國家缺席，可能造成特定國家獎牌數下降或其他國家上升。",
        "女性獎牌資料增加，性別分布逐漸改變。",
        "女性項目增加，使女性獎牌紀錄持續累積。",
        "女性參賽機會提高，有助於解釋性別獎牌分布的變化。"
    ]
})

# =========================
# 讀取資料
# =========================
@st.cache_data
def load_data():
    df = pd.read_csv("SummerSD.csv")

    if "Unnamed: 0" in df.columns:
        df = df.drop(columns=["Unnamed: 0"])

    df["Code"] = df["Code"].fillna("Unknown").astype(str).str.strip().str.upper()
    df["Country"] = df["Country"].fillna("Unknown").astype(str).str.strip()

    df["Country"] = df["Country"].replace({
        "": "Unknown",
        "nan": "Unknown",
        "None": "Unknown"
    })

    df["Sport"] = df["Sport"].fillna("未知項目")
    df["Gender"] = df["Gender"].fillna("未知性別")
    df["Medal"] = df["Medal"].fillna("未知獎牌")
    df["City"] = df["City"].fillna("未知城市")
    df["Discipline"] = df["Discipline"].fillna("未知分項")
    df["Athlete"] = df["Athlete"].fillna("未知選手")
    df["Event"] = df["Event"].fillna("未知比賽項目")

    df["運動項目"] = df["Sport"].map(sport_name_map).fillna(df["Sport"])
    df["性別"] = df["Gender"].map(gender_name_map).fillna(df["Gender"])
    df["獎牌種類"] = df["Medal"].map(medal_name_map).fillna(df["Medal"])

    df["國家"] = df["Country"].map(country_name_map)
    df["國家"] = df["國家"].fillna(df["Code"].map(code_to_country_chinese))
    df["國家"] = df["國家"].fillna(df["Country"])
    df.loc[df["國家"].isin(["Unknown", "Unknown Country", "未知國家"]), "國家"] = df["Code"].map(code_to_country_chinese)
    df["國家"] = df["國家"].fillna("未知國家")

    return df


df = load_data()

# =========================
# 標題
# =========================
st.title("🏅 夏季奧運獎牌視覺化分析")

st.markdown(
    """
    ### 114-2 運動大數據與視覺化分析專題研究 / 姓名：林宥均
    """
)

st.write("本系統使用夏季奧運獎牌資料，分析不同年份、國家、運動項目、性別與獎牌表現。")

# =========================
# 側邊欄
# =========================
st.sidebar.title("📌 功能選單")

page = st.sidebar.radio(
    "選擇分析頁面",
    [
        "總覽儀表板",
        "國家分析",
        "運動項目分析",
        "時間趨勢分析",
        "酷炫互動圖",
        "背後原因解讀",
        "資料表"
    ]
)

st.sidebar.divider()
st.sidebar.header("🔍 篩選條件")

year_list = sorted(df["Year"].dropna().unique())

selected_year_range = st.sidebar.slider(
    "選擇年份範圍",
    min_value=int(min(year_list)),
    max_value=int(max(year_list)),
    value=(int(min(year_list)), int(max(year_list))),
    step=4
)

top_n_country = st.sidebar.slider(
    "選擇顯示前幾名國家",
    min_value=3,
    max_value=30,
    value=5,
    step=1
)

sport_list = sorted(df["運動項目"].unique())
selected_sports = st.sidebar.multiselect(
    "選擇運動項目",
    sport_list,
    default=sport_list
)

gender_list = sorted(df["性別"].unique())
selected_gender = st.sidebar.multiselect(
    "選擇性別",
    gender_list,
    default=gender_list
)

medal_list = ["金牌", "銀牌", "銅牌"]
selected_medals = st.sidebar.multiselect(
    "選擇獎牌種類",
    medal_list,
    default=medal_list
)

# =========================
# 篩選資料
# =========================
filtered_df = df[
    (df["Year"] >= selected_year_range[0]) &
    (df["Year"] <= selected_year_range[1]) &
    (df["運動項目"].isin(selected_sports)) &
    (df["性別"].isin(selected_gender)) &
    (df["獎牌種類"].isin(selected_medals))
]

if filtered_df.empty:
    st.warning("目前篩選條件下沒有資料，請重新選擇篩選條件。")
    st.stop()

# =========================
# 共用統計
# =========================
gold_count = filtered_df[filtered_df["獎牌種類"] == "金牌"].shape[0]
silver_count = filtered_df[filtered_df["獎牌種類"] == "銀牌"].shape[0]
bronze_count = filtered_df[filtered_df["獎牌種類"] == "銅牌"].shape[0]
total_count = filtered_df.shape[0]

country_count = filtered_df["國家"].nunique()
sport_count_total = filtered_df["運動項目"].nunique()
athlete_count = filtered_df["Athlete"].nunique()

country_medals = (
    filtered_df
    .groupby(["國家", "Country", "Code", "獎牌種類"])
    .size()
    .reset_index(name="數量")
)

country_pivot = country_medals.pivot_table(
    index=["國家", "Country", "Code"],
    columns="獎牌種類",
    values="數量",
    fill_value=0
).reset_index()

for medal in ["金牌", "銀牌", "銅牌"]:
    if medal not in country_pivot.columns:
        country_pivot[medal] = 0

country_pivot["總獎牌數"] = country_pivot["金牌"] + country_pivot["銀牌"] + country_pivot["銅牌"]

country_pivot = country_pivot.sort_values(
    by=["金牌", "銀牌", "銅牌", "總獎牌數"],
    ascending=False
)

top_country_names = country_pivot.head(top_n_country)["國家"].tolist()

# =========================
# 總覽儀表板
# =========================
if page == "總覽儀表板":
    st.subheader("📊 整體資料統計")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🥇 金牌數", gold_count)
    col2.metric("🥈 銀牌數", silver_count)
    col3.metric("🥉 銅牌數", bronze_count)
    col4.metric("🏅 總獎牌數", total_count)

    col5, col6, col7, col8 = st.columns(4)
    col5.metric("📄 資料筆數", f"{len(filtered_df):,}")
    col6.metric("🌍 國家數", country_count)
    col7.metric("⚽ 運動項目數", sport_count_total)
    col8.metric("👤 選手數", athlete_count)

    st.divider()

    st.subheader("🌍 各國獎牌分布地圖")

    fig_map = px.choropleth(
        country_pivot,
        locations="Code",
        color="總獎牌數",
        hover_name="國家",
        hover_data={
            "金牌": True,
            "銀牌": True,
            "銅牌": True,
            "總獎牌數": True,
            "Country": False,
            "Code": False
        },
        color_continuous_scale="YlOrRd",
        title="各國總獎牌數分布",
        labels={"總獎牌數": "總獎牌數"}
    )

    fig_map.update_layout(
        geo=dict(showframe=False, showcoastlines=True),
        height=560
    )

    st.plotly_chart(fig_map, use_container_width=True, config=plot_config)

# =========================
# 國家分析
# =========================
elif page == "國家分析":
    st.subheader(f"🏆 獎牌數前 {top_n_country} 名國家排行")

    top_country = country_pivot.head(top_n_country)

    top_long = top_country.melt(
        id_vars=["國家", "Country", "Code"],
        value_vars=["金牌", "銀牌", "銅牌"],
        var_name="獎牌種類",
        value_name="數量"
    )

    fig_bar = px.bar(
        top_long,
        x="國家",
        y="數量",
        color="獎牌種類",
        color_discrete_map=medal_colors,
        title=f"前 {top_n_country} 名國家金、銀、銅牌數比較",
        text="數量"
    )

    fig_bar.update_layout(
        xaxis_title="國家",
        yaxis_title="獎牌數",
        barmode="stack",
        height=560
    )

    st.plotly_chart(fig_bar, use_container_width=True, config=plot_config)

    st.divider()

    st.subheader("🔎 單一國家獎牌查詢")

    country_options = sorted(filtered_df["國家"].unique())

    selected_country = st.selectbox(
        "選擇國家",
        country_options
    )

    country_detail = filtered_df[filtered_df["國家"] == selected_country]

    country_summary = (
        country_detail
        .groupby("獎牌種類")
        .size()
        .reset_index(name="數量")
    )

    col1, col2 = st.columns([1, 2])

    with col1:
        st.write(f"### {selected_country} 獎牌統計")
        st.dataframe(country_summary, use_container_width=True)

    with col2:
        country_sport = (
            country_detail
            .groupby(["運動項目", "性別", "獎牌種類"])
            .size()
            .reset_index(name="數量")
        )

        fig_country = px.bar(
            country_sport,
            x="運動項目",
            y="數量",
            color="獎牌種類",
            pattern_shape="性別",
            color_discrete_map=medal_colors,
            title=f"{selected_country} 各運動項目、性別與獎牌數",
            text="數量"
        )

        fig_country.update_layout(
            xaxis_title="運動項目",
            yaxis_title="獎牌數",
            xaxis_tickangle=-45,
            height=520
        )

        st.plotly_chart(fig_country, use_container_width=True, config=plot_config)

# =========================
# 運動項目分析
# =========================
elif page == "運動項目分析":
    st.subheader(f"⚽ 前 {top_n_country} 名國家的主要運動項目獎牌組成")

    sport_base = filtered_df[filtered_df["國家"].isin(top_country_names)]

    sport_medal = (
        sport_base
        .groupby(["運動項目", "性別", "獎牌種類"])
        .size()
        .reset_index(name="數量")
    )

    top_sports = (
        sport_base
        .groupby("運動項目")
        .size()
        .reset_index(name="總獎牌數")
        .sort_values("總獎牌數", ascending=False)
        .head(10)
    )

    top_sport_names = top_sports["運動項目"].tolist()
    sport_medal = sport_medal[sport_medal["運動項目"].isin(top_sport_names)]

    fig_sport_medal = px.bar(
        sport_medal,
        x="數量",
        y="運動項目",
        color="獎牌種類",
        pattern_shape="性別",
        color_discrete_map=medal_colors,
        orientation="h",
        title=f"前 {top_n_country} 名國家中，主要運動項目的性別與獎牌組成",
        text="數量"
    )

    fig_sport_medal.update_layout(
        xaxis_title="獎牌數",
        yaxis_title="運動項目",
        barmode="stack",
        height=620
    )

    st.plotly_chart(fig_sport_medal, use_container_width=True, config=plot_config)

    st.divider()

    st.subheader(f"🚻 前 {top_n_country} 名國家主要運動項目之性別獎牌分布")

    st.write(
        f"比較前 {top_n_country} 名國家在主要運動項目中，男性、女性與混合項目的獎牌數差異。"
    )

    sport_gender = (
        sport_base[sport_base["運動項目"].isin(top_sport_names)]
        .groupby(["運動項目", "性別"])
        .size()
        .reset_index(name="獎牌數")
    )

    fig_sport_gender = px.bar(
        sport_gender,
        x="運動項目",
        y="獎牌數",
        color="性別",
        barmode="group",
        title=f"前 {top_n_country} 名國家主要運動項目之性別獎牌分布",
        text="獎牌數"
    )

    fig_sport_gender.update_layout(
        xaxis_title="運動項目",
        yaxis_title="獎牌數",
        xaxis_tickangle=-45,
        height=560
    )

    st.plotly_chart(fig_sport_gender, use_container_width=True, config=plot_config)

# =========================
# 時間趨勢分析
# =========================
elif page == "時間趨勢分析":
    st.subheader("📈 各年份金、銀、銅牌數趨勢")

    year_medal = (
        filtered_df
        .groupby(["Year", "獎牌種類"])
        .size()
        .reset_index(name="數量")
    )

    fig_line = px.line(
        year_medal,
        x="Year",
        y="數量",
        color="獎牌種類",
        markers=True,
        color_discrete_map=medal_colors,
        title="不同年份金、銀、銅牌數變化"
    )

    fig_line.update_layout(
        xaxis_title="年份",
        yaxis_title="獎牌數",
        height=560
    )

    for event_year in [1900, 1964, 1980, 1984, 1992, 2000, 2012]:
        if selected_year_range[0] <= event_year <= selected_year_range[1]:
            fig_line.add_vline(
                x=event_year,
                line_dash="dash",
                line_color="gray",
                opacity=0.6
            )

    st.plotly_chart(fig_line, use_container_width=True, config=plot_config)

    st.info("圖中的灰色虛線為重要歷史事件或項目加入年份，可搭配「背後原因解讀」頁面進一步說明。")

    st.divider()

    st.subheader(f"📊 前 {top_n_country} 名國家各年份獎牌變化")

    top_country_year = (
        filtered_df[filtered_df["國家"].isin(top_country_names)]
        .groupby(["Year", "國家"])
        .size()
        .reset_index(name="獎牌數")
    )

    fig_country_year = px.line(
        top_country_year,
        x="Year",
        y="獎牌數",
        color="國家",
        markers=True,
        title=f"前 {top_n_country} 名國家在不同年份的獎牌數變化"
    )

    fig_country_year.update_layout(
        xaxis_title="年份",
        yaxis_title="獎牌數",
        height=560
    )

    for event_year in [1900, 1964, 1980, 1984, 1992, 2000, 2012]:
        if selected_year_range[0] <= event_year <= selected_year_range[1]:
            fig_country_year.add_vline(
                x=event_year,
                line_dash="dash",
                line_color="gray",
                opacity=0.6
            )

    st.plotly_chart(fig_country_year, use_container_width=True, config=plot_config)

# =========================
# 酷炫互動圖
# =========================
elif page == "酷炫互動圖":
    st.subheader(f"🌳 樹狀圖：前 {top_n_country} 名國家－運動項目－性別－獎牌種類")

    tree_data = (
        filtered_df
        .groupby(["國家", "運動項目", "性別", "獎牌種類"])
        .size()
        .reset_index(name="獎牌數")
    )

    tree_data = tree_data[tree_data["國家"].isin(top_country_names)]

    fig_tree = px.treemap(
        tree_data,
        path=["國家", "運動項目", "性別", "獎牌種類"],
        values="獎牌數",
        color="獎牌種類",
        color_discrete_map=medal_colors,
        title=f"前 {top_n_country} 名國家之運動項目、性別與獎牌組成"
    )

    fig_tree.update_layout(height=680)

    st.plotly_chart(fig_tree, use_container_width=True, config=plot_config)

    st.divider()

    st.subheader("☀️ 太陽圖：獎牌種類－性別－運動項目")

    sunburst_data = (
        filtered_df
        .groupby(["獎牌種類", "性別", "運動項目"])
        .size()
        .reset_index(name="獎牌數")
    )

    top_sports_for_sun = (
        sunburst_data
        .groupby("運動項目")["獎牌數"]
        .sum()
        .sort_values(ascending=False)
        .head(12)
        .index
        .tolist()
    )

    sunburst_data = sunburst_data[sunburst_data["運動項目"].isin(top_sports_for_sun)]

    fig_sun = px.sunburst(
        sunburst_data,
        path=["獎牌種類", "性別", "運動項目"],
        values="獎牌數",
        color="獎牌種類",
        color_discrete_map=medal_colors,
        title="獎牌種類、性別與運動項目分層分析"
    )

    fig_sun.update_layout(height=650)

    st.plotly_chart(fig_sun, use_container_width=True, config=plot_config)

    st.divider()

    st.subheader(f"🔄 桑基圖：前 {top_n_country} 名國家 → 運動項目 → 性別 → 獎牌種類")

    sankey_base = filtered_df[filtered_df["國家"].isin(top_country_names)].copy()

    top_sankey_sports = (
        sankey_base
        .groupby("運動項目")
        .size()
        .sort_values(ascending=False)
        .head(8)
        .index
        .tolist()
    )

    sankey_base = sankey_base[sankey_base["運動項目"].isin(top_sankey_sports)]

    country_sport_flow = (
        sankey_base
        .groupby(["國家", "運動項目"])
        .size()
        .reset_index(name="數量")
    )

    sport_gender_flow = (
        sankey_base
        .groupby(["運動項目", "性別"])
        .size()
        .reset_index(name="數量")
    )

    gender_medal_flow = (
        sankey_base
        .groupby(["性別", "獎牌種類"])
        .size()
        .reset_index(name="數量")
    )

    labels = top_country_names + top_sankey_sports + sorted(sankey_base["性別"].unique().tolist()) + ["金牌", "銀牌", "銅牌"]
    labels = list(dict.fromkeys(labels))
    label_index = {label: i for i, label in enumerate(labels)}

    sources = []
    targets = []
    values = []

    for _, row in country_sport_flow.iterrows():
        sources.append(label_index[row["國家"]])
        targets.append(label_index[row["運動項目"]])
        values.append(row["數量"])

    for _, row in sport_gender_flow.iterrows():
        sources.append(label_index[row["運動項目"]])
        targets.append(label_index[row["性別"]])
        values.append(row["數量"])

    for _, row in gender_medal_flow.iterrows():
        sources.append(label_index[row["性別"]])
        targets.append(label_index[row["獎牌種類"]])
        values.append(row["數量"])

    fig_sankey = go.Figure(
        data=[
            go.Sankey(
                node=dict(
                    pad=18,
                    thickness=18,
                    line=dict(color="black", width=0.3),
                    label=labels
                ),
                link=dict(
                    source=sources,
                    target=targets,
                    value=values
                )
            )
        ]
    )

    fig_sankey.update_layout(
        title_text=f"前 {top_n_country} 名國家與主要運動項目的性別與獎牌流向",
        height=650,
        font_size=12
    )

    st.plotly_chart(fig_sankey, use_container_width=True, config=plot_config)

# =========================
# 背後原因解讀
# =========================
elif page == "背後原因解讀":
    st.subheader("🧠 獎牌變化背後的可能原因")

    st.write(
        "這一頁將獎牌數據與奧運歷史事件、項目加入時間、女性參與變化與政治事件連結，"
        "用來輔助解釋圖表中看到的獎牌變化。"
    )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 1️⃣ 項目增加會影響獎牌數")
        st.info(
            "有些年份獎牌數上升，不一定代表所有國家都變強，"
            "也可能是因為奧運新增比賽項目或小項，使獎牌機會增加。"
        )
        st.write(
            "例如柔道在 1964 年東京奧運成為正式項目，女子柔道在 1992 年巴塞隆納奧運成為正式項目。"
            "因此，從這些年份開始，相關國家才有更多機會在柔道項目中累積獎牌。"
        )

    with col2:
        st.markdown("### 2️⃣ 女性參賽機會增加")
        st.info(
            "早期奧運女性參賽項目較少，因此整體資料中男性獎牌數通常明顯多於女性。"
        )
        st.write(
            "女性在 1900 年巴黎奧運開始參與奧運，之後隨著女子項目逐漸增加，"
            "女性獎牌資料也逐漸累積。"
        )

    st.divider()

    col3, col4 = st.columns(2)

    with col3:
        st.markdown("### 3️⃣ 政治事件影響獎牌分布")
        st.warning(
            "1980 年莫斯科奧運與 1984 年洛杉磯奧運都受到政治抵制影響，"
            "部分國家缺席會使該年獎牌分布出現變化。"
        )
        st.write(
            "如果某個國家在特定年份獎牌數突然下降，不能只解釋為實力退步，"
            "也可能與國際政治事件或參賽資格有關。"
        )

    with col4:
        st.markdown("### 4️⃣ 項目本身獎牌機會不同")
        st.info(
            "水上運動、田徑、體操等項目包含較多小項，因此本來就有較多獎牌機會。"
        )
        st.write(
            "所以獎牌數多不一定只代表該國在單一運動特別強，"
            "也可能與該項目可競爭的小項數量較多有關。"
        )

    st.divider()

    st.subheader("📌 重要年份與可能影響")

    event_filtered = event_data[
        (event_data["年份"] >= selected_year_range[0]) &
        (event_data["年份"] <= selected_year_range[1])
    ]

    st.dataframe(event_filtered, use_container_width=True)

    st.divider()

    st.subheader("📈 目前篩選範圍內的年份趨勢與事件標記")

    year_medal_context = (
        filtered_df
        .groupby(["Year", "獎牌種類"])
        .size()
        .reset_index(name="數量")
    )

    fig_context = px.line(
        year_medal_context,
        x="Year",
        y="數量",
        color="獎牌種類",
        markers=True,
        color_discrete_map=medal_colors,
        title="各年份獎牌數變化與重要事件對照"
    )

    fig_context.update_layout(
        xaxis_title="年份",
        yaxis_title="獎牌數",
        height=560
    )

    for _, row in event_filtered.iterrows():
        fig_context.add_vline(
            x=row["年份"],
            line_dash="dash",
            line_color="gray",
            opacity=0.6
        )

    st.plotly_chart(fig_context, use_container_width=True, config=plot_config)

    st.info("灰色虛線代表重要歷史事件或項目加入年份，可用來輔助解釋某些年份的獎牌變化。")

    st.divider()

    st.subheader("📝 可直接放進報告的解讀文字")

    st.markdown(
        """
        本研究的資料主要呈現夏季奧運獎牌結果，但若要理解背後原因，
        需要搭配奧運歷史脈絡進行分析。首先，奧運比賽項目與小項會隨著年代增加，
        因此獎牌數增加不一定只是競技實力提升，也可能是新增項目帶來更多獎牌機會。
        
        其次，早期女性參賽機會較少，直到後期女子項目逐漸增加，
        才使女性獎牌資料量逐漸上升。因此，性別獎牌分布不只是運動表現差異，
        也反映了奧運制度與性別參與機會的歷史變化。
        
        此外，1980 年莫斯科奧運與 1984 年洛杉磯奧運受到政治抵制影響，
        部分國家缺席，可能導致特定年份的獎牌分布出現變化。
        最後，主辦國優勢、國家運動資源與各運動項目的小項數量，
        也都可能影響獎牌數據的呈現。
        
        因此，視覺化圖表呈現的是數據結果，而真正的解讀需要結合歷史事件、
        項目制度與社會背景進行分析。
        """
    )

# =========================
# 資料表
# =========================
elif page == "資料表":
    st.subheader("📋 各國獎牌統計表")

    country_table = country_pivot[[
        "國家", "Code", "金牌", "銀牌", "銅牌", "總獎牌數"
    ]].rename(columns={
        "Code": "國家代碼"
    })

    st.dataframe(country_table, use_container_width=True)

    st.divider()

    st.subheader("📄 原始資料表")

    display_df = filtered_df.copy()

    display_df = display_df.rename(columns={
        "Year": "年份",
        "City": "城市",
        "Discipline": "分項",
        "Athlete": "選手",
        "Event": "比賽項目",
        "Code": "國家代碼"
    })

    display_df = display_df[[
        "年份",
        "城市",
        "運動項目",
        "分項",
        "選手",
        "國家代碼",
        "性別",
        "比賽項目",
        "獎牌種類",
        "國家"
    ]]

    st.dataframe(display_df, use_container_width=True)

    csv = display_df.to_csv(index=False).encode("utf-8-sig")

    st.download_button(
        label="📥 下載篩選後資料 CSV",
        data=csv,
        file_name="夏季奧運獎牌篩選資料.csv",
        mime="text/csv"
    )