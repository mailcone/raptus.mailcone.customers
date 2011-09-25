import os
import grok

from grokcore.view.interfaces import ITemplateFileFactory

from megrok import navigation

from zope.component import getUtility

from raptus.mailcone.layout.interfaces import IOverviewMenu
from raptus.mailcone.layout.navigation import locatormenuitem
from raptus.mailcone.layout.datatable import BaseDataTable
from raptus.mailcone.layout.views import Page, AddForm, EditForm, DeleteForm, DisplayForm

from raptus.mailcone.rules.interfaces import IRuleset

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
    grok.baseclass()
    form_fields = grok.AutoFields(interfaces.ICustomer).omit('id')


class RulesetsTable(BaseDataTable):
    grok.context(interfaces.ICustomer)
    interface_fields = IRuleset
    ignors_fields = ['id']
    inputs = (dict( title = _('Add Ruleset'),
                     cssclass = '',
                     type = 'checkbox',
                     prefix = 'addruleset',),)
    
    def _ajaxcontent(self, brains):
        return list()

class TabsCustomer(grok.View):
    grok.name('index')
    grok.template('customer')
    grok.context(interfaces.ICustomer)
    grok.require('zope.Public')

    def customerhtml(self):
        view = DisplayFormCustomer(self.context, self.request)
        return view()

    def rulesetshtml(self):
        filepath = os.path.join(os.path.dirname(__file__),'templates','rulesets.cpt')
        return getUtility(ITemplateFileFactory, name='cpt')(filename=filepath).render(self)

    @property
    def rulesetstable(self):
        return RulesetsTable(self.context, self.request).html()

    @property
    def tabs(self, ignors=[]):
        li = list()
        li.append(dict(id='ui-tabs-customer-informations',
                       title=_('Customer Informations'),
                       html=self.customerhtml()))
        li.append(dict(id='ui-tabs-rulesets',
                       title=_('Rulesets'),
                       html=self.rulesetshtml()))
        return [i for i in li if not  i.get('id') in ignors]



