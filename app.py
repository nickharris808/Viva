import streamlit as st
import pandas as pd

def main():
    st.title("Drug Data Visualization")

    # 1. Read the CSV from local file (in the same repo/directory)
    df = pd.read_csv("data.csv")

    # Make sure session state is initialized
    if "selected_row_index" not in st.session_state:
        st.session_state["selected_row_index"] = None

    # 2. Set up Filters
    st.subheader("Filters")

    # Orphan filter
    orphan_filter = st.selectbox("Orphan:", ["All", "Yes", "No"], index=0)

    # Category filter (adjust categories as needed)
    category_options = ["Novel Pathway", "StuffThatWorks", "Drug-Supplement Combo"]
    category_filter = st.multiselect(
        "Category:",
        category_options,
        default=category_options  # By default, include all
    )

    # Apply filters to the DataFrame
    filtered_df = df.copy()

    # Filter by Orphan
    if orphan_filter != "All":
        filtered_df = filtered_df[filtered_df["Orphan"] == orphan_filter]

    # Filter by Category
    if category_filter:
        filtered_df = filtered_df[filtered_df["Category"].isin(category_filter)]

    # 3. Detail view or table view?
    if st.session_state["selected_row_index"] is not None:
        # We are in the detail view
        row_idx = st.session_state["selected_row_index"]

        # row_idx is the position in the *filtered* dataframe
        row_data = filtered_df.iloc[row_idx]

        st.subheader(f"Details for: {row_data['Drug_Name']}")
        st.write(f"**Disease:** {row_data['Disease']}")

        # 4. Display multiple tabs (1-Pager, Studies)
        tab1, tab2 = st.tabs(["1-Pager", "Studies"])

        with tab1:
            st.markdown(row_data["1-Pager"])

        with tab2:
            st.markdown(row_data["Studies"])

        # 5. Back button
        if st.button("Back to Table"):
            st.session_state["selected_row_index"] = None
            st.experimental_rerun()

    else:
        # We are in the table view
        st.subheader("Filtered Results")

        # Columns to display in the table
        columns_to_show = [
            "Disease",
            "Drug_Name",
            "StuffThatWorks_Rank",
            "StuffThatWorks_#_of_reports",
            "Category",
            "Orphan",
            "Total Score"
        ]

        st.dataframe(filtered_df[columns_to_show])

        # For each row, add a button that navigates to the detail view
        for i, row in filtered_df.iterrows():
            drug_name = row["Drug_Name"]
            if st.button(f"View more about {drug_name}", key=f"view_{i}"):
                # Record the row index relative to the filtered dataframe
                row_position_in_filtered = filtered_df.index.get_loc(i)
                st.session_state["selected_row_index"] = row_position_in_filtered
                st.experimental_rerun()

if __name__ == "__main__":
    main()
