#!/usr/bin/env python
#-*- coding: utf-8 -*-

#
# DESCRIPTION
#
# a library holding useful and object-oriented functionalities to interface with
# a (freeplane) mindmap. using this library, information can easily be extracted
# and used in a programmatical way without having to browse through the mindmap
# itself.
#
#
# AUTHOR
#
#   - nnako, 2016
#


# generals
from __future__ import print_function
import argparse
import os
import re
import sys

# xml format
import xml.etree.ElementTree as ET


# MINDMAP

class Mindmap(object):

    """
    Freeplane interfacing class

    Access Freeplane mindmap file and do various search, read and write
    operations to retrieve or modify text passages within the mindmap.

    """

    num_of_maps = 0

    def __init__(self, path='', type='freeplane', version='1.3', id=''):




        #
        # define main command line arguments
        #

        # do this only if called from the command line
        if id == 'cli':

            # define information
            parser = argparse.ArgumentParser(
                    description='Operation on Freeplane mindmap',
                    usage='''%s <command> [<args>]

Possible commands are:
    getText    return text portion of a node
    ...               ...''' % os.path.basename(sys.argv[0]))

            # define command argument
            parser.add_argument(
                    'command',
                    help='Subcommand to run'
                    )




            #
            # read out CLI and execute main command
            #

            # get main arguments from user
            args = parser.parse_args(sys.argv[1:2])

            # check if command is provided in script
            if not hasattr(self, args.command):

                print( 'Unrecognized command' )
                parser.print_help()
                exit(1)

            # use dispatch pattern to invoke method with same name
            getattr(self, args.command)()




        #
        # access class variables
        #

        Mindmap.num_of_maps += 1




        #
        # access instance variables and read mindmap
        #

        # path of instance's mindmap file
        self.path = path

        # type, version
        self.type = type
        self.version = version

        # read entire etree mindmap
        self.mindmap = ET.parse(self.path)

        # get root of mindmap
        self.root = self.mindmap.getroot()

        # find and get first node element of etree
        self.rootNode = self.root.find('node')


# MAP

    @classmethod
    def getNumOfMaps(cls):
        return cls.num_of_maps


    @property
    def RootNode(self):
        return Node(self.rootNode)


    def findNodes(self,
            id='',
            core='',
            attrib='',
            details='',
            notes='',
            link='',
            exact=False
            ):

        #
        # find list of nodes in map
        #

        # init
        lstNodes = []

        # check for ID
        if not id == '':

            # list nodes matching specific ID
            lstNodes = self.root.findall(".//*[@ID='" + id + "']")

        # nothing given
        else:

            # list all nodes regardless of further properties
            lstNodes = self.root.findall(".//node")

        # create Node instances
        lstNodesRet = []
        for _node in lstNodes:
            lstNodesRet.append(Node(_node))

        return lstNodesRet


# NODE

