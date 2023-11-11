import folium
import pgeocode

nomi = pgeocode.Nominatim('es')


# Sample data (replace with your actual data)
faculty_data = [
    {
        'Faculty': 'FIB',
        'Postal Code': ['08020','08910','08960','08290','08200','08720','17400','25200','08980','08860'
        ],
        'Latitude': 41.3833,
        'Longitude': 2.1834
    },
    {
        'Faculty': 'FME',
        'Postal Code': ['08020','08001','08900','08720','08750','08770' ,'08780','08790','08820','08830'
        ],
        'Latitude': 41.3833,
        'Longitude': 2.1834
    },
]


# Create maps for each faculty

for faculty in faculty_data:
    m = folium.Map(location=[faculty["Latitude"], faculty["Longitude"]], zoom_start=14)
    for postalcode in faculty['Postal Code']:
        print(postalcode)
        queryinfo = nomi.query_postal_code(postalcode);
        
        
        # Add markers for the top 10 postal codes       
        folium.CircleMarker(
            location=[queryinfo.latitude, queryinfo.longitude],
            radius=5,
            color='red',
            fill=True,
            fill_color='red'
        ).add_to(m)
    map_filename = f"{faculty['Faculty']}_top_10_postal_codes_map.html"
    m.save(map_filename)
    # Save the map as an HTML file
    