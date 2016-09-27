# -*- coding: utf-8 -*-

from tastypie.resources import ModelResource, NamespacedModelResource
from tastypie.fields import ToManyField
from tastypie.exceptions import BadRequest
from django.utils import six

ALL_FIELDS = ''

class SpecificFieldsResource(NamespacedModelResource):

    def get_object_list(self, request):

        filters = super(SpecificFieldsResource, self).build_filters()
        objects = super(SpecificFieldsResource, self).get_object_list(request)

        self.specified_fields = dict()
        
        fields = request.GET.get("fields", False)
        if fields:
            self.specified_fields = parse_specified_fields(fields)

        return objects

    def full_dehydrate(self, bundle, for_list=False):

        """
        This override disables `full=True` and other things we don't use
        """

        # call the base class if no specified fields
        if not hasattr(self, 'specified_fields') or not self.specified_fields or self.specified_fields == ALL_FIELDS:
            return super(SpecificFieldsResource, self).full_dehydrate(bundle, for_list)

        use_in = ['all', 'list' if for_list else 'detail']

        # Dehydrate each field.
        for field_name, field_object in self.fields.items():
            #If it does not exist in specified fields, skip
            if not field_name in self.specified_fields:
                continue

            # If it's not for use in this mode, skip
            field_use_in = getattr(field_object, 'use_in', 'all')
            if callable(field_use_in):
                if not field_use_in(bundle):
                    continue
            else:
                if field_use_in not in use_in:
                    continue

            sf = self.specified_fields.get(field_name, ALL_FIELDS)

            # A touch leaky but it makes URI resolution work.
            if getattr(field_object, 'dehydrated_type', None) == 'related':
                field_object.api_name = self._meta.api_name
                field_object.resource_name = self._meta.resource_name

                # We add the specified fields for this related field
                if not isinstance(field_object, ToManyField):
                    field_object.to.specified_fields = sf

            bundle.data[field_name] = field_object.dehydrate(bundle, for_list=for_list)

            # Check for an optional method to do further dehydration.
            method = getattr(self, "dehydrate_%s" % field_name, None)

            if method:
                bundle.data[field_name] = method(bundle)

            # Processing of the ToManyField
            if not sf == ALL_FIELDS:
                if isinstance(field_object, ToManyField):
                    for bund in bundle.data[field_name]:
                        d = dict()
                        for f in sf:
                            if f in bund.data:
                                d[f] = bund.data[f]

                        bund.data = d

        bundle = self.dehydrate(bundle)
        return bundle

def parse_specified_fields(fields):

    """
    A function that parse the 'fields' string to the corresponding dict
    """

    fields = fields.replace(" ", "")
    fields_copy = fields
    empty_char = "#" # The character to mark the already processed part of the fields parameter
    
    # The list of all the temporary found attributes
    tuples = []
    
    # Identification of all the commas, the opening and closing parentheses
    opening = []
    closing = []
    commas = []
    for i in range(len(fields)):
        if fields[i] == "(":
            opening.append(i)
        elif fields[i] == ")":
            closing.append(i)
        elif fields[i] == ",":
            commas.append(i)

    # Browsing all the opening parentheses (finding all the related objects)
    while opening:
        op = opening.pop()
        
        # Looking for the corresponding closing parenthese
        clo = None
        for ind in range(len(closing)):
            if closing[ind] > op:
                clo = closing.pop(ind)
                break

        if not clo: # Badly formatted expression
            raise BadRequest("Invalid resource lookup data provided. The fields attribute '%s' is invalid." % (fields_copy))

        # Looking for the corresponding comma
        com = -1
        ind = len(commas) - 1
        while ind >= 0:
            if commas[ind] < op:
                com = commas[ind]
                break
            ind -= 1
        if opening:
            com = max(com, opening[-1] + 1)
        if com == -1:
            com = 0
        current = fields[com:clo+1].replace(empty_char, "") # Extracting the part to be processed

        # Marking the 'current' string as already processed
        chars = list(fields)
        for i in range(clo-com+1):
            chars[com + i] = empty_char
        fields = "".join(chars)

        tmp = current.split("(")
        if not len(tmp) == 2: # Badly formatted expression
            raise BadRequest("Invalid resource lookup data provided. The fields attribute '%s' is invalid." % (fields_copy))

        # Processing the 'current' part of the fields
        attr = tmp[0].replace(",", "")
        vals = dict()
        temp = tmp[1].replace(")", "").split(",")
        if temp == ['']:
            vals = ALL_FIELDS
        else:
            for att in temp:
                vals[att] = ALL_FIELDS
        tuple = (op, clo, attr, vals)
        tuples.append(tuple)

    if closing: # Badly formatted expression (There are still closing parentheses)
        raise BadRequest("Invalid resource lookup data provided. The fields attribute '%s' is invalid." % (fields_copy))

    
    ############### Construction of the final dict ##################
    f = dict()
    
    # Processing the direct attributes without related objects
    fs = fields.replace(empty_char, "").replace(" ","")
    if fs:
        for field in fs.split(","):
            f[field] = ALL_FIELDS
    
    # Processing the other related objects (those objects have been registered in the 'tuples' list)
    l = len(tuples)
    for i in range(l):
        tuple = tuples[i]
        begin = tuple[0]
        end = tuple[1]
        attr = tuple[2]
        vals = tuple[3]
        
        # Browsing the parts, looking for the first parent of this object
        j = i + 1
        found = False
        while j < l:
            tup = tuples[j]
            current_begin = tuples[j][0]
            current_end = tuples[j][1]
            
            # Look if it is included in the other part of the fields and add it as an attribute of that object
            if (current_begin < begin < current_end) and (current_begin < end < current_end):
                found = True
                if not isinstance(tuples[j][3], dict):
                    temp_tup = (current_begin, current_end, tuples[j][2], dict())
                    tuples[j] = temp_tup
                tuples[j][3][attr] = vals
                break
                
            j += 1
                
        if not found: # It is a direct attribute
            f[attr] = vals

    # print f
    return f
