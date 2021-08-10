import asyncio
import logging
from slixmpp import ClientXMPP

import nest_asyncio
nest_asyncio.apply()


class Cliente(ClientXMPP):
    def __init__(self, jid, password, isRegistered = False):


        ClientXMPP.__init__(self, jid, password)
        self.add_event_handler("session_start", self.session_start)
        self.add_event_handler("message", self.message)
        self.add_event_handler("register", self.register)
                # If you wanted more functionality, here's how to register plugins:
        self.register_plugin('xep_0030') # Service Discovery
        self.register_plugin('xep_0199') # XMPP Ping
        self.register_plugin('xep_0004') # Data forms
        self.register_plugin('xep_0066') # Out-of-band Data
        self.register_plugin('xep_0077') # In-band Registration
        if isRegistered:
            self['xep_0077'].force_registration = True
                # Here's how to access plugins once you've registered them:
                # self['xep_0030'].add_feature('echo_demo')

    def session_start(self, event):
        self.send_presence()
        self.get_roster()
            # Most get_*/set_* methods from plugins use Iq stanzas, which
            # are sent asynchronously. You can almost always provide a
            # callback that will be executed when the reply is received.
    def message(self, msg):
        if msg['type'] in ('chat', 'normal'):
            msg.reply("Thanks for sending\n%(body)s" % msg).send()

    async def register(self, iq):
        """
        Fill out and submit a registration form.
        The form may be composed of basic registration fields, a data form,
        an out-of-band link, or any combination thereof. Data forms and OOB
        links can be checked for as so:
        if iq.match('iq/register/form'):
            # do stuff with data form
            # iq['register']['form']['fields']
        if iq.match('iq/register/oob'):
            # do stuff with OOB URL
            # iq['register']['oob']['url']
        To get the list of basic registration fields, you can use:
            iq['register']['fields']
        """
        resp = self.Iq()
        resp['type'] = 'set'
        resp['register']['username'] = self.boundjid.user
        resp['register']['password'] = self.password

        try:
            await resp.send()
            logging.info("Account created for %s!" % self.boundjid)
        except IqError as e:
            logging.error("Could not register account: %s" %
                    e.iq['error']['text'])
            self.disconnect()
        except IqTimeout:
            logging.error("No response from server.")
            self.disconnect()


if __name__ == '__main__':
    # Ideally use optparse or argparse to get JID, # password, and log level.
    #logging.basicConfig(level=logging.DEBUG,
    #                    format='%(levelname)-8s %(message)s')
    dele = True
    opcion1 = 0
    #port = 5222

    while dele:
        try:
            #displays main menu and ask user what option they want
            print("--------------------\nBienvenido a el chat de Kristen\n\n\tYa tiene un usuario? (1)\n\tDesea crear un usario nuevo? (2)\n\tSalir (3)")

            opcion_general = int(input())
            if opcion_general == 1:
                #existing username
                opcion1 = 1
                dele = False
            elif opcion_general == 2:
                #new username
                opcion1 = 2
                dele = False
            elif opcion_general == 3:
                #get out out the chat
                opcion1 = 3
                dele = False
            else:
                #defensive programing
                print("Porfavor ingrese una opcion valida (1,2,3)\n")
        except:
            # defensive programing
            print("Porfavor ingrese una opcion valida (1,2,3)\n")


            #
    # existing user
    if opcion1 == 1:
        username = input("Porfavor ingrese su usuario: ")
        password = input("Porfavor ingrese su contraseña: ")

        #verification for existing username
        #true es cuando estoy registrado un usuario
        xmpp = Cliente(username, password, False)
        xmpp.connect()
        xmpp.process(forever = False)


    #new user
    elif opcion1 == 2:
        username_new = input("Porfavor ingrese el usuario que desea: ")
        password_new = input("Porfavor ingrese la contraseña que desea: ")
        #true es cuando estoy registrado un usuario
        #if the username doesn't exist creates it
        #if the username exists error message

        xmpp = Cliente(username_new, password_new, True)
        xmpp.connect()
        xmpp.process(forever = False)

    #get out of chat
    else:
        print("\nGracias por utilizar el chat de Kristen\nSaliendo ...\n--------------------")






    xmpp.disconect()
