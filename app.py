import streamlit as st
import pandas as pd

# ----- CSS for card-like UI -----
CARD_STYLE = """
<style>
.card {
    background-color: #f9f9f9;
    border-radius: 8px;
    padding: 1rem;
    margin-bottom: 1rem;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.card h4 {
    margin-top: 0;
    margin-bottom: 0.5rem;
}

.card .info {
    color: #666;
    font-size: 0.9rem;
    margin-bottom: 0.5rem;
}

.card .small-text {
    font-size: 0.85rem;
    color: #333;
    margin-bottom: 1rem;
}

/* Optional: ensure expanders look good inside the card */
.streamlit-expander {
    margin-top: 0.5rem;
}
</style>
"""

def display_card(row):
    """
    Renders a single 'card' containing basic info and an expander for details.
    """
    st.markdown('<div class="card">', unsafe_allow_html=True)

    # Title / Drug Name
    st.markdown(f"<h4>{row['Drug_Name']}</h4>", unsafe_allow_html=True)

    # Disease
    st.markdown(
        f'<div class="info"><strong>Disease:</strong> {row["Disease"]}</div>',
        unsafe_allow_html=True
    )

    # Show Orphan, Category, and Total Score
    # Using <br> to place each item on a separate line
    st.markdown(f"""
    <div class="small-text">
        <strong>Orphan:</strong> {row["Orphan"]}<br>
        <strong>Category:</strong> {row["Category"]}<br>
        <strong>Total Score:</strong> {row["Total Score"]}
    </div>
    """, unsafe_allow_html=True)

    # Inline expander for more details (1-Pager & Studies)
    with st.expander("View More"):
        st.write("### 1-Pager")
        st.markdown(row["1-Pager"] if pd.notnull(row["1-Pager"]) else "No 1-Pager available.")

        st.write("### Studies")
        st.markdown(row["Studies"] if pd.notnull(row["Studies"]) else "No Studies available.")

    st.markdown('</div>', unsafe_allow_html=True)


def display_cards_in_grid(df, columns_per_row=2):
    """
    Displays the DataFrame rows as a grid of cards.
    :param df: Filtered Pandas DataFrame
    :param columns_per_row: How many cards wide each row is
    """
    for start_idx in range(0, len(df), columns_per_row):
        # Create a set of columns for this 'row' of cards
        cols = st.columns(columns_per_row)

        # For each card in this row
        for col_idx in range(columns_per_row):
            row_idx = start_idx + col_idx
            if row_idx < len(df):
                with cols[col_idx]:
                    display_card(df.iloc[row_idx])


def main():
    # Inject our custom CSS for the card style
    st.markdown(CARD_STYLE, unsafe_allow_html=True)

    st.title("Drug Data Visualization with Cards (and Total Score)")

    # ----- 1. Read the CSV -----
    df = pd.read_csv("data.csv")

    # ----- 2. Filters -----
    st.subheader("Filters")
    
    # Orphan filter
    orphan_filter = st.selectbox("Orphan:", ["All", "Yes", "No"], index=0)

    # Category filter - derive options from data or set them manually
    if "Category" in df.columns and not df["Category"].dropna().empty:
        category_options = sorted(df["Category"].dropna().unique().tolist())
    else:
        category_options = ["Novel Pathway", "StuffThatWorks", "Drug-Supplement Combo"]

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
        # Show the cards in a grid of 2 columns per row. Adjust as needed.
        display_cards_in_grid(filtered_df, columns_per_row=2)


if __name__ == "__main__":
    main()
