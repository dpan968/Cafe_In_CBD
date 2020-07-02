import folium
import pandas

data = pandas.read_csv("Cafe_2018.csv")

lat = list(data["y coordinate"])
lon = list(data["x coordinate"])
size = list(data["Number of seats"])
name = list(data["Trading name"])
address = list(data["Street address"])

def color_producer(size):
    if size < 10:
        return "red"
    elif 10 <= size < 20:
        return "orange"
    else:
        return "green"
    

def construct_map():
    html = """
    Cafe name:<br>
    <a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
    <p>Name: %s<p>
    <p>Seat: %s<p> 
    Address: %s
    """

    map = folium.Map(location=[-37.811128, 144.962832], zoom_start=15, tiles="Stamen Terrain")

    fgp= folium.FeatureGroup(name="CBD")

    fgp.add_child(folium.GeoJson(data = open('Postcodes.geojson', 'r', encoding='utf-8-sig').read(), 
    style_function=lambda x: {'fillColor':'yellow'}))

    fgv= folium.FeatureGroup(name="Cafes")
    for ln, lt, seat, nm, addr in zip(lon, lat, size, name, address):
        iframe = folium.IFrame(html=html % (nm, nm, nm, seat, addr), width=200, height=150)
        fgv.add_child(folium.CircleMarker(location=[lt, ln], popup=folium.Popup(iframe), rasius = 2, fill=True, 
        fill_color=color_producer(seat), color = 'green', fill_opacity=0.7))
    map.add_child(fgp)
    map.add_child(fgv)
    map.add_child(folium.LayerControl())
    map.save("Cafes_in_CDB.html")

if __name__ == "__main__":
    construct_map()

    

