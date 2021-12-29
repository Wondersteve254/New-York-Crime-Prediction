import streamlit as st
import folium
from streamlit_folium import folium_static
from datetime import datetime
import clipboard
from branca.element import Template, MacroElement



class ClickForLatLng(MacroElement):
    _template = Template(u"""
                {% macro script(this, kwargs) %}
                    var marker = new Array();
                    function getLatLng(e){  
                        if (marker.length >0) {
                            for(i=0;i<marker.length;i++){
                                {{this._parent.get_name()}}.removeLayer(marker[i])
                            }
                        }
                        var new_mark = L.marker().setLatLng(e.latlng).addTo({{this._parent.get_name()}});
                        marker.push(new_mark);
                        new_mark.dragging.enable();
                        new_mark.on('dblclick', function(e){ {{this._parent.get_name()}}.removeLayer(e.target)})
                        var lat = e.latlng.lat.toFixed(6),
                        lng = e.latlng.lng.toFixed(6);
                        var txt = {{this.format_str}};
                        navigator.clipboard.writeText(txt);
                        new_mark.bindPopup({{ this.popup }});
                        };
                    {{this._parent.get_name()}}.on('click', getLatLng);
                    
                {% endmacro %}
                """)

    def __init__(self,popup=None):
        super(ClickForLatLng, self).__init__()
        self._name = 'ClickForLatLng'
        self.format_str = 'lat + "," + lng'
        self.alert = True
        self.lat_long = clipboard.paste().split(',')
        if popup:
            self.popup = ''.join(['"', popup, '"'])
        else:
            self.popup = '"Latitude: " + lat + "<br>Longitude: " + lng '


def generateBaseMap(default_location=[40.704467, -73.892246], default_zoom_start=11,min_zoom=11,max_zoom=15,):
    base_map = folium.Map(location=default_location, control_scale=True, zoom_start=default_zoom_start, min_zoom=min_zoom, max_zoom=max_zoom)
    return base_map


def init():
    with st.sidebar:
        st.header("Enter your information", )
        gender = st.radio("Gender:", ["Male","Female"])
        race = st.selectbox("Race:",['WHITE', 'WHITE HISPANIC', 'BLACK', 'ASIAN / PACIFIC ISLANDER', 'BLACK HISPANIC', 'AMERICAN INDIAN/ALASKAN NATIVE', 'OTHER'])
        age = st.slider("Age:",0,120)
        _,col,_ = st.sidebar.columns(3)
        with  col:
            predict = st.button("predict")

    return gender, race, age, predict


st.title("New York Crime Prediction")
gender, race, age, predict= init()
base_map = generateBaseMap()
click = ClickForLatLng()
base_map.add_child(click)
lat_long = click.lat_long
if len(lat_long) == 2:
    lat = lat_long[0]
    long = lat_long[1]
else :
    lat = ""
    long = ""
# try :
#     folium.Marker([float(lat),float(long)],).add_to(base_map)
# except:
#     print("no marker")

folium_static(base_map,width=900)

if predict:
    time = datetime.now()
    month = time.month
    day = time.day
    hour = time.hour
    print(gender,race,age,month,day,hour,lat,long)
