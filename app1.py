import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit

# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Denda PNBP", page_icon=":bar_chart:", layout="wide")

# ---- READ EXCEL ----
@st.cache
def get_data_from_excel():
    df = pd.read_excel(
        io="Rekap PNBP September 2021.xlsx",
        engine="openpyxl",
        sheet_name="Rekapitulasi Denda PNBP",
        #skiprows=3,
        usecols="A:C",
        nrows=28,
    )
    df.dropna(inplace=True)
    # Add 'hour' column to dataframe
    # df["hour"] = pd.to_datetime(df["Time"], format="%H:%M:%S").dt.hour
    return df

df = get_data_from_excel()

# ---- SIDEBAR ----
st.sidebar.header("Silahkan Pilih:")
bulan = st.sidebar.multiselect(
    "Bulan:",
    options=df["Bulan"].unique(),
    default=df["Bulan"].unique()
)

#OAA = st.sidebar.multiselect(
    #"OAA:",
    #options=df["KAPA_atau_OAA"].unique(),
    #default=df["KAPA_atau_OAA"].unique(),
#)

#OAI = st.sidebar.multiselect(
    #"OAI:",
    #options=df["OAI"].unique(),
    #default=df["OAI"].unique()
#)

df_selection = df.query(
    "Bulan == @bulan"
)

# ---- MAINPAGE ----
st.title(":bar_chart: Jenis Denda PNBP Satker PPPK")
st.markdown("##")

# TOP KPI's
total_denda = int(df_selection["Jumlah"].sum())
#average_rating = round(df_selection["Rating"].mean(), 1)
#star_rating = ":star:" * int(round(average_rating, 0))
rata_denda = int(df_selection["Jumlah"].mean())

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Total Denda:")
    st.subheader(f"Rp {total_denda:,}")
#with middle_column:
    #st.subheader("Average Rating:")
    #st.subheader(f"{average_rating} {star_rating}")
with right_column:
    st.subheader("Rata-rata Denda:")
    st.subheader(f"Rp {rata_denda:,}")

st.markdown("""---""")

# SALES BY PRODUCT LINE [BAR CHART]
sales_by_product_line = (
    df_selection.groupby(by=["Jenis_PNBP"]).sum()[["Jumlah"]].sort_values(by="Jumlah")
)
fig_product_sales = px.bar(
    sales_by_product_line,
    x=sales_by_product_line.index,
    y="Jumlah",
    #orientation="h",
    title="<b></b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_product_line),
    template="plotly_white",
    #width = 1200,
    #height = 600,
)
fig_product_sales.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

st.plotly_chart(fig_product_sales)

# SALES BY HOUR [BAR CHART]
#sales_by_hour = df_selection.groupby(by=["Big_4"]).sum()[["Fee_Jasa"]]
#fig_hourly_sales = px.bar(
    #sales_by_hour,
    #x=sales_by_hour.index,
    #y="Fee_Jasa",
    #title="<b>Big 4</b>",
    #color_discrete_sequence=["#0083B8"] * len(sales_by_hour),
    #template="plotly_white",
#)
#fig_hourly_sales.update_layout(
    #xaxis=dict(tickmode="linear"),
    #plot_bgcolor="rgba(0,0,0,0)",
    #yaxis=(dict(showgrid=False)),
#)


#left_column, right_column = st.columns(2)
#left_column.plotly_chart(fig_hourly_sales, use_container_width=True)
#right_column.plotly_chart(fig_product_sales, use_container_width=True)


# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)