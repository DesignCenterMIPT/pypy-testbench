from importlib import import_module


etree = import_module('xml.etree.ElementTree')


if __name__ == "__main__":
    try:
        from xml.parsers import expat
    except ImportError:
        try:
            import pyexpat as expat
        except ImportError:
            raise ImportError("No module named expat; use SimpleXMLTreeBuilder instead")
    
    parser = expat.ParserCreate(None, "}")
   
    with open("data/xml_data.bin", mode="rb") as bfile:
        xml_data = bfile.read()
    
    for _ in range(1000):
        etree.fromstring(xml_data)

