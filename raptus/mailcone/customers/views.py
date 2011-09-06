import grok

from megrok import navigation

from raptus.mailcone.layout.views import Page
from raptus.mailcone.layout.interfaces import IOverviewMenu
from raptus.mailcone.layout.navigation import locatormenuitem

from raptus.mailcone.customers import _
from raptus.mailcone.customers import interfaces



grok.templatedir('templates')


class Customers(Page):
    grok.name('index')
    grok.context(interfaces.ICustomersContainer)
    locatormenuitem(IOverviewMenu, interfaces.ICustomersContainerLocator, _(u'Customers'))
    
