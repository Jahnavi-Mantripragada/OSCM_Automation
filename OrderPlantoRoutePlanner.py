import streamlit as st
import pandas as pd
from io import BytesIO
# from opencage.geocoder import OpenCageGeocode

# # Function to Fetch Latitude and Longitude
# def get_lat_long(address):
#     api_key = 'f84de8bb057943e8a27584749c31f68e'
#     geocoder = OpenCageGeocode(api_key)
#     try:
#         result = geocoder.geocode(address)
#         if result:
#             return pd.Series([result[0]['geometry']['lat'], result[0]['geometry']['lng']])
#         else:
#             return pd.Series([None, None])
#     except Exception as e:
#         print(f"Error: {e}")
#         return pd.Series([None, None])

# Detect columns with date-like values dynamically
def detect_date_columns(df):
    return [col for col in df.columns if pd.to_datetime(col, errors='coerce') is not pd.NaT]

# Streamlit App
st.title("Ordering Plan to Route Planner")

# Step 1: Upload Location and Address File
st.header("Step 1: Upload Location and Address File")
st.text("You can use this template: ")
# Create a sample template dynamically
template_data = {
    "Location": ["Mumbai", "Delhi", "Bengaluru"],
    "Address":["Unilever House, B. D. Sawant Marg, Chakala, Mumbai, Maharashtra 400099", 
                "8th Floor Mohante Building, Tolstoy Marg, New Delhi, Delhi 110001",
                "64 Main Road, Whitefield, Bengaluru, Karnataka 560066"]
}
template_df = pd.DataFrame(template_data)

# Save DataFrame to Excel in Memory
output = BytesIO()
with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
    template_df.to_excel(writer, index=False, sheet_name="Template")

