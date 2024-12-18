import streamlit as st
import pandas as pd
from io import BytesIO
from opencage.geocoder import OpenCageGeocode

# Function to Fetch Latitude and Longitude
def get_lat_long(address):
    api_key = 'f84de8bb057943e8a27584749c31f68e'
    geocoder = OpenCageGeocode(api_key)
    try:
        result = geocoder.geocode(address)
        if result:
            return pd.Series([result[0]['geometry']['lat'], result[0]['geometry']['lng']])
        else:
            return pd.Series([None, None])
    except Exception as e:
        print(f"Error: {e}")
        return pd.Series([None, None])

# Detect columns with date-like values dynamically
def detect_date_columns(df):
    return [col for col in df.columns if pd.to_datetime(col, errors='coerce') is not pd.NaT]

# Streamlit App
st.title("Ordering Plan to Route Planner")

# Step 1: Upload Location and Address File
st.header("Step 1: Upload Location and Address File")
uploaded_address_file = st.file_uploader("Choose a file", type=["csv", "xlsx"])

if uploaded_address_file:
    st.subheader("Uploaded Address Data")
    if uploaded_address_file.name.endswith(".csv"):
        address_data = pd.read_csv(uploaded_address_file)
    else:
        address_data = pd.read_excel(uploaded_address_file)
    st.dataframe(address_data)

    # Apply geocoding to get latitude and longitude
   # with st.spinner("Fetching Latitude and Longitude..."):
    #    address_data[["Latitude", "Longitude"]] = address_data["Address"].apply(get_lat_long)
    st.success("Geocoding Complete!")
    st.dataframe(address_data)

    # Download updated address data
    csv_address = address_data.to_csv(index=False)
    st.download_button(
        label="Download Address Data with Coordinates",
        data=csv_address,
        file_name="address_with_coordinates.csv",
        mime="text/csv"
    )

    # Step 2: Upload Ordering Plan
    st.header("Step 2: Upload Ordering Plan File")
    ordering_plan_file = st.file_uploader("Upload Your Ordering Plan File (Excel)", type=["xlsx"])

    if ordering_plan_file:
        with st.spinner("Processing Ordering Plan..."):
            ordering_plan = pd.read_excel(ordering_plan_file, sheet_name="Sheet", header=None)

            # Clean and set headers
            ordering_plan.dropna(how="all", inplace=True)
            ordering_plan.drop([0,2], inplace=True)
            ordering_plan.columns = ordering_plan.iloc[0].fillna("S.No.").astype(str)
            ordering_plan = ordering_plan[1:].reset_index(drop=True)
            # Validate required columns
            if "Location" not in ordering_plan.columns:
                st.error("The file must contain a 'Location' column.")
                st.stop()

            # Detect date-like columns
            date_columns = detect_date_columns(ordering_plan)
            if not date_columns:
                st.error("No date-like columns detected. Ensure your file has date columns.")
                st.stop()

        st.success("Ordering Plan Processed!")

        # Step 3: Melt Data
        with st.spinner("Melting Data..."):
            melted_df = pd.melt(
                ordering_plan,
                id_vars=["Location"],
                value_vars=date_columns,
                var_name="Month",
                value_name="Order Size"
            )
            melted_df["Month"] = pd.Categorical(melted_df["Month"], categories=date_columns, ordered=True)
            melted_df = melted_df.sort_values(["Location", "Month"]).reset_index(drop=True)
        # st.write("Melted Data:")
        # st.dataframe(melted_df)

        # Step 4: Pivot Data
        pivot_df = melted_df.pivot_table(
            index="Location",
            columns="Month",
            values="Order Size",
            aggfunc="sum",
            fill_value=0
        )
        st.write("Pivot Table:")
        st.write(pivot_df.head(20))

        # Reset index to ensure 'Location' is a column
        pivot_df = pivot_df.reset_index()

        # Step 3: Merge DataFrames on 'Location'
        # Check for 'Location' column
        if "Location" not in address_data.columns or "Location" not in pivot_df.columns:
            st.write(address_data.columns)
            st.write(pivot_df.columns)
            st.error("The 'Location' column is missing. Please check your files.")
            st.stop()

        # Reset index to avoid indexing issues
        address_df = address_data.reset_index(drop=True)
        order_df = pivot_df.reset_index(drop=True)
        # Merge DataFrames (left join to retain Address DataFrame locations)
        with st.spinner("Merging Data..."):
            merged_df = pd.merge(
                address_data,
                pivot_df,
                on="Location",
                how="left",   # Include only those in the address data
                validate="one_to_one"  # Ensures no duplicate keys in the merge
            )

        # Display the merged DataFrame
        st.success("Merge Successful! Showing locations present in the address data:")
        st.dataframe(merged_df)


        # Step 5: Download Options
        with BytesIO() as excel_output:
            with pd.ExcelWriter(excel_output, engine="xlsxwriter") as writer:
                pivot_df.to_excel(writer, sheet_name="Pivot Table")
            st.download_button(
                label="Download Pivot Table as Excel",
                data=excel_output.getvalue(),
                file_name="processed_ordering_plan.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

        # Step 6: Add Factory Location and Create Merged Table
        st.subheader("Add Factory Location")

        # Input for Factory Location Details
        factory_address = st.text_area("Enter Factory Address:", placeholder="e.g., Mc Cain Food India Pvt Ltd Mehsana...")
        service_time = st.number_input("Enter Service Time (in minutes):", min_value=0, value=30)
        factory_status = st.selectbox("Select Factory Status:", options=["Green", "Yellow", "Red"], index=0)

        if factory_address:
            # Factory Data
            factory_row = pd.DataFrame({
                "Location": ["Factory"],
                "Service Time": [""],
                "Order Size": [""],
                "Address": [factory_address],
                "Latitude": [""],
                "Longitude": [""],
                "Status": [""]
            })

            # Combine Factory Location with Address Data
            combined_address_data = pd.concat([factory_row, address_data], ignore_index=True)

            # Merge DataFrames
            st.subheader("Merged Table with Orders and Factory Location")
            pivot_df = pivot_df.reset_index()  # Ensure 'Location' is a column
            merged_df = pd.merge(
                combined_address_data,
                pivot_df,
                on="Location",
                how="left"
            )

            # Add Additional Columns
            merged_df["Service Time"] = merged_df["Service Time"].fillna(service_time)
            merged_df["Status"] = merged_df["Status"].fillna(factory_status)

            # Rearrange Columns
            merged_df = merged_df[[
                "Location", 
                "Service Time", 
                pivot_df.columns[2],  # Replace with actual first order size column
                "Address", 
                "Latitude", 
                "Longitude", 
                "Status"
            ]]
            merged_df.rename(columns={"Location":"Title", pivot_df.columns[2]:"Order Size"},inplace=True)

            # Display Merged Table
            st.dataframe(merged_df)

            # Download Option
            with BytesIO() as excel_output:
                with pd.ExcelWriter(excel_output, engine="xlsxwriter") as writer:
                    merged_df.to_excel(writer, sheet_name="Merged Table", index=False)
                st.download_button(
                    label="Download Merged Table as Excel",
                    data=excel_output.getvalue(),
                    file_name="merged_table_with_factory.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
        else:
            st.info("Enter factory details to include in the merged table.")