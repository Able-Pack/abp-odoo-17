import json
from lxml import etree

def _apply_field_options(res, paths=[], no_create=False, no_create_edit=False, no_open=False, no_quick_create=False):
    """
    Applies no_create, no_create_edit, and no_quick_create options to all fields.
    """
    doc = etree.XML(res["arch"])
    for path in paths:
        for node in doc.xpath(path):
            options = node.attrib.get("options", "{}")
            options = options.strip().replace('true', 'True').replace('false', 'False')
            # Update options dictionary with the restrictions
            options_dict = eval(options) if options.strip() else {}
            options_dict.update({
                'no_create': True if no_create else False,
                'no_create_edit': True if no_create_edit else False,
                'no_open': True if no_open else False,
                'no_quick_create': True if no_quick_create else False,
            })
            node.set("options", str(options_dict))
        
    res["arch"] = etree.tostring(doc, encoding="unicode")
    
def apply_list_record_limit(res, paths=[], limit=80):
    """
    Applies record limit to list view.
    """
    doc = etree.XML(res["arch"])
    for path in paths:
        for node in doc.xpath(path):
            node.set('limit', str(limit))
    res["arch"] = etree.tostring(doc, encoding="unicode")

def set_readonly(doc, value, paths=[],):
    for path in paths:
        for node in doc.xpath(path):
            node.set('readonly', str(value))
            
            
def set_invisible(doc, value, paths=[]):
    for path in paths:
        for node in doc.xpath(path):
            node.set('invisible', str(value))
            node.set('column_invisible', str(value))
            
            
def set_no_create_edit_delete(doc, paths=[], no_create=False, no_edit=False, no_delete=True):
    for path in paths:
        for node in doc.xpath(path):
            node.set('create', '0') if no_create else None
            node.set('edit', '0') if no_edit else None
            node.set('delete', '0') if no_delete else None
            
def set_field_option(doc, paths=[], no_create=False, no_create_edit=False, no_open=False, no_quick_create=False):
    for path in paths:
        for node in doc.xpath(path):
            options = {
                'no_create': True if no_create else False,
                'no_create_edit': True if no_create_edit else False,
                'no_open': True if no_open else False,
                'no_quick_create': True if no_quick_create else False,
            }
            options_json = json.dumps(options, indent=2).encode('utf-8')
            node.set('options', options_json)
            
def set_empty_widget(doc, paths=[]):
    for path in paths:
        for node in doc.xpath(path):
            node.set('widget', '')
            
def user_has_any_group(self, group_xml_ids):
    return any(self.env.user.has_group(group_id) for group_id in group_xml_ids)
            
            