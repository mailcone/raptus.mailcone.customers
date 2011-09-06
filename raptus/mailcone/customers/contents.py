import grok

from zope import schema

from raptus.mailcone.customers import interfaces
from raptus.mailcone.core.interfaces import IMailcone
from raptus.mailcone.core.bases import BaseLocator


class Customer(grok.Container):
    """ A customer
    """
    grok.implements(interfaces.ICustomer)


class CustomerContainer(grok.Container):
    """ A container for Customers
    """
    grok.implements(interfaces.ICustomersContainer)
    


@grok.subscribe(IMailcone, grok.IApplicationInitializedEvent)
def init_customers_container(obj, event):
    obj['customers'] = CustomerContainer()

class CustomersContainerLocator(BaseLocator):
    splitedpath = ['customers']
grok.global_utility(CustomersContainerLocator, provides=interfaces.ICustomersContainerLocator)