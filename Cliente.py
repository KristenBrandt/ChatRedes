import asyncio
import logging
from slixmpp import ClientXMPP

import nest_asyncio
nest_asyncio.apply()


class Cliente(ClientXMPP):
    def __init__(self, jid, password, nickname, isRegistered = False):


        ClientXMPP.__init__(self, jid, password)
        self.nick = nickname
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
        sub_menu = True
        print("He entrado al chat exitosamente :)")
        self.send_presence()
        self.get_roster()

        sub_menuu()
        opcion = int(input("Porfavor ingrese la opcion deseada: "))
        while sub_menu:
            if opcion == 1:
                pass

            elif opcion == 2:
                pass
                print("op2")
            elif opcion == 3:
                print(print("\nGracias por utilizar el chat de Kristen\nSaliendo ...\n--------------------"))
                self.logout()

                sub_menu = False
            elif opcion == 4:
                self.delete_account()



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
            print("Cuenta creada")
            logging.info("Account created for %s!" % self.boundjid)
        except IqError as e:
            print("Error al crear cuenta")
            logging.error("Could not register account: %s" %
                    e.iq['error']['text'])
            self.disconnect()
        except IqTimeout:
            logging.error("No response from server.")
            self.disconnect()

    def logout(self):
        self.authenticated = False
        self.disconnect()

    def cerrar(self):
        self.running = False

    async def uno_a_uno(self, to):
        men = input('Type direct message > ')
        self.send_message(mto = to, mbody = msg, mtype = 'chat', mnick = self.nick)






async def proceso(xmpp):
    xmpp.process(forever = False)

async def conectar1(xmpp):
    xmpp.connect()


def sub_menuu():
    print("-"*20)
    print("\n1. Chat normal")
    print("\n2. Chat grupal")
    print("\n3. Salir")
    print("\n4. Eliminar cuenta\n")



async def main():
    # Ideally use optparse or argparse to get JID, # password, and log level.
    #logging.basicConfig(level=logging.DEBUG,
    #                    format='%(levelname)-8s %(message)s')
    dele = True
    sub_menu = True

    print("--------------------\nBienvenido a el chat de Kristen\n")
    # existing user
    existente = int(input("Es un usuario ya existente si = 1, no = 2: "))
    username = input("Porfavor ingrese su usuario: (alfinal del username agregue @Dominio) ")
    password = input("Porfavor ingrese su contraseña: ")

    if existente == 1:
        dele = False

    if existente == 2:
        dele  = True
    #true es cuando estoy registrado un usuario

    xmpp = Cliente(username, password, dele)
    conectar = asyncio.create_task(conectar1(xmpp))
    await asyncio.wait({conectar}, return_when=asyncio.ALL_COMPLETED)

    processTask = asyncio.create_task(proceso(xmpp))










asyncio.run(main())