class Node(object):

    def __init__(self, node):

        #
        # initialize instance
        #

        self.node = node
        self.id = node.attrib['ID']
        self.attribute = {}
        _lst = node.findall('attribute')
        for _attr in _lst:
            _name = _attr.get('NAME', '')
            _value = _attr.get('VALUE', '')
            if not _name == '':
                self.attribute[_name] = _value


    @property
    def PlainText(self):
        return getCoreTextFromNode(self.node, bOnlyFirstLine=False)


    @property
    def Id(self):
        return self.id


    @property
    def Attributes(self):
        return self.attribute


    @property
    def Style(self):
        if 'STYLE_REF' in self.node.attrib.keys():
            return self.node.attrib['STYLE_REF']
        return ""


    @property
    def CoreLink(self):

        # check for TEXT attribute
        if not self.node.get('TEXT') is None:

            # read out text content
            text = self.node.attrib['TEXT']

            if len(text) > 0 \
                    and text[0] == "=":




                #
                # check for reference to external node
                #

                # identify link based on type (file, http, ...)




                #
                # check for reference to internal node
                #

                _match=re.match(r'^.*ID_([\d]+)\.text.*', text)
                # valid match found?
                if _match:
                    return 'ID_' + _match.group(1)




        return ""


    @property
    def Comment(self):

        # check for existence of child
        if not self.node.find('node') is None:

            # get first child
            node = self.node.find('node')

            # check for TEXT attribute
            if not node.get('TEXT') is None:

                # read out text content
                return node.attrib['TEXT']

        return ""


    @property
    def Children(self):
        lstNodes = []
        for item in  self.node.findall("./node"):
            lstNodes.append(Node(item))
        return lstNodes


    @property
    def isComment(self):
        if not self.node.get('STYLE_REF') is None \
                and self.node.attrib['STYLE_REF'] == 'klein und grau':
            return True
        return False


    @property
    def hasChildren(self):
        if not self.node.findall('./node'):
            return False
        return True


    def findNodes(self,
                 id='',
                 core='',
                 attrib='',
                 details='',
                 notes='',
                 link='',
                 exact=False
                 ):

        #
        # find list of nodes in map
        #

        # init
        lstNodes = []

        # check for ID
        if not id == '':

            # list nodes matching specific ID
            lstNodes = self.node.findall(".//*[@ID='" + id + "']")

        # check other properties...

        # nothing given
        else:

            # list all nodes regardless of further properties
            lstNodes = self.node.findall(".//node")

        # create Node instances
        lstNodesRet = []
        for _node in lstNodes:
            lstNodesRet.append(Node(_node))

        return lstNodesRet


    def findChildren(self,
                 id='',
                 core='',
                 attrib='',
                 details='',
                 notes='',
                 link='',
                 exact=False
                 ):

        #
        # find list of nodes in map
        #

        # init
        lstNodes = []

        # check for ID
        if not id == '':

            # list nodes matching specific ID
            lstNodes = self.node.findall("./*[@ID='" + id + "']")

        # check others...

        # nothing given
        else:

            # list all nodes regardless of further properties
            lstNodes = self.node.findall("./node")

        # create Node instances
        lstNodesRet = []
        for _node in lstNodes:
            lstNodesRet.append(Node(_node))

        return lstNodesRet


    def getSubText(self, token=''):

        # initialize contents
        text = ""
        commentnode = None

        #
        # find node's INTERMEDIATE child node
        #

        # skip tokennode if token present
        if not token == "":

            # check for token node
            tokennode = self.node.findall("./node[@TEXT='" + token + "']")
            if not tokennode == []:

                # go further to find the comment text
                commentnode = tokennode[0].find('./node')

        else:

            # get first node node as comment node
            commentnode = self.node.find('./node')

        #
        # access text portion of target node
        #

        # if comment node exists
        if commentnode is not None:

            # get comment text
            text = getCoreTextFromNode(commentnode, bOnlyFirstLine=False)

        else:

            # text is invalid
            text = ""

        return text


# FUNCTIONS

def getCoreTextFromNode(node, bOnlyFirstLine=False):

    # initialize text content
    text = ""

    #
    # get TEXT attribute of node if present
    #

    if not node.get('TEXT') is None:

        # read out text content
        text = node.attrib['TEXT']

    #
    # strip text from RICHTEXT content if present
    #

    elif not node.find('richcontent') is None:

        # get richtext node
        richnode = node.find('richcontent')

        # get html node
        htmlnode = richnode.find('html')

        # get html body node
        htmltext = htmlnode.find('body')

        # filter out plain text content
        raw = "".join([x for x in htmltext.itertext()])

        #
        # filter first line if desired
        #

        if bOnlyFirstLine:

            # take only first line of text content
            text = raw.strip().split('\n')[0].strip()

        else:

            # replace <CR> and leading / trailing <SPACE>
            raw__no_CR = raw.replace('\n', '')
            text = raw__no_CR.strip()

    return text


# OLD

# read text paragraph from mindmap
def getText(self, strRootAttribute, strTitleText, strPortion):

    # get list of all attributes
    lstAttributes = self.mindmap.getElementsByTagName('attribute')

    # search for ROOT ATTRIBUTE NODE
    for item in lstAttributes:
        if item.attributes['NAME'].value == 'type' and \
                item.attributes['VALUE'].value == strRootAttribute:
            rootnode = item.parentNode

    # get list of all nodes below
    lstNodes = rootnode.getElementsByTagName('node')

    # look for node containing TITLE STRING
    for item in lstNodes:
        if item.hasAttribute('TEXT'):
            if item.getAttribute('TEXT') == strTitleText:
                titlenode = item

    # get list of all nodes below
    lstNodes = titlenode.getElementsByTagName('node')

    # look for node containing PORTION STRING
    for item in lstNodes:
        if item.hasAttribute('TEXT'):
            if item.getAttribute('TEXT') == strPortion:
                portionnode = item

    # if there is no richtext content ...
    if not portionnode.getElementsByTagName('richcontent'):

        # get next following single node
        textnode = portionnode.getElementsByTagName('node')[0]

        # get standard TEXT attribute
        strText = textnode.getAttribute('TEXT')

    else:

        # look for HTML content
        richcontents = portionnode.getElementsByTagName('richcontent')

        # convert content to HTML
        strHtml = richcontents[0].toxml()

        # convert HTML to MARKDOWN ASCII
        strText = html2text.html2text(strHtml)

    # replace cryptic text passages
    strText = strText.replace('&lt;', '<')
    strText = strText.replace('&gt;', '>')

    # return value back to caller
    return strText


#
# execute this module code
#

if __name__ == "__main__":

    # execute class init with command line environment
    Mindmap(id='cli')
