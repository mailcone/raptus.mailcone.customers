import os
import grok
import json
import copy

from grokcore.view.interfaces import ITemplateFileFactory

from megrok import navigation

from zope.component import getUtility
from zope.formlib import form

from raptus.mailcone.layout.interfaces import IOverviewMenu
from raptus.mailcone.layout.navigation import locatormenuitem
from raptus.mailcone.layout.datatable import BaseDataTable
from raptus.mailcone.layout.views import Page, AddForm, EditForm, DeleteForm, DisplayForm

from raptus.mailcone.core import utils

from raptus.mailcone.rules.interfaces import IRuleset, IRuleItem
from raptus.mailcone.rules.wireit import IdentifierMixing

from raptus.mailcone.customers import _
from raptus.mailcone.customers import interfaces
from raptus.mailcone.customers import contents

grok.templatedir('templates')

ADD_RULESET_PREFIX = 'addruleset'





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



class OverrideFormRuleItem(EditForm, IdentifierMixing):
    grok.context(IRuleItem)
    
    actions = list()
    
    
    def __call__(self):
        data = self.request.form.get('metadata', None)
        if data:
            jsondata = json.loads(data)
            self.request = copy.copy(self.request)
            self.request.form = jsondata
            self.process(jsondata)
        return super(OverrideFormRuleItem, self).__call__()
    
    def __init__(self, context, request, customer):
        super(OverrideFormRuleItem, self).__init__(context, request)
        self.customer = customer
    
    def process(self, data):
        self.update_form()
        results = dict()
        form.getWidgetsData(self.widgets, self.prefix, results)
        self.customer.set_ruleset_data(utils.parent(self.context).id, results)
    
    def setUpWidgets(self, ignore_request=False):
        self.adapters = {}
        data = self.customer.get_ruleset_data(utils.parent(self.context).id)
        self.widgets = form.setUpWidgets(
            self.form_fields, self.prefix, self.context, self.request,
            form=self, adapters=self.adapters, ignore_request=ignore_request, data=data)
    
    @property
    def form_fields(self):
        factory = self.identifer(self.context.identifer, utils.parent(self.context))
        ids = [k for k,v in self.context.overrides.iteritems() if v]
        return factory.form_fields.select(*ids)

    @property
    def prefix(self):
        return 'form_%s' % self.context.id

class OverrideFormRuleset(grok.View):
    grok.context(IRuleset)
    
    def __init__(self, context, request, customer):
        super(OverrideFormRuleset, self).__init__(context, request)
        self.customer = customer
    
    @property
    def ruleitems(self):
        li = list()
        for item in self.context.objects():
            if not [k for k,v in item.overrides.iteritems() if v]:
                continue
            html = OverrideFormRuleItem(item, self.request, self.customer)()
            di = dict(description = item.description,
                      title = item.title,
                      html = html)
            li.append(di)
        return li



class RulesetsTable(BaseDataTable):
    grok.context(interfaces.ICustomer)
    interface_fields = IRuleset
    ignors_fields = ['id']
    inputs = (dict(  title = _('Active'),
                     cssclass = '',
                     type = 'checkbox',
                     prefix = ADD_RULESET_PREFIX,
                     id = 'addruleset'),)
    
    def _ajaxcontent(self, brains):
        return list()

    def inputbuilder_value(self, input, brain):
        if input.get('id') == 'addruleset':
            return brain.id in [i.id for i in self.context.get_rulesets()]



class TabsCustomer(grok.View):
    grok.name('index')
    grok.template('customer')
    grok.context(interfaces.ICustomer)
    grok.require('zope.Public')

    def __call__(self):
        data = self.request.form.get('metadata', None)
        if data:
            jsondata = json.loads(data)
            self.process(jsondata)
        return super(TabsCustomer, self).__call__()

    def process(self, data):
        rulesets = dict([(i.id,True) for i in self.context.get_rulesets()])
        for name, value in data.iteritems():
            if name.startswith('%s.'%ADD_RULESET_PREFIX):
                name = name[len('%s.'%ADD_RULESET_PREFIX):]
                rulesets[name] = value
        self.context.set_rulesets([k for k, v in rulesets.iteritems() if v])
        
    def customerhtml(self):
        view = DisplayFormCustomer(self.context, self.request)
        return view()

    def rulesetshtml(self):
        filepath = os.path.join(os.path.dirname(__file__),'templates','rulesets.cpt')
        return getUtility(ITemplateFileFactory, name='cpt')(filename=filepath).render(self)

    def overridehtml(self, ruleset):
        view = OverrideFormRuleset(ruleset, self.request, self.context)
        return view()

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
        for ruleset in self.context.get_rulesets():
            li.append(dict(id='ui-tabs-override-%s'%ruleset.id,
                           title=ruleset.name,
                           html=self.overridehtml(ruleset)))
        return [i for i in li if not  i.get('id') in ignors]



