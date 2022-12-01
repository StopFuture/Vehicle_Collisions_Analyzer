from VisualElements.Charts import *


class ArticleCSV:
    def __init__(self):
        st.header("CSV Overview")
        st.markdown("**CSV – a comma-separated values file. AKA Character Separated Values, or Comma Delimited file**")
        st.markdown("File example:")
        st.code("Year,Make,Model,Length\n"
                "1997,Ford,E350,2.35\n"
                "2000,Mercury,Cougar,2.38", language="python")
        st.markdown("Processing csv files is made easier by using the Pandas library,"
                    " just run the following code snippet")
        st.code('''import pandas as pd
    data = pd.read_csv(source_file) # the file stored as a DataFrame ''',  language="python")


class ArticleIntro:
    def __init__(self):
        st.write("Note that you could see some of the information on the main page after uploading the file.")


class ArticleXML:
    def __init__(self):
        st.header("XML Parser Overview")
        st.markdown("Everyone knows the structure of an XML file: ")
        st.code('''<root>
    <row>
        <a1>XML</a1>
        <a2>Example</a2>
    </row>
</root>''', language="xml")
        st.markdown("So let's look at ways to process them using Python:")
        st.subheader("Untangle Strategy")
        st.markdown("Untangle is a tiny Python library which converts an XML document to a Python object. "
                    "This approach is equivalent to the classic DOM strategy, "
                    "because it reads the entire file to the clipboard, "
                    "and  builds a Node Tree with certain connections. ")
        st.markdown("It works rather slowly due to the approach to the task, "
                    "but it is very convenient to use because you need to remember essentially one function")
        st.code('''untangle.parse("file_name.xml")''', language="python")
        st.subheader("Element Tree Strategy")
        st.markdown("If you want cool performance, the broadest spectrum of functionality, "
                    "and the most familiar interface to SAX strategy and all wrapped in one package, "
                    "then use ElementTree and forget about the rest of the libraries.")
        st.code('''from xml.etree import ElementTree
    xml = ElementTree.parse(xml_file)''')
        st.subheader("XML Dict Strategy")
        st.markdown("If you like JSON but you’re not a fan of XML, then check out xmltodict, "
                    "which tries to bridge the gap between both data formats. "
                    "As the name implies, the library can parse an XML document"
                    " and represent it as a Python dictionary,"
                    " which also happens to be the target data type for JSON documents in Python."
                    " This makes conversion between XML and JSON possible.")
        st.code('''import xmltodict
    with open(xml_source_file) as xmlfile:
        xml = xmltodict.parse(xmlfile.read())''', language="python")
        st.markdown("Obviously, this is my favorite, "
                    "because the JSON format is gradually taking up all the space and displacing XML files.")
        st.markdown("Below is a graph showing how the parsing time of an xml "
                    "file depends on the number of lines in it.")

        LC = LineChart()
        st.pyplot(LC.fig)
        st.markdown("The default XML Dict Strategy is used,"
                    " but you can choose something else to further process the file.")
