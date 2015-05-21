import colander
import deform.widget
import random

from pyramid.decorator import reify
from pyramid.httpexceptions import HTTPFound
from pyramid.renderers import get_renderer
from pyramid.security import remember, forget, authenticated_userid
from pyramid.view import view_config, forbidden_view_config

from .models import DBSession, Ticket

#Schema to use for tickets
class TicketSchema(colander.MappingSchema):
    email = colander.SchemaNode(colander.String())
    amount = colander.SchemaNode(
        colander.Integer(), validator=colander.Range(0, 20))

#define all views belonging to to lottery
class LotteryViews(object):
    def __init__(self, request):
        self.request = request
        renderer = get_renderer("templates/layout.pt")
        self.layout = renderer.implementation().macros['layout']
        self.logged_in = authenticated_userid(request)

    @reify
    def registration_form(self):
        schema = TicketSchema()
        return deform.Form(schema, buttons=('confirm',))

    @reify
    def reqts(self):
        return self.registration_form.get_widget_resources()

    @view_config(route_name='registration',
                 renderer='templates/registration.pt')
    def registration(self):
        if 'confirm' in self.request.params:
            controls = self.request.POST.items()
            try:
                #try to validate the form
                appstruct = self.registration_form.validate(controls)
            except deform.ValidationFailure as e:
                # Form is NOT valid
                return dict(title='Lottery Ticket Registration', form=e.render())

            # Add all the tickets to the database
            email = appstruct['email']
            for x in range(0, appstruct['amount']):
                DBSession.add(Ticket(email))

            url = self.request.route_url('confirmation', email=email)
            return HTTPFound(url)

        return dict(title='Lottery Ticket Registration', form=self.registration_form.render())

    @view_config(route_name='confirmation',
                 renderer='templates/confirmation.pt')
    def confirmation(self):
        email = self.request.matchdict['email']
        #select all tickets for this email
        tickets = DBSession.query(Ticket).filter_by(email=email)
        return dict(title="Confirmation of registration", email=email, tickets=tickets)

    @view_config(route_name='winningticket',
                 renderer='templates/winningticket.pt')
    def winningticket(self):
        #pick random ticket out of database as winner
        total = DBSession.query(Ticket).count()
        rand = random.randrange(0, total)
        ticket = DBSession.query(Ticket)[rand]
        return dict(title="The winner is", email=ticket.email, ticket=ticket.uid)

