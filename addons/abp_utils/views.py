import json


def set_readonly(doc, paths=[]):
    for path in paths:
        for node in doc.xpath(path):
            modifiers = json.loads(node.attrib.pop('modifiers', '{}'))
            modifiers['readonly'] = True
            node.set("modifiers", json.dumps(modifiers))
            
            
def set_invisible(doc, paths=[]):
    for path in paths:
        for node in doc.xpath(path):
            modifiers = json.loads(node.attrib.pop('modifiers', '{}'))
            modifiers['invisible'] = True
            modifiers['column_invisible'] = True
            node.set("modifiers", json.dumps(modifiers))
            
            
def set_no_create_edit_delete(doc, paths=[], no_create=False, no_edit=False, no_delete=True):
    for path in paths:
        for node in doc.xpath(path):
            node.set('create', '0') if no_create else None
            node.set('edit', '0') if no_edit else None
            node.set('delete', '0') if no_delete else None
            
            
def user_has_any_group(self, group_xml_ids):
    return any(self.env.user.has_group(group_id) for group_id in group_xml_ids)
            
            