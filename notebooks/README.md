# Como Configurar o Ambiente (Google Colab)

Este projeto utiliza uma integração entre **Google Colab**, **Google Drive** e **GitHub via SSH** para garantir que seu trabalho seja salvo automaticamente e com segurança diretamente na sua nuvem.

## ⚠️ Regra de Ouro: O Ciclo de Execução
Como o ambiente do Google Colab é temporário (volátil), você **deve** realizar este setup toda vez que iniciar uma nova sessão de trabalho:
1. Abra o arquivo `config.ipynb` (sua cópia pessoal do template).
2. Execute todas as células para montar o Drive e carregar suas credenciais SSH na memória da instância.

---

## Passo 1: Configuração Única da Chave SSH 

1. **Gere a chave** no seu computador: `ssh-keygen -t rsa -b 4096 -f NOME_DA_SUA_CHAVE`.
2. **Cadastre no GitHub**: Adicione o conteúdo da chave pública (`.pub`) ao seu perfil em *Settings > SSH and GPG keys*.
3. **Salve no Drive**: Na raiz do seu **Meu Drive**, crie uma pasta chamada `.ssh` e faça o upload da sua **chave privada** (o arquivo sem extensão).
   * *Atenção: Nunca coloque sua chave privada dentro da pasta do repositório.*

---

## Passo 2: Configuração do Projeto no Colab

1. Abra o arquivo `config_template.ipynb` no Google Colab.
2. Salve uma cópia como `config.ipynb` (este nome está no `.gitignore` para sua segurança).
3. Altere a variável `NOME_DA_CHAVE_PRIVADA_NO_DRIVE` com o nome exato do arquivo que você subiu ao Drive.
4. Execute todas as células. Se o repositório não existir no seu Drive, o script fará o `git clone` automaticamente.

---

## Passo 3: Gerenciamento via Terminal

Após executar o `config.ipynb`, você não precisa de células Python para usar o Git. Use o **Terminal Nativo** do Colab:

1. Clique no ícone de **Terminal** (`>_`) no canto inferior da barra lateral esquerda.
2. **Navegação Automática**: O terminal abrirá diretamente na pasta do repositório (`/content/drive/MyDrive/UAVs_forest_fires_STE`).
3. **SSH Integrado**: O agente SSH é carregado automaticamente. Você pode rodar `git pull` ou `git push` sem digitar senhas.


### 💡 Dicas de Terminal
* **Recarregar Configurações**: Se o terminal não iniciar na pasta correta ou o SSH falhar, digite o comando:
  ```bash
  source ~/.bashrc
