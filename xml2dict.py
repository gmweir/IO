# -*- coding: utf-8 -*-
"""
Created on Tue Jun 20 21:37:30 2017

@author: gawe
"""

from xml.etree import ElementTree

class XmlListConfig(list):
    def __init__(self, aList):
        for element in aList:
            if element:
                # treat like dict
                if len(element) == 1 or element[0].tag != element[1].tag:
                    self.append(XmlDictConfig(element))
                # treat like list
                elif element[0].tag == element[1].tag:
                    self.append(XmlListConfig(element))
            elif element.text:
                text = element.text.strip()
                if text:
                    self.append(text)


class XmlDictConfig(dict):
    '''
    Example usage:

    >>> tree = ElementTree.parse('your_file.xml')
    >>> root = tree.getroot()
    >>> xmldict = XmlDictConfig(root)

    Or, if you want to use an XML string:

    >>> root = ElementTree.XML(xml_string)
    >>> xmldict = XmlDictConfig(root)

    And then use xmldict for what it is... a dict.
    '''
    def __init__(self, parent_element):
        if parent_element.items():
            self.update(dict(parent_element.items()))
        for element in parent_element:
            if element:
                # treat like dict - we assume that if the first two tags
                # in a series are different, then they are all different.
                if len(element) == 1 or element[0].tag != element[1].tag:
                    aDict = XmlDictConfig(element)
                # treat like list - we assume that if the first two tags
                # in a series are the same, then the rest are the same.
                else:
                    # here, we put the list in dictionary; the key is the
                    # tag name the list elements all share in common, and
                    # the value is the list itself 
                    aDict = {element[0].tag: XmlListConfig(element)}
                # if the tag has attributes, add those to the dict
                if element.items():
                    aDict.update(dict(element.items()))
                self.update({element.tag: aDict})
            # this assumes that if you've got an attribute in a tag,
            # you won't be having any text. This may or may not be a 
            # good idea -- time will tell. It works for the way we are
            # currently doing XML configuration files...
            elif element.items():
                self.update({element.tag: dict(element.items())})
            # finally, if there are no child tags and no attributes, extract
            # the text
            else:
                self.update({element.tag: element.text})


#
## calling example
#def main():
#    
#    import os as _os
#    infil = _os.path.join('G:/','Workshop','DataOP11','XP20160302.008','input_data.xml')
#    outfil = _os.path.join('G:/','Workshop','DataOP11','XP20160302.008','example.xml')
#    travisdict = ConvertXmlToDict(infil)
#    print(travisdict)
#    
#    root = ConvertDictToXml(travisdict)
#    tree = ElementTree.ElementTree(root)
#    tree.write(outfil)
#    
##    configdict = ConvertXmlToDict('config.xml')
##    print(configdict)
##
##    # you can access the data as a dictionary
##    print(configdict['settings']['color'])
##    configdict['settings']['color'] = 'red'
##
##    # or you can access it like object attributes
##    print(configdict.settings.color)
##    configdict.settings.color = 'red'
##
##    root = ConvertDictToXml(configdict)
##
##    tree = ElementTree.ElementTree(root)
##    tree.write('config.new.xml')
#
#
## Module Code:
#
#class XmlDictObject(dict):
#    """
#    Adds object like functionality to the standard dictionary.
#    """
#
#    def __init__(self, initdict=None):
#        if initdict is None:
#            initdict = {}
#        dict.__init__(self, initdict)
#    
#    def __getattr__(self, item):
#        return self.__getitem__(item)
#    
#    def __setattr__(self, item, value):
#        self.__setitem__(item, value)
#    
#    def __str__(self):
#        if self.has_key('_text'):
#            return self.__getitem__('_text')
#        else:
#            return ''
#
#    @staticmethod
#    def Wrap(x):
#        """
#        Static method to wrap a dictionary recursively as an XmlDictObject
#        """
#
#        if isinstance(x, dict):
#            return XmlDictObject((k, XmlDictObject.Wrap(v)) for (k, v) in x.iteritems())
#        elif isinstance(x, list):
#            return [XmlDictObject.Wrap(v) for v in x]
#        else:
#            return x
#
#    @staticmethod
#    def _UnWrap(x):
#        if isinstance(x, dict):
#            return dict((k, XmlDictObject._UnWrap(v)) for (k, v) in x.iteritems())
#        elif isinstance(x, list):
#            return [XmlDictObject._UnWrap(v) for v in x]
#        else:
#            return x
#        
#    def UnWrap(self):
#        """
#        Recursively converts an XmlDictObject to a standard dictionary and returns the result.
#        """
#
#        return XmlDictObject._UnWrap(self)
#
#def _ConvertDictToXmlRecurse(parent, dictitem):
#    assert type(dictitem) is not type([])
#
#    if isinstance(dictitem, dict):
#        for (tag, child) in dictitem.iteritems():
#            if str(tag) == '_text':
#                parent.text = str(child)
#            elif type(child) is type([]):
#                # iterate through the array and convert
#                for listchild in child:
#                    elem = ElementTree.Element(tag)
#                    parent.append(elem)
#                    _ConvertDictToXmlRecurse(elem, listchild)
#            else:                
#                elem = ElementTree.Element(tag)
#                parent.append(elem)
#                _ConvertDictToXmlRecurse(elem, child)
#    else:
#        parent.text = str(dictitem)
#    
#def ConvertDictToXml(xmldict):
#    """
#    Converts a dictionary to an XML ElementTree Element 
#    """
#
#    roottag = xmldict.keys()[0]
#    root = ElementTree.Element(roottag)
#    _ConvertDictToXmlRecurse(root, xmldict[roottag])
#    return root
#
#def _ConvertXmlToDictRecurse(node, dictclass):
#    nodedict = dictclass()
#    
#    if len(node.items()) > 0:
#        # if we have attributes, set them
#        nodedict.update(dict(node.items()))
#    
#    for child in node:
#        # recursively add the element's children
#        newitem = _ConvertXmlToDictRecurse(child, dictclass)
#        if nodedict.has_key(child.tag):
#            # found duplicate tag, force a list
#            if type(nodedict[child.tag]) is type([]):
#                # append to existing list
#                nodedict[child.tag].append(newitem)
#            else:
#                # convert to list
#                nodedict[child.tag] = [nodedict[child.tag], newitem]
#        else:
#            # only one, directly set the dictionary
#            nodedict[child.tag] = newitem
#
#    if node.text is None: 
#        text = ''
#    else: 
#        text = node.text.strip()
#    
#    if len(nodedict) > 0:            
#        # if we have a dictionary add the text as a dictionary value (if there is any)
#        if len(text) > 0:
#            nodedict['_text'] = text
#    else:
#        # if we don't have child nodes or attributes, just set the text
#        nodedict = text
#        
#    return nodedict
#        
#def ConvertXmlToDict(root, dictclass=XmlDictObject):
#    """
#    Converts an XML file or ElementTree Element to a dictionary
#    """
#
#    # If a string is passed in, try to open it as a file
#    if type(root) == type(''):
#        root = ElementTree.parse(root).getroot()
#    elif not isinstance(root, ElementTree.Element):
#        raise(TypeError, 'Expected ElementTree.Element or file path string')
#
#    return dictclass({root.tag: _ConvertXmlToDictRecurse(root, dictclass)})
#
#
#if __name__ == '__main__':       
#    main()
#    

