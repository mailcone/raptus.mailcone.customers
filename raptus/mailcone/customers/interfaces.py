from zope import interface


#class ICustomersContainer(interfaces.IContainer):
class ICustomersContainer(interface.Interface):
    """ A container for customers
    """


class ICustomersContainerHolder(interface.Interface):
    """ Marker interface for objects adaptable to ICustomersContainer
    """


class ICustomer(interface.Interface):
    """ A customer
    """