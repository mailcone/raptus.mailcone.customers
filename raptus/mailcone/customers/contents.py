import grok

from zope import schema

from raptus.mailcone.customers import interfaces
from raptus.mailcone.core.interfaces import IMailcone



class Customer(grok.Container):
    """ A customer
    """
    grok.implements(interfaces.ICustomer)
    #id = schema.fieldproperty.FieldProperty(interfaces.ICustomer['id'])


class CustomerContainer(grok.Container):
    """ A container for Customers
    """
    grok.implements(interfaces.ICustomersContainer)
    


@grok.subscribe(IMailcone, grok.IApplicationInitializedEvent)
def init_customers_container(obj, event):
    obj['customers'] = CustomerContainer()


@grok.adapter(interfaces.ICustomersContainerHolder)
@grok.implementer(interfaces.ICustomersContainer)
def customers_container_of_holder(holder):
    return holder['customers']