import streamlit as st
import pandas as pd

# ----- CSS for card-like UI -----
CARD_STYLE = """
<style>
/* Basic "card" styling */
.card {
    background-color: #f9f9f9;
    border-radius: 8px;
    padding: 1rem;
    margin-bottom: 1rem;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

/* Title styling */
.card h4 {
    margin-top: 0;
    margin-bottom: 0.5rem;
}

/* Subtext or extra info styling */
.card .info {
    color: #666;
    font-size: 0.9rem;
    margin-bottom: 0.5rem;
}

/* Make text a bit smaller in some places, optional */
.card .small-text {
    font-size: 0.85rem;
    color: #333;
}
</style>
"""

def display_card(row):
    """
    Renders a single 'card' containing basic info and an expander for details.
    """
    st.markdown('<div class="card">', unsafe_allow_html=True)

    # Title
    st.markdown(f"<h4>{row['Drug_Name']}</h4>", unsafe_allow_html=True)
    # Info
    st.markdown(f'<div class="info"><strong>Disease:</strong> {row["Disease"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="small-text"><strong>Orphan:</strong> {row["Orphan"]} | '
                f'<strong>Category:</strong> {row["Category"]}</div>', 
                unsafe_allow_html=True)

    # Inline expander for more details
    with st.expander("View More"):
        # You can add more fields here if you’d like
        st.write("### 1-Pager")
        st.markdown(row["1-Pager"] if pd.notnull(row["1-Pager"]) else "No 1-Pager available")

        st.write("### Studies")
        st.markdown(row["Studies"] if pd.notnull(row["Studies"]) else "No Studies available")

    # Close the card div
    st.markdown('</div>', unsafe_allow_html=True)


def display_cards_in_grid(df, columns_per_row=3):
    """
    Displays the DataFrame rows as a grid of cards.
    :param df: Filtered Pandas DataFrame
    :param columns_per_row: How many cards wide each row is
    """
    for start_idx in range(0, len(df), columns_per_row):
        cols = st.columns(columns_per_row)
        for col_idx in range(columns_per_row):
            row_idx = start_idx + col_idx
            if row_idx < len(df):
                with cols[col_idx]:
                    display_card(df.iloc[row_idx])


def main():
    # Inject our custom CSS for cards
    st.markdown(CARD_STYLE, unsafe_allow_html=True)

    st.title("Drug Data Visualization with Cards")

    # ----- 1. Read CSV -----
    df = pd.read_csv("data.csv")

    # ----- 2. Filters -----
    st.subheader("Filters")
    
    # Orphan filter
    orphan_filter = st.selectbox("Orphan:", ["All", "Yes", "No"], index=0)

    # Category filter
    category_options = sorted(df["Category"].dropna().unique().tolist())
    # If you want to limit it to a known set: 
    # category_options = ["Novel Pathway", "StuffThatWorks", "Drug-Supplement Combo"]
    category_filter = st.multiselect("Category:", category_options, default=category_options)

    # Apply filters
    filtered_df = df.copy()

    if orphan_filter != "All":
        filtered_df = filtered_df[filtered_df["Orphan"] == orphan_filter]

    if category_filter:
        filtered_df = filtered_df[filtered_df["Category"].isin(category_filter)]

    # ----- 3. Display Cards -----
    st.subheader("Filtered Results")
    if filtered_df.empty:
        st.warning("No results found for the selected filters.")
    else:
        # Adjust columns_per_row as needed. 
        # 2 or 3 is typical on wider screens, 
        # but you can also auto-detect screen width or let it be user-configurable.
        display_cards_in_grid(filtered_df, columns_per_row=2)


if __name__ == "__main__":
    main()
