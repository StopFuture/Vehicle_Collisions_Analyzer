from ControlElements.DataImporter import *

source_file = "Datasets/50k_data.xml"
parser_strategy = ["XML Dict Strategy", "Untangle Strategy", "Element Tree Strategy"]

step = -500
final = list()

xml1 = ElementTree.parse(source_file)
with open(source_file) as xmlfile:
    xml2 = xmltodict.parse(xmlfile.read())
xml3 = untangle.parse(source_file)
for cnt in range(40000, 0, step):
    res = list()
    res.append(cnt)
    for parse_strategy in parser_strategy:

        if parse_strategy == "Element Tree Strategy":

            now1 = time.time()  # time object

            rows = []
            cur = 0
            for row in xml1.findall("row"):
                if cur > cnt:
                    break
                cur += step
                if row:
                    try:
                        line = dict()
                        for el in cols:
                            tmp = row.find(el)
                            line[el] = tmp.text
                        rows.append(line)
                    finally:
                        continue

            now2 = time.time()
            now = now2 - now1

            res.append(now * 1000)
        elif parse_strategy == "Untangle Strategy":

            now1 = time.time()
            rows = []
            cur = 0
            for element in xml3.root.row:
                if cur > cnt:
                    break
                cur += step

                if element:
                    try:
                        dct = dict()
                        dct["date-time"] = element.date_time.cdata
                        dct["borough"] = element.borough.cdata
                        dct["zip_code"] = element.zip_code.cdata
                        dct["latitude"] = element.latitude.cdata
                        dct["longitude"] = element.longitude.cdata
                        dct["location"] = element.location.cdata
                        dct["on_street_name"] = element.on_street_name.cdata
                        dct["cross_street_name"] = element.cross_street_name.cdata
                        dct["off_street_name"] = element.off_street_name.cdata
                        dct["injured_persons"] = element.injured_persons.cdata
                        dct["killed_persons"] = element.killed_persons.cdata
                        dct["injured_pedestrians"] = element.injured_pedestrians.cdata
                        dct["killed_pedestrians"] = element.killed_pedestrians.cdata
                        dct["injured_cyclists"] = element.injured_cyclists.cdata
                        dct["killed_cyclists"] = element.killed_cyclists.cdata
                        dct["injured_motorists"] = element.injured_motorists.cdata
                        dct["killed_motorists"] = element.killed_motorists.cdata
                        rows.append(dct)
                    finally:
                        continue

            now2 = time.time()
            now = now2 - now1

            res.append(now* 1000)
        else:
            now1 = time.time()  # time object

            rows = []


            xml_root = xml2["root"]
            cur = 0
            for element in xml_root["row"]:
                if cur > cnt:
                    break
                cur += step
                if element:
                    try:
                        dct = dict()
                        for name in cols:
                            dct[name] = element[name]
                        rows.append(dct)
                    finally:
                        continue

            now2 = time.time()
            now = now2 - now1

            res.append(now* 1000)
    final.append(res)

df = pd.DataFrame(final, columns=["N_rows"] + parser_strategy)
df.to_csv("comparing.csv", encoding='utf-8', index=False)
print(df.head(5))