# Provide Download Button
st.download_button(
    label="Download Template File",
    data=output.getvalue(),
    file_name="template_file.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

uploaded_address_file = st.file_uploader("Choose a file", type=["csv", "xlsx"])

if uploaded_address_file:
    st.subheader("Uploaded Address Data")
    if uploaded_address_file.name.endswith(".csv"):
        address_data = pd.read_csv(uploaded_address_file)
    else:
        address_data = pd.read_excel(uploaded_address_file)
    st.dataframe(address_data)

    # # Apply geocoding to get latitude and longitude
    # with st.spinner("Fetching Latitude and Longitude..."):
    #     address_data[["Latitude", "Longitude"]] = address_data["Address"].apply(get_lat_long)
    # st.success("Geocoding Complete!")
    # st.dataframe(address_data)

    # # Download updated address data
    # csv_address = address_data.to_csv(index=False)
    # st.download_button(
    #     label="Download Address Data with Coordinates",
    #     data=csv_address,
    #     file_name="address_with_coordinates.csv",
    #     mime="text/csv"
    # )

    city_coordinates = [
    {"City": "Ahmedabad", "Latitude": 23.0225, "Longitude": 72.5714},
    {"City": "Bangalore", "Latitude": 12.9716, "Longitude": 77.5946},
    {"City": "Chandigarh", "Latitude": 30.7333, "Longitude": 76.7794},
    {"City": "Chennai", "Latitude": 13.0827, "Longitude": 80.2707},
    {"City": "Coimbatore", "Latitude": 11.0168, "Longitude": 76.9558},
    {"City": "Delhi", "Latitude": 28.7041, "Longitude": 77.1025},
    {"City": "Hyderabad", "Latitude": 17.3850, "Longitude": 78.4867},
    {"City": "Indore", "Latitude": 22.7196, "Longitude": 75.8577},
    {"City": "Jaipur", "Latitude": 26.9124, "Longitude": 75.7873},
    {"City": "Kolkata", "Latitude": 22.5726, "Longitude": 88.3639},
    {"City": "Lucknow", "Latitude": 26.8467, "Longitude": 80.9462},
    {"City": "Mumbai", "Latitude": 19.0760, "Longitude": 72.8777},
    {"City": "Nagpur", "Latitude": 21.1458, "Longitude": 79.0882},
    {"City": "Patna", "Latitude": 25.5941, "Longitude": 85.1376},
    {"City": "Pune", "Latitude": 18.5204, "Longitude": 73.8567},
    {"City": "Surat", "Latitude": 21.1702, "Longitude": 72.8311},
    {"City": "Varanasi", "Latitude": 25.3176, "Longitude": 82.9739},
    {"City": "Bhopal", "Latitude": 23.2599, "Longitude": 77.4126},
    {"City": "Kanpur", "Latitude": 26.4499, "Longitude": 80.3319},
    {"City": "Thiruvananthapuram", "Latitude": 8.5241, "Longitude": 76.9366},
    {"City": "Vadodara", "Latitude": 22.3072, "Longitude": 73.1812},
    {"City": "Mysore", "Latitude": 12.2958, "Longitude": 76.6394},
    {"City": "Ranchi", "Latitude": 23.3441, "Longitude": 85.3096},
    {"City": "Guwahati", "Latitude": 26.1445, "Longitude": 91.7362},
    {"City": "Kochi", "Latitude": 9.9312, "Longitude": 76.2673},
    {"City": "Vijayawada", "Latitude": 16.5062, "Longitude": 80.6480},
    {"City": "Agra", "Latitude": 27.1767, "Longitude": 78.0081},
    {"City": "Gwalior", "Latitude": 26.2183, "Longitude": 78.1828},
    {"City": "Jodhpur", "Latitude": 26.2389, "Longitude": 73.0243},
    {"City": "Shimla", "Latitude": 31.1048, "Longitude": 77.1734},
    {"City": "Amritsar", "Latitude": 31.6340, "Longitude": 74.8723},
    {"City": "Dehradun", "Latitude": 30.3165, "Longitude": 78.0322},
    {"City": "Allahabad", "Latitude": 25.4358, "Longitude": 81.8463},
    {"City": "Noida", "Latitude": 28.5355, "Longitude": 77.3910},
    {"City": "Faridabad", "Latitude": 28.4089, "Longitude": 77.3178},
    {"City": "Ghaziabad", "Latitude": 28.6692, "Longitude": 77.4538},
    {"City": "Jabalpur", "Latitude": 23.1815, "Longitude": 79.9864},
    {"City": "Raipur", "Latitude": 21.2514, "Longitude": 81.6296},
    {"City": "Panaji", "Latitude": 15.4909, "Longitude": 73.8278},
    {"City": "Madurai", "Latitude": 9.9252, "Longitude": 78.1198},
    {"City": "Nashik", "Latitude": 19.9975, "Longitude": 73.7898},
    {"City": "Thrissur", "Latitude": 10.5276, "Longitude": 76.2144},
    {"City": "Guntur", "Latitude": 16.3067, "Longitude": 80.4365},
    {"City": "Warangal", "Latitude": 17.9784, "Longitude": 79.5941},
    {"City": "Tirupati", "Latitude": 13.6288, "Longitude": 79.4192},
    {"City": "Aurangabad", "Latitude": 19.8762, "Longitude": 75.3433},
    {"City": "Shillong", "Latitude": 25.5788, "Longitude": 91.8933},
    {"City": "Udaipur", "Latitude": 24.5854, "Longitude": 73.7125},
    {"City": "Ajmer", "Latitude": 26.4499, "Longitude": 74.6399},
    {"City": "Pondicherry", "Latitude": 11.9416, "Longitude": 79.8083}
    # Continue to 100 locations if required
]

    # Convert to a DataFrame if needed
    city_df = pd.DataFrame(city_coordinates)

        # Merge city_coordinates into address_data based on Location
    address_data = pd.merge(
        address_data,
        city_coordinates,
        left_on="Location",  # Column in address_data
        right_on="City",     # Column in city_coordinates
        how="left"           # Keep all rows from address_data
    )

    # Drop redundant 'City' column if not needed
    address_data.drop(columns=["City"], inplace=True)


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
