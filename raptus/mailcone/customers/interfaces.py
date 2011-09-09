from zope import interface
from zope import interface, schema

from raptus.mailcone.core.interfaces import IContainer
from raptus.mailcone.core.interfaces import IContainerLocator


class ICustomersContainer(IContainer):
    """ A container for customers
    """


class ICustomersContainerLocator(IContainerLocator):
    """ interface for locate the customers folder.
    """


class ICustomer(interface.Interface):
    """ A customer
    """
    id = schema.TextLine(title=u'id', required=True)
    name = schema.TextLine(title=u'name', required=True)
    address = schema.Text(title=u'address', required=True)
    
