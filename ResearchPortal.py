import streamlit as st
import pandas as pd

# -------------------------
# Load dataset
# -------------------------
df = pd.read_csv("Final_Cleaned_File.csv").fillna("")

st.set_page_config(page_title="Autism Research Explorer", layout="wide")
st.title("🧠 Autism Research Explorer")
st.write("Explore, filter, and read autism-related scientific research papers.")

# -------------------------
# Sidebar Filters
# -------------------------
st.sidebar.header("🔎 Filters")

# Category filter
category_options = sorted(df["category"].unique())
category_filter = st.sidebar.selectbox("Filter by Category", ["All"] + category_options)

# Title filter
title_options = sorted(df["title"].unique())
title_filter = st.sidebar.selectbox("Filter by Title", ["All"] + title_options)

# Year filter (NEW)
year_options = sorted(df["year"].dropna().unique())
year_filter = st.sidebar.selectbox("Filter by Year", ["All"] + [str(y) for y in year_options])

# -------------------------
# Apply filters
# -------------------------
filtered = df.copy()

if category_filter != "All":
    filtered = filtered[filtered["category"] == category_filter]

if title_filter != "All":
    filtered = filtered[filtered["title"] == title_filter]

if year_filter != "All":
    filtered = filtered[filtered["year"].astype(str) == year_filter]

# -------------------------
# Display Number of Results
# -------------------------
st.write(f"### 🔍 {len(filtered)} studies found")

# -------------------------
# Select Title from Filtered Results
# -------------------------
if not filtered.empty:

    selected_title = st.selectbox(
        "📌 Choose a Study",
        filtered["title"].tolist()
    )

    selected_row = filtered[filtered["title"] == selected_title].iloc[0]


    # -------------------------
    # Main Research Card
    # -------------------------
    st.markdown("---")
    st.subheader(selected_row["title"])

    # Year + Category Badges
    st.markdown(
        f"""
        <div style='margin-bottom: 10px;'>
            <span style='background:#e0e7ff;padding:6px 10px;border-radius:8px;margin-right:10px; color:#000000;'>
                📅 {selected_row['year']}
            </span>
            <span style='background:#d1fae5;padding:6px 10px;border-radius:8px; color:#000000;'>
                🏷️ {selected_row['category']}
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Authors
    st.write(f"**👥 Authors:** {selected_row['authors']}")

    # Keywords Tag Display
    keyword_list = selected_row["keywords"].split(",") if selected_row["keywords"] else []
    if keyword_list:
        st.write("### 🔖 Keywords")
        st.markdown(
            " ".join(
                [
                    f"<span style='background:#fef3c7;padding:5px 8px;border-radius:6px;margin-right:6px; color:#000000;'>{kw.strip()}</span>"
                    for kw in keyword_list
                ]
            ),
            unsafe_allow_html=True
        )

    # Summary (short abstract_text)
    st.write("### 📝 Summary")
    summary_text = (
        selected_row["abstract_text"][:500] + "..."
        if len(selected_row["abstract_text"]) > 500
        else selected_row["abstract_text"]
    )
    st.write(summary_text)

    # Collapsible full abstract
    with st.expander("📄 Full Abstract / Content"):
        st.write(selected_row["abstract_text"])

    # Links
    st.markdown("---")
    st.write("### 🔗 External Links")

    if selected_row.get("url"):
        st.markdown(f"**[OpenAlex Page]({selected_row['url']})**")

    if selected_row.get("doi"):
        st.markdown(f"**[DOI Link](https://doi.org/{selected_row['doi']})**")

    if selected_row.get("openalex_id"):
        st.markdown(f"**OpenAlex ID:** `{selected_row['openalex_id']}`")

else:
    st.info("No studies match your selected filters.")
