import grok

from megrok import navigation

from zope.component import getUtility

from raptus.mailcone.layout.interfaces import IOverviewMenu
from raptus.mailcone.layout.navigation import locatormenuitem
from raptus.mailcone.layout.datatable import BaseDataTable
from raptus.mailcone.layout.views import Page, AddForm, EditForm, DeleteForm, DisplayForm

from raptus.mailcone.customers import _
from raptus.mailcone.customers import interfaces
from raptus.mailcone.customers import contents

grok.templatedir('templates')



class CustomersTable(BaseDataTable):
    grok.context(interfaces.ICustomersContainer)
    interface_fields = interfaces.ICustomer
    ignors_fields = ['id']
    actions = (dict( title = _('delete'),
                     cssclass = 'ui-icon ui-icon-trash ui-modal-minsize ui-datatable-ajaxlink',
                     link = 'deletecustomerform'),
               dict( title = _('edit'),
                     cssclass = 'ui-icon ui-icon-pencil ui-datatable-ajaxlink',
                     link = 'editcustomerform'),)

class Customers(Page):
    grok.name('index')
    grok.context(interfaces.ICustomersContainer)
    locatormenuitem(IOverviewMenu, interfaces.ICustomersContainerLocator, _(u'Customers'))
    
    @property
    def customerstable(self):
        return CustomersTable(self.context, self.request).html()
    
    @property
    def addurl(self):
        return '%s/addcustomerform' % grok.url(self.request, self.context)
    

class AddCustomerForm(AddForm):
    grok.context(interfaces.ICustomersContainer)
    grok.require('zope.Public')
    form_fields = grok.AutoFields(interfaces.ICustomer).omit('id')
    label = _('Add a new customer')

    def create(self, **data):
        return contents.Customer()


class EditCustomerForm(EditForm):
    grok.context(interfaces.ICustomer)
    grok.require('zope.Public')
    form_fields = grok.AutoFields(interfaces.ICustomer).omit('id')
    label = _('Edit customer')


class DeleteCustomerForm(DeleteForm):
    grok.context(interfaces.ICustomer)
    grok.require('zope.Public')
    
    def item_title(self):
        return self.context.name
    
    
class DisplayFormCustomer(DisplayForm):
    grok.name('index')
    grok.context(interfaces.ICustomer)
    grok.require('zope.Public')






