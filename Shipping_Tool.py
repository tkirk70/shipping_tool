import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Home",
    page_icon=":house:",
)

# st.balloons()

# take input for the zip code
col6, col4, col5 = st.columns(3)
with col4:
    zip_code = st.text_input("What is the zip?", "43123")
    
with col5:
    weight = st.number_input("What is the weight?", 1)
    
with col6:
    option = st.selectbox(
        "Ship From Location",
        ('Kentucky', 'Ohio')
    )
    
if option == 'Kentucky':
    file = 'Zone chart for Kentucky locations.xlsx'
else:
    file = 'TCG zone chart.xlsx'  

# st.write(file)

    
ground_zones = pd.read_excel(file, sheet_name='ground_zones', dtype=str)
# ground_zones_ky = pd.read_excel('Zone chart for Kentucky locations.xlsx', sheet_name='ground_zones', dtype=str)

ground_commercial = pd.read_csv("2023_UPS Ground Commercial.csv")
ground_residential = pd.read_csv("2023_UPS Ground Residential.csv")
ground_surepost = pd.read_csv("2023_UPS SurePost - 1lb or greater.csv")

ground_commercial.set_index('lbs', inplace=True)
ground_residential.set_index('lbs', inplace=True)
ground_surepost.set_index('lbs', inplace=True)

# create title, header and subheader
st.title('TCG Shipping Tool')
# st.divider('✨')
st.divider()
st.header('Check UPS Shipping Costs')
# st.subheader('A TDS Application')

 
# zip_code = input(str('What is the zip?'))
# weight = int(input('What is the weight?'))
zip_code_clipped = zip_code[:3]
# Use boolean indexing to extract the names of customers who ordered product A
result = dict(zip(ground_zones['Dest. ZIP'], ground_zones['Ground']))

# st.write(result)
# result[zip_code_clipped]

c_price = ground_commercial.loc[weight, result[zip_code_clipped][-1]]
r_price = ground_residential.loc[weight, result[zip_code_clipped][-1]]
sure_price = ground_surepost.loc[weight, result[zip_code_clipped][-1]]

from uszipcode import SearchEngine

sr = SearchEngine()
z = sr.by_zipcode(zip_code)


# calculate the distance
import haversine as hs   
from haversine import Unit

loc1=(39.8815, -83.0930)
loc3=(37.7719, -87.1112)
loc2=(z.bounds_north, z.bounds_east)

if option == 'Ohio':
    distance=hs.haversine(loc1,loc2,unit=Unit.MILES)
    print(f'The distance from TCG is: {distance:,.0f} miles.')
else:
    distance=hs.haversine(loc3,loc2,unit=Unit.MILES)
    print(f'The distance from TCG KY Warehouse is: {distance:,.0f} miles.')
    


# st.write(z.major_city + ', ' + z.state + '  ' + z.zipcode + ' is in UPS Ground Zone ' + result[zip_code_clipped] + ' for TCG Continuum.')
# st.write(f'The distance from TCG is: {distance:,.0f} miles.')

st.write(f'{z.major_city},  {z.state}   {z.zipcode} is in UPS Ground Zone {result[zip_code_clipped]} for TCG Continuum {option}  {distance:,.0f} miles away.')
        
col1, col2, col3 = st.columns(3)

with col1:
    length = st.number_input("Length", 1)
    
with col2:
    width = st.number_input("Width", 1)
    
with col3:
    height = st.number_input("Height", 1)
    
dim_weight = length * width * height / 139
# usps_dim_weight = length * width * height / 166 not used for under 1 cubic foot.

if dim_weight > weight:
    st.write(f'The dimensional weight of your package is: {int(round(dim_weight, 0))}lbs.')
    st.write('**USE DIMENSIONAL WEIGHT**')
else:
    st.write(f'The dimensional weight of your package is: {int(round(dim_weight, 0))}lbs.')



# from uszipcode import SearchEngine

# sr = SearchEngine()
# z = sr.by_zipcode(zip_code)
# print(z.major_city + ', ' + z.state + '  ' + z.zipcode + ' is in UPS Ground Zone ' + result[zip_code_clipped] + ' for TCG Continuum.')
# print(f'A package with a weight of {weight}lbs using {ground_residential.columns[0]} will cost: ${r_price:.2f}.')
# print(f'A package with a weight of {weight}lbs using {ground_commercial.columns[0]} will cost: ${c_price:.2f}.')
# print(f'A package with a weight of {weight}lbs using {ground_surepost.columns[0]} will cost: ${sure_price:.2f}.')


# figure out how many different ship services to present.



# try adding buttons to sidebar
with st.sidebar:
    st.button("Cost", type="primary")
    if st.button('Upcharge', type="primary"):
        st.write("**:orange[20% Surcharge for Customer]**")
        multiplier = 1.2
    else:
        st.write("**:orange[TCG Cost]**")
        multiplier = 1


# # add multiplier button for TCG or Customer cost
# st.button("Cost", type="primary")
# if st.button('Upcharge', type="primary"):
#     st.write("**:orange[20% Surcharge for Customer]**")
#     multiplier = 1.2
# else:
#     st.write("**:orange[TCG Cost]**")
#     multiplier = 1

# from copilot
# Display results
# st.write(z.major_city + ', ' + z.state + '  ' + z.zipcode + ' is in UPS Ground Zone ' + result[zip_code_clipped] + ' for TCG Continuum.')
# st.write(f'The distance from TCG is: {distance:,.0f} miles.')
# st.write(f"     A package with a weight of {weight} lbs using {ground_residential.columns[0]} will cost: ${multiplier*r_price:.2f}.")
# st.write(f"     A package with a weight of {weight} lbs using {ground_commercial.columns[0]} will cost: ${multiplier*c_price:.2f}.")
# st.write(f"     A package with a weight of {weight} lbs using {ground_surepost.columns[0]} will cost: ${multiplier*sure_price:.2f}.")

# try to center 3 lines
# Custom CSS style for center alignment
custom_style = '<div style="text-align: left; padding-left: 29px;">'

# Add each line of text with proper formatting
custom_style += f"A package with a weight of {weight} lbs using {ground_residential.columns[0]} will cost: ${multiplier*r_price:.2f}.<br>"
custom_style += f"A package with a weight of {weight} lbs using {ground_commercial.columns[0]} will cost: ${multiplier*c_price:.2f}.<br>"
custom_style += f"A package with a weight of {weight} lbs using {ground_surepost.columns[0]} will cost: ${multiplier*sure_price:.2f}."

# Close the div tag
custom_style += "</div>"

# Render the styled text using st.markdown
st.markdown(custom_style, unsafe_allow_html=True)


st.divider()

## Create a sample DataFrame with latitude and longitude values
data = pd.DataFrame({
    'latitude': [39.8815, z.bounds_north],
    'longitude': [-83.0930, z.bounds_east]
})
 
data_ky = pd.DataFrame({
    'latitude': [37.7719, z.bounds_north],
    'longitude': [-87.1112, z.bounds_east]
})
## Create a map with the data
if option == 'Kentucky':
    data = data_ky
else:
    data = data
st.map(data, zoom=3)

# st.subheader('A TDS Application')
# st.markdown('<div style="text-align: right;">A TDS Application</div>', unsafe_allow_html=True)

# Custom CSS style for the text
custom_style = '<div style="text-align: right; font-size: 20px;">✨ A TDS Application ✨</div>'

# Render the styled text using st.markdown
st.markdown(custom_style, unsafe_allow_html=True)

# over twenty lbs, post office becomes less competative.
