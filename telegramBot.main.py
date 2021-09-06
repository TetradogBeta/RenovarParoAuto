from TelegramHelper.Bot import Bot
from TelegramHelper.Client import Client
from User import User

from os.path import exists

def Main():
    dicDateAndUserArray={};
    dicAutenticacioUsers={};
    dicUsers={};
    dicTelegramUsers={};
    fileConfig="Config";

    if exists(fileConfig):
        fConfig = open(fileConfig, "r");
        config = fConfig.readlines();
        fConfig.close();
        token=config[0].replace("\n","");
    elif len(sys.argv)>1:
        token=sys.argv[1];
        fConfig = open(fileConfig, 'w');
        fConfig.writelines([token]);
        fConfig.close();
    
    bot=Bot(token,"Renovació Atur V1.0");
    bot.AddCommand("Alta", lambda cli,args:Alta(cli,dicUsers,dicAutenticacioUsers,dicTelegramUsers));
    bot.AddCommand("Actualitza", lambda cli,args:Actualitza(cli,dicUsers,dicAutenticacioUsers,dicTelegramUsers));

    bot.AddCommand("Eliminar",lambda cli,args:Elimina(cli,dicUsers,dicAutenticacioUsers,dicTelegramUsers));
    bot.AddCommand("Renovar", lambda cli,args:Renovar(cli,dicUsers,dicAutenticacioUsers,dicTelegramUsers));
    bot.Default.Default=lambda cli:cli.SendMessage("/Alta DNI/NIE pin\n/Actualitza pin\n/Eliminar (elimina el compte del sevidor)\n/Renovar (renova si hi ha un compte)");

    bot.Start();

def Actualitza(cli,dicUsers,dicAutenticacioUsers,dicTelegramUsers):
    if cli.Id in dicAutenticacioUsers:
        user=dicAutenticacioUsers[cli.Id];
        if not user.IsOk():
             user.Password=cli.Args[0];
             if not user.IsOk():
                cli.SendMessage("Imposible fer login, actualizta les dades per entrar primer!");
        elif user.Password!=cli.Args[0]:
            cli.SendMessage("Les dades actuals ja serveixen!");
        else:
            cli.SendMessage("El pin introduit ja estaba possat!");
    else:
        cli.SendMessage("Primer t'has de donar d'alta!!");

def Renovar(cli,dicUsers,dicAutenticacioUsers,dicTelegramUsers):
    if cli.Id in dicAutenticacioUsers:
        user=dicAutenticacioUsers[cli.Id];
        if not user.IsOk():
            cli.SendMessage("Imposible fer login, actualizta les dades per entrar primer!");
        else:
            user.Update();
            cli.SendMessage("Actualitzat correctament!\nPin: "+user.Password+"\nData renovació: "+str(user.DataRenovacio).split(" ")[0]);
    else:
        cli.SendMessage("Primer t'has de donar d'alta!!");


def Elimina(cli,dicUsers,dicAutenticacioUsers,dicTelegramUsers):
    if cli.Id in dicAutenticacioUsers:
        userName=dicAutenticacioUsers[cli.Id].User;
        dicTelegramUsers.pop(userName);
        dicUsers.pop(userName);
        dicAutenticacioUsers.pop(cli.Id);
        cli.SendMessage("S'ha eliminat el compte asociat al compte de Telegram correctament!")

    else:
        cli.SendMessage("No hi ha cap compte asociat al compte de Telegram!");

def Alta(cli,dicUsers,dicAutenticacioUsers,dicTelegramUsers):
    if len(cli.Args)>=2:
        userName=cli.Args[0];
        password=cli.Args[1];
        
        if userName not in dicUsers:

                if userName in dicTelegramUsers:
                    if dicTelegramUsers[userName] != cli.Id:
                        cliOri=Client(cli.Bot,dicTelegramUsers[userName]);#mirar de obtener el ID del chat...
                        cliOri.SendMessage("Algu te les teves dades d'accés, millor canvia el pin...");
                else:
                    if cli.Id not in dicAutenticacioUsers:
                        user=User(userName, password);
                        if user.IsOk():
                            dicUsers[userName]=user;
                            dicAutenticacioUsers[cli.Id]=user;
                            dicTelegramUsers[user.User]=cli.Id;
                            cli.SendMessage("Donat d'alta correctament!");
                        else:
                            cli.SendMessage("Error al fer login, el DNI/NIE o el pin son incorrectes!");
                        
                    elif dicAutenticacioUsers[cli.Id].User!=userName:
                            cli.SendMessage("Ja tens un altre compte...primer haurias d'eliminar el compte que hi ha asociat al teu compte de Telegram!");

            
        elif cli.Id in dicAutenticacioUsers and dicAutenticacioUsers[cli.Id].User == userName:
            cli.SendMessage("Ja estas donat d'alta, si vols fes /Actualitza pin");
        else:
            cli.SendMessage("Usuari d'un altre compte, si es teu millor canvia el PIN!");

    else:
        cli.SendMessage("Es requereix DNI/NIE y el pin separats per un espai!");
        



Main();