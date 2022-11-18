from __future__ import annotations
from abc import ABC, abstractmethod
import pandas as pd


cols = ["date-time", "borough", "zip_code", "latitude", "longitude", "location", "on_street_name",
        "cross_street_name", "off_street_name", "injured_persons", "killed_persons", "injured_pedestrians",
        "killed_pedestrians", "injured_cyclists", "killed_cyclists", "injured_motorists",
        "killed_motorists"]


class DefParserXML:
    def __init__(self, strategy: Strategy) -> None:
        self._strategy = strategy

    @property
    def strategy(self) -> Strategy:
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: Strategy) -> None:
        self._strategy = strategy

    def extract_data(self, xml_source_file) -> None:
        return self._strategy.parse_xml(xml_source_file)


class Strategy(ABC):
    @abstractmethod
    def parse_xml(self, xml_source_file):
        pass


# xmltodict
class XMLDictStrategy(Strategy):
    def parse_xml(self, xml_source_file) -> pd.DataFrame:
        import xmltodict
        rows = []
        with open(xml_source_file) as xmlfile:
            xml = xmltodict.parse(xmlfile.read())

        xml_root = xml["root"]
        for element in xml_root["row"]:
            if element:
                try:
                    dct = dict()
                    for name in cols:
                        dct[name] = element[name]
                    rows.append(dct)
                finally:
                    continue

        df = pd.DataFrame(rows, columns=cols)

        return df


class UntangleStrategy(Strategy):
    def parse_xml(self, xml_source_file) -> pd.DataFrame:
        import untangle

        xml = untangle.parse(xml_source_file)
        rows = []
        for element in xml.root.row:
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

        df = pd.DataFrame(rows, columns=cols)
        return df


class ElementTreeStrategy(Strategy):
    def parse_xml(self, xml_source_file) -> pd.DataFrame:
        from xml.etree import ElementTree
        xml = ElementTree.parse(xml_source_file)
        rows = []
        for row in xml.findall("row"):
            if row:
                try:
                    line = dict()
                    for el in cols:
                        tmp = row.find(el)
                        line[el] = tmp.text
                    rows.append(line)
                finally:
                    continue

        df = pd.DataFrame(rows, columns=cols)

        return df


if __name__ == "__main__":

    print()

