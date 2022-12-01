from VisualElements.Visual_Initialize import *


@st.experimental_memo
def load_data(imported_data):
    def lowercase(el): return str(el).lower()

    imported_data.rename(lowercase, axis='columns', inplace=True)

    imported_data.dropna(subset=["latitude", "longitude", "injured_persons", "date-time", "on_street_name"],
                         inplace=True)
    imported_data['date-time'] = pd.to_datetime(imported_data['date-time'], format='%Y-%m-%d %H:%M:%S')
    for name in ["injured_persons", "killed_persons", "injured_pedestrians",
                 "killed_pedestrians", "injured_cyclists", "killed_cyclists", "injured_motorists",
                 "killed_motorists"]:
        imported_data[name] = imported_data[name].astype('int')
    for name in ["vehicle_type_1", "vehicle_type_2", "vehicle_type_3",
                 "vehicle_type_4", "vehicle_type_5", "contributing_factor_vehicle_1"]:
        imported_data[name] = imported_data[name].str.lower().str.capitalize()

    imported_data['latitude'] = imported_data['latitude'].astype('float')
    imported_data['longitude'] = imported_data['longitude'].astype('float')

    return imported_data



