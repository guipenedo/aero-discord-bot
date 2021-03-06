# Aero Discord Bot
Um bot de discord para interagir com a plataforma [FénixEdu](https://fenixedu.org/). Desenvolvido originalmente para o servidor de discord do curso de [Engenharia Aeroespacial](https://fenix.tecnico.ulisboa.pt/cursos/meaer) no [Instituto Superior Técnico](https://tecnico.ulisboa.pt/).
O bot, após autenticação dos utilizadores com uma conta do fénix, cria e adiciona automaticamente os utilizadores a channels específicos para cada cadeira em que estão inscritos. Existem channels dedicados à postagem automática de anúncios da página de cada cadeira através dos seus feeds de rss, e channels para discussão entre os alunos inscritos em cada cadeira.

## Criação e adição do bot de discord
Para utilizar a app é necessário criar um bot de discord e adicioná-lo ao servidor onde se pretende que este corra. Instruções [aqui]().

## Configuração
A configuração da aplicação é realizada através de environment variables. Estas podem estar definidas num ficheiro *.env* ou diretamente no ambiente. O ficheiro *.env.default* é um modelo que pode ser copiado para *.env* e as configurações alteradas, para quem quiser seguir esta opção.

Uma descrição detalhada das várias opções e dos seus valores pode ser encontrada [aqui](https://github.com/guipenedo/aero-discord-bot/wiki/Configura%C3%A7%C3%A3o).