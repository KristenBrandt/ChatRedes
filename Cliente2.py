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
        self.add_event_handler("groupchat_message", self.muc_message)
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

    async def session_start(self, event):
        print("He entrado al chat exitosamente :)")
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
            print("Cuenta creada")
            logging.info("Account created for %s!" % self.boundjid)
        except IqError as e:
            print("Error al crear cuenta")
            logging.error("Could not register account: %s" %
                    e.iq['error']['text'])
            self.disconnect()
        except IqTimeout:
            print("Error al crear cuenta")
            logging.error("No response from server.")
            self.disconnect()

    def join_room(self, room, nicknam):
        try:
            self.plugin['xep_0045'].join_muc(room,
                                            nicknam,
                                         # If a room password is needed, use:
                                         # password=the_room_password,
                                             )
            print("Se ha ingresado a :" , room)
        except:
            print("No se pudo ingresar a el chat room")

    def muc_message(self, msg, room):
        """
        Process incoming message stanzas from any chat room. Be aware
        that if you also have any handlers for the 'message' event,
        message stanzas may be processed by both handlers, so check
        the 'type' attribute when using a 'message' event handler.

        Whenever the bot's nickname is mentioned, respond to
        the message.

        IMPORTANT: Always check that a message is not from yourself,
                   otherwise you will create an infinite loop responding
                   to your own messages.

        This handler will reply to messages that mention
        the bot's nickname.

        Arguments:
            msg -- The received message stanza. See the documentation
                   for stanza objects and the Message stanza to see
                   how it may be used.
        """
        if msg['mucnick'] != self.nick and self.nick in msg['body']:
            self.send_message(mto=msg['from'].bare,
                              mbody="I heard that, %s." % msg['mucnick'],
                              mtype='groupchat')

    def muc_online(self, presence):
        """
        Process a presence stanza from a chat room. In this case,
        presences from users that have just come online are
        handled by sending a welcome message that includes
        the user's nickname and role in the room.

        Arguments:
            presence -- The received presence stanza. See the
                        documentation for the Presence stanza
                        to see how else it may be used.
        """
        if presence['muc']['nick'] != self.nick:
            self.send_message(mto=presence['from'].bare,
                              mbody="Hello, %s %s" % (presence['muc']['role'],
                                                      presence['muc']['nick']),
                              mtype='groupchat')

    def logout(self):
        #print(self.authenticated)
        #self.authenticated = False
        self.disconnect()

    def cerrar(self):
        self.running = False

    def mensaje_directo(self, to):
        try:
            mensaje = input("Porfavor ingrese el mensaje: ")
            self.send_message(mto = to, mbody = mensaje, mtype = 'chat')
            print("Mensaje enviado a " +to+ " exitosamente")
        except:
            print("No se pudo enviar el mensaje privado.")

    def xmpp_message(self, con, event):
        type = event.getType()
        fromjid = event.getFrom().getStripped()
        if type in ['message', 'chat', None] and fromjid == self.remotejid:
            sys.stdout.write(event.getBody() + '\n')


def menu_principal():
    dele = True
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

    return(username, password,  dele)


def menu_secundario():
    print("-"*20)
    print("\n1. Chat normal")
    print("\n2. Chat grupal")
    print("\n3. Salir")
    print("\n4. Eliminar cuenta\n")
    opcion = int(input("Porfavor ingrese la opcion deseada: "))

    return opcion

def menu_mensaje():
    recepient = input("Porfavor ingrese el usuario al que le quiere mandar el mensaje: ")

    return recepient



async def orden():
    try:
        username, password, dele=menu_principal()
        xmpp = Cliente(username, password, dele)
        xmpp.connect()
        await asyncio.sleep(15)
        xmpp.loop.create_task(main(xmpp))
        xmpp.process(forever = False)
    except  Exception as error:
        print("Un error:  ", error)
    finally:
        xmpp.disconnect()
        print("Usuario desconectado")



async def main(xmpp):
    doit = True
    while doit:
        opcion = menu_secundario()
        if opcion == 1:
            recepient = menu_mensaje()
            xmpp.mensaje_directo(recepient)
            xmpp.message(recepient)

            pass

        elif opcion == 2:
            room = input("Cual es el nombre del chatroom: ")
            nicknam= input("Cual quiere que sea su nickname: ")
            xmpp.join_room(room, nicknam)

            pass
        elif opcion == 3:
            print("\nGracias por utilizar el chat de Kristen\n")
            print("Saliendo ...")
            xmpp.logout()
            doit = False


        elif opcion == 4:
            xmpp.delete_account()
            xmpp.cerrar()
            doit = False



asyncio.run(orden())
