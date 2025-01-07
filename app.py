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

/* Increase the font size for total score specifically */
.card .total-score {
    font-size: 1.2rem;     /* Adjust this to be bigger or smaller as needed */
    color: #000;          /* Could style color (e.g., #d9534f for red) */
    margin-bottom: 0.5rem;
    display: block;
}

.streamlit-expander {
    margin-top: 0.5rem;
}
</style>
"""

def display_card(row):
    """
    Renders a single 'card' containing basic info and 
    an expander for 1-Pager and Studies.
    """
    st.markdown('<div class="card">', unsafe_allow_html=True)

    # Title / Drug Name
    st.markdown(f"<h4>{row['Drug_Name']}</h4>", unsafe_allow_html=True)

    # Disease
    st.markdown(
        f'<div class="info"><strong>Disease:</strong> {row["Disease"]}</div>',
        unsafe_allow_html=True
    )

    # Orphan, Category, and a bigger "Total Score"
    st.markdown(f"""
    <div class="small-text">
        <strong>Orphan:</strong> {row["Orphan"]}<br>
        <strong>Category:</strong> {row["Category"]}
    </div>
    """, unsafe_allow_html=True)

    # Larger/bolder total score
    st.markdown(
        f'<span class="total-score"><strong>Total Score:</strong> {row["Total Score"]}</span>',
        unsafe_allow_html=True
    )

    # Inline expander for more details
    with st.expander("View More"):
        st.write("### 1-Pager")
        st.markdown(row["1-Pager"] if pd.notnull(row["1-Pager"]) else "No 1-Pager available.")

        st.write("### Studies")
        st.markdown(row["Studies"] if pd.notnull(row["Studies"]) else "No Studies available.")

    st.markdown('</div>', unsafe_allow_html=True)


def display_cards_in_grid(df, columns_per_row=1):
    """
    Displays the DataFrame rows as a grid of cards.
    columns_per_row=1 => a single column layout (one card per row).
    """
    for start_idx in range(0, len(df), columns_per_row):
        cols = st.columns(columns_per_row)
        for col_idx in range(columns_per_row):
            row_idx = start_idx + col_idx
            if row_idx < len(df):
                with cols[col_idx]:
                    display_card(df.iloc[row_idx])


def main():
    # Inject custom CSS
    st.markdown(CARD_STYLE, unsafe_allow_html=True)

    # 1) New Title
    st.title("5052B Potential Drugs")

    # 2) Centered Logo with use_container_width
    st.image(
        "https://vmbpi.com/wp-content/uploads/2024/12/Asset-2@4x-8.png",
        use_container_width=True
    )

    # 3) "How This Was Made" Section
    st.subheader("How This Was Made")
    st.markdown("""
Here’s an explanation of the three routes I used to identify potential drugs for 5052B:

1. **StuffThatWorks Database**:  
   I scraped the StuffThatWorks database, which aggregates patient-reported outcomes for various medications treating chronic diseases. By focusing on off-label drugs with high success rates in treating the target disease, I was able to identify candidates that have shown real-world effectiveness.

2. **Drug-Supplement Combinations**:  
   Using an AI reasoning model (o1), I explored potential drug-supplement combinations. The AI analyzed how specific supplements could synergize with existing drugs, enhancing efficacy or addressing complementary aspects of the disease. This route highlights innovative pairings that may not yet be widely recognized but could provide meaningful therapeutic benefits.

3. **Novel Pathway Exploration**:  
   Again leveraging the AI reasoning model (o1), I researched emerging issues, targets, and pathways that may be linked to the disease. This includes investigating conditions with overlapping mechanisms, such as postural orthostatic tachycardia syndrome (POTS), which I have personal experience with. This route focuses on identifying underexplored or novel pathways that could open doors to groundbreaking treatments.
""")

    # ----- Read CSV -----
    df = pd.read_csv("data.csv")

    # ----- Filters -----
    st.subheader("Filters")
    
    # Orphan filter
    orphan_filter = st.selectbox("Orphan:", ["All", "Yes", "No"], index=0)

    # Category filter
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

    # ----- Display Cards (Single Column) -----
    st.subheader("Filtered Results")
    if filtered_df.empty:
        st.warning("No results found for the selected filters.")
    else:
        display_cards_in_grid(filtered_df, columns_per_row=1)


if __name__ == "__main__":
    main()
