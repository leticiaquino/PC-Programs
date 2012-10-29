import xml.etree.ElementTree as etree
import os

class XMLManager:

    root = {}
    debug = True

    def __init__(self, table_ent):
        self.root = None
        
        
        self.invalid = []
        self.table_ent = table_ent
        self.error_message = ''

        try:
            self.parser = etree.XMLParser(recover=True, remove_blank_text=True, resolve_entities=False) #recovers from bad characters.
        except:
            self.parser = None
    
        

    def _load(self, xml_filename):
        self.ns = ''
        self.root = None
        self.report.write('_load ' + xml_filename)
        try:
            if self.parser != None:
                self.report.write('_load self.parser != None')
                self.root = etree.parse(xml_filename, self.parser).getroot()
            else:
                self.report.write('_load self.parser == None')
                self.root = etree.parse(xml_filename).getroot()
            
            if '{' in self.root.tag:
                self.ns = self.root.tag[0:self.root.tag.find('}')+1]
            else:
                self.ns = ''
            
            r = True
        except Exception as inst:
            self.report.write('Unable to load ' + xml_filename, True, True, False, inst)
            r = False
        return r

    def load(self, xml_filename, report):
        self.report = report

        r = False
        if os.path.exists(xml_filename):
            r = self._load(xml_filename)

            if not r:
                from tempfile import mkstemp
                _, new_xml_filename = mkstemp()

                self.named2number(xml_filename, new_xml_filename)
                r = self._load(new_xml_filename)
                if not r:
                    import shutil
                    shutil.copyfile(new_xml_filename,xml_filename.replace('.xml', '.fixed.xml'))
                    self.report.write('Invalid XML file:' + xml_filename.replace('.xml', '.fixed.xml'), True, True)
                os.unlink(new_xml_filename)
        else:
            self.report.write('Missing XML file:' + xml_filename, True, True)
        return r

    

    def named2number(self, xml_filename, new_xml_filename):
        
        self.report.write('named2number:' + xml_filename)
        f = open(xml_filename, 'r')
        original = f.read()
        f.close()
        
        self.report.write('named2number:' + new_xml_filename)
        f = open(new_xml_filename, 'w')
        f.write(self.table_ent.replace_to_numeric_entities(original))
        f.close()
    
    def return_nodes(self, xpath = '', current_node = None):
        r = []
        n = current_node
        if n == None:
            n = self.root

        if n != None:
            if xpath != '':
                p = self.ns + xpath
                try:
            	    r = n.findall(p)
            	except:
            	    self.report.write('Invalid xpath: ' + p)
            else:
                p = '.'
                r.append(n)
            n_str = ''
            if len(n)>0:
                n_str = etree.tostring(n)
        return r

    def return_node_value(self, node):
        r = '' 
        s = ''
        if node != None:
            n = 0
            children = node.iter()
            for child in children:
                n +=1
            if n == 1:
                r = node.text
            if n > 1:
                r = etree.tostring(node)
                
                r = r[r.find('>')+1:]
                r = r[0:r.rfind('</')]
            try:
                s = r.strip()
            except:
                s = ''
                self.report.write('Empty element')
                self.report.write('node', False, False, False, node)
                self.report.write('n', False, False, False, n)
                self.report.write('r', False, False, False, r)        
        return s
    
    def return_xml(self, node):
        r = '' 
        
        if node != None:
            r = etree.tostring(node)
             
        return r
    
    
    
    def return_node_attr_value(self, node, attr_name):
        attr = '' 
        if node != None:
            if len(node.attrib)>0:
                if ':' in attr_name:
                    aname = attr_name[attr_name.find(':')+1:]
                    for k,a in node.attrib.items():
                        if aname == k[k.find('}')+1:]:
                            attr = a 
                else:
                    if attr_name[0:1] == '@':
                        attr_name = attr_name[1:]
                    try:
                        attr = node.attrib[attr_name]
                    except:
                        attr = ''
            
        return attr  
