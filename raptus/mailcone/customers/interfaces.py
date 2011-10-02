from zope import interface
from zope import interface, schema

from raptus.mailcone.core.interfaces import IContainer
from raptus.mailcone.core.interfaces import IContainerLocator

from raptus.mailcone.customers import _

class ICustomersContainer(IContainer):
    """ A container for customers
    """


class ICustomersContainerLocator(IContainerLocator):
    """ interface for locate the customers folder.
    """


class ICustomer(interface.Interface):
    """ A customer
    """
    id = schema.TextLine(title=_(u'Id'), required=True)
    name = schema.TextLine(title=_(u'Name'), required=True)
    address = schema.Text(title=_(u'Address'), required=True)
    
    def get_rulesets(self):
        """ get rulesets objects
        """
    
    def set_rulesets(self, ids):
        """ set customer in relation with any rulesets
        """


    def get_ruleset_data(self, id):
        """ get data for a ruleitem
        """
        
    def set_ruleset_data(self, id, data):
        """ store data to specified ruleitem
        """