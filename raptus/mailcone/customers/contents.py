import grok

from zope import schema
from zope import component
from zope.annotation.interfaces import IAnnotations

from persistent.list import PersistentList
from persistent.dict import PersistentDict

from raptus.mailcone.core import bases
from raptus.mailcone.core.interfaces import IMailcone, ISearchable

from raptus.mailcone.rules.interfaces import IRulesetContainerLocator

from raptus.mailcone.customers import interfaces

RULESETS_ANNOTATIONS_KEY = 'raptus.mailcone.contents.rulesets'
RULESET_DATA_ANNOTATIONS_KEY = 'raptus.mailcone.contents.ruleset_data'


class Customer(bases.Container):
    grok.implements(interfaces.ICustomer)
    
    id = None
    name = None
    address = None

    @property
    def rulesets(self):
        storage = IAnnotations(self)
        return storage.setdefault(RULESETS_ANNOTATIONS_KEY, PersistentList())

    def get_rulesets(self):
        container = component.getUtility(IRulesetContainerLocator)()
        return [container.get_object(i) for i in self.rulesets if i in container]
        
    def set_rulesets(self, ids):
        storage = IAnnotations(self)
        storage[RULESETS_ANNOTATIONS_KEY] = PersistentList()
        self.rulesets.extend(ids)

    @property
    def ruleset_data(self):
        storage = IAnnotations(self)
        if not storage.has_key(RULESET_DATA_ANNOTATIONS_KEY):
            storage[RULESET_DATA_ANNOTATIONS_KEY] = PersistentDict()
        return storage[RULESET_DATA_ANNOTATIONS_KEY]

    def get_ruleset_data(self, id, use_default=True):
        # bug here !! data is parsend as string
        data = self.ruleset_data.get(id, dict())
        if not use_default:
            return data
        overrides = dict()
        rules = component.getUtility(IRulesetContainerLocator)().get_ruleitems()
        for rule in rules:
            if id is not rule.id:
                continue
            for k, v in rule.overrides.iteritems():
                if v:
                    overrides[k] = getattr(rule, k)
        overrides.update(data)
        return overrides

    def set_ruleset_data(self, id, data):
        self.ruleset_data.update({id:data})
        self._p_changed = 1


class CustomerContainer(bases.Container):
    grok.implements(interfaces.ICustomersContainer)

@grok.subscribe(IMailcone, grok.IApplicationInitializedEvent)
def init_customers_container(obj, event):
    obj['customers'] = CustomerContainer()

class CustomersContainerLocator(bases.BaseLocator):
    splitedpath = ['customers']
grok.global_utility(CustomersContainerLocator, provides=interfaces.ICustomersContainerLocator)



