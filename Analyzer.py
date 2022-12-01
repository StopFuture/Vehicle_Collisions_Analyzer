from VisualElements.Grouper import *
from VisualElements.Articles import *
from VisualElements.Breakers import *
from VisualElements.CustomMaps import *
from ControlElements.ConverterToHTML import *
# starter = streamlit run Analyzer.py

__all__ = [st, pd, np, pdk, px]
DATE_TIME = "date/time"


st.set_page_config(page_title="Analyzer", page_icon="💥🗺", layout="centered", initial_sidebar_state="auto",
                   menu_items=None)
st.title("Motor Vehicle Collisions Analyzer")


st.markdown("This multi-page application is a Streamlit dashboard that can \
            be used to analyze XML and CSV file from the State Automobile Inspection 🚔💥")
st.markdown("🔵     Author: **Andriy Fedorych**")
st.markdown("🟡     GitHub: [**StopFuture**](https://github.com/StopFuture)")

st.sidebar.success("Select a page above.")


StarterInit()

upload_xml = False
upload_check = False


file2 = st.file_uploader("Upload SAI file", type=["xml", "csv"])

if file2 is not None:
    st.session_state["source_file"] = file2

source_file = st.session_state["source_file"] if st.session_state["source_file"] is not None else file2
st.session_state["source_file"] = source_file

if source_file is not None and upload_check is False:
    try:
        if source_file.name[-3:] == "xml":
            context_t = DefParserXML(XMLDictStrategy())
            context_t.strategy = XMLDictStrategy()

            imported = context_t.extract_data(source_file)
            source_file.seek(0)
            Converter = ConverterToHTML(source_file.name)
            st.markdown("You uploaded XML file! ")
            st.session_state["imported"] = imported

            upload_xml = True
            upload_check = True
            st.session_state["upload_xml"] = upload_xml
            st.session_state["upload_check"] = upload_check

        elif source_file.name[-3:] == "csv":
            if st.session_state["imported"] is None:
                imported = pd.read_csv(source_file)
                st.session_state["imported"] = imported

            imported = st.session_state["imported"]
            st.session_state["imported"] = imported
            st.markdown("You uploaded CSV file! ")
            upload_check = True
            upload_xml = False
            st.session_state["upload_xml"] = upload_xml
            st.session_state["upload_check"] = upload_check

    except Exception as exp:
        x = exp
        st.markdown("⚠️   ️**The file is not from the SAI system, try upload another file**")
        # st.markdown(x)
else:
    upload_check = False
    st.session_state["upload_check"] = upload_check

if upload_check:
    if upload_xml:
        ArticleXML()
        StrategyTester(source_file)
    else:
        ArticleCSV()
