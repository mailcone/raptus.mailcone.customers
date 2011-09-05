import grok

from megrok import navigation

from raptus.mailcone.layout.views import Page
from raptus.mailcone.layout.interfaces import IOverviewMenu

from raptus.mailcone.customers import interfaces
from raptus.mailcone.customers import _

grok.templatedir('templates')

class Customers(Page):
    grok.name('index')
    grok.context(interfaces.ICustomersContainer)
    navigation.menuitem(IOverviewMenu, _(u'Customers'))
    
