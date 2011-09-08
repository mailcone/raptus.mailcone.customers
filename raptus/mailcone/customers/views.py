import grok

from megrok import navigation

from zope.component import getUtility

from raptus.mailcone.layout.views import Page
from raptus.mailcone.layout.interfaces import IOverviewMenu
from raptus.mailcone.layout.navigation import locatormenuitem

from raptus.mailcone.customers import _
from raptus.mailcone.customers import interfaces
from raptus.mailcone.customers import contents
from raptus.mailcone.layout.datatable import BaseDataTable

grok.templatedir('templates')



class CustomersTable(BaseDataTable):
    grok.context(interfaces.ICustomersContainer)


class Customers(Page):
    grok.name('index')
    grok.context(interfaces.ICustomersContainer)
    locatormenuitem(IOverviewMenu, interfaces.ICustomersContainerLocator, _(u'Customers'))
    
    @property
    def customerstable(self):
        return CustomersTable(self.context, self.request).html()
    

class AddCustomerForm(grok.AddForm):
    grok.context(interfaces.ICustomersContainer)
    grok.require('zope.Public')
    form_fields = grok.AutoFields(interfaces.ICustomer).omit('id')
    label = _('Add a customer')
    
    @grok.action(_('add_customer', default='add customer'))
    def add(self, **data):
        obj = contents.Customer(**data)
        self.context[obj.id] = obj


class EditCustomerForm(grok.EditForm):
    grok.context(interfaces.ICustomer)
    grok.require('zope.Public')
    form_fields = grok.AutoFields(interfaces.ICustomer).omit('id')
    label = _('Edit customer')
    
    @grok.action(_('save'))
    def save(self, **data):
        self.applyData(self.context, **data)


