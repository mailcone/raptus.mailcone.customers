import grok

from zope import schema

from raptus.mailcone.customers import interfaces
from raptus.mailcone.core.interfaces import IMailcone
from raptus.mailcone.core.bases import BaseLocator


class Customer(grok.Container):
    grok.implements(interfaces.ICustomer)
    def __init__(self, name, address):
        super(Customer, self).__init__()
        self.id = name.lower().replace(' ', '_')
        self.name = name
        self.address = address


class CustomerContainer(grok.Container):
    grok.implements(interfaces.ICustomersContainer)

@grok.subscribe(IMailcone, grok.IApplicationInitializedEvent)
def init_customers_container(obj, event):
    obj['customers'] = CustomerContainer()

class CustomersContainerLocator(BaseLocator):
    splitedpath = ['customers']
grok.global_utility(CustomersContainerLocator, provides=interfaces.ICustomersContainerLocator)