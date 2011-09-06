from zope import interface

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