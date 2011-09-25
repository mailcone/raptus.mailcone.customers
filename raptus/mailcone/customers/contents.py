import grok

from zope import schema
from zope import component

from persistent.list import PersistentList

from raptus.mailcone.core import bases
from raptus.mailcone.core.interfaces import IMailcone, ISearchable

from raptus.mailcone.rules.interfaces import IRulesetContainerLocator

from raptus.mailcone.customers import interfaces



class Customer(bases.Container):
    grok.implements(interfaces.ICustomer)
    
    id = None
    name = None
    address = None
    
    rulesets = PersistentList()
    
    def get_rulesets(self):
        container = component.getUtility(IRulesetContainerLocator)()
        return [container.get_object(i) for i in self.rulesets if i in container]
        
    def set_rulesets(self, ids):
        self.rulesets = PersistentList(ids)



class CustomerContainer(bases.Container):
    grok.implements(interfaces.ICustomersContainer)

@grok.subscribe(IMailcone, grok.IApplicationInitializedEvent)
def init_customers_container(obj, event):
    obj['customers'] = CustomerContainer()

class CustomersContainerLocator(bases.BaseLocator):
    splitedpath = ['customers']
grok.global_utility(CustomersContainerLocator, provides=interfaces.ICustomersContainerLocator)