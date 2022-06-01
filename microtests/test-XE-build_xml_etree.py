import xml.etree.ElementTree as etree


def build_xml_tree():
    SubElement = etree.SubElement
    root = etree.Element('root')

    # create a couple of repetitive broad subtrees
    for c in range(50):
        child = SubElement(root, 'child-%d' % c,
                                 tag_type="child")
        for i in range(100):
            SubElement(child, 'subchild').text = 'LEAF-%d-%d' % (c, i)

    # create a deep subtree
    deep = SubElement(root, 'deepchildren', tag_type="deepchild")
    for i in range(50):
        deep = SubElement(deep, 'deepchild')
    SubElement(deep, 'deepleaf', tag_type="leaf").text = "LEAF"

    # store the number of elements for later
    nb_elems = sum(1 for elem in root.iter())
    root.set('nb-elems', str(nb_elems))


build_xml_tree()

