import grok

from zope import schema

from raptus.mailcone.customers import interfaces
from raptus.mailcone.core import bases
from raptus.mailcone.core.interfaces import IMailcone, ISearchable


class Customer(bases.Container):
    grok.implements(interfaces.ICustomer)
    
    id = None
    name = None
    address = None


class CustomerContainer(bases.Container):
    grok.implements(interfaces.ICustomersContainer)

@grok.subscribe(IMailcone, grok.IApplicationInitializedEvent)
def init_customers_container(obj, event):
    obj['customers'] = CustomerContainer()

class CustomersContainerLocator(bases.BaseLocator):
    splitedpath = ['customers']
grok.global_utility(CustomersContainerLocator, provides=interfaces.ICustomersContainerLocator)