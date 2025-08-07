Criação do RPA:
Será criado um RPA utilizando a linguagem Python;
O RPA fará os seguintes passos:
1. Acessar o site https://www.sefaz.mt.gov.br/acesso/;
2. Realizar o login como contabilista;
3. No menu esquerdo acessar o caminho: "Consulta NFe" > "Consultas"> "Consulta de NF-e
Emitida/Recebida";
4. Nas informações do contribuinte, a consulta deve ser feita por 'Destinatário'. o Tipo de Documento, a UF
do destinatário, bem como o CNPJ/CPF, devem ser consultados de acordo com a tabela SIGAEMP;
5. No período, a Data Inicial e a Data Final devem ser o primeiro e o último dia do mês anterior,
respectivamente;
6. Clicar em "Consultar", logo após a geração da Consulta, clicar em "Exportar para Excel".
7. Alterar o nome do arquivo para o seguinte padrão: NFe + Grupo + Filial + Mês + Ano;
8. Alterar a extensão de .XLS para .CSV;
9. Os arquivos devem ser salvos na subpasta separados por Grupo de Empresas, que será criado pelo RPA
todo mês cujo nome seguirá o padrão: Número do Mês - Mês, na pasta "Consulta de NF-e
Emitida/Recebida" dentro do diretório SPED Fiscal.
O RPA também deve exportar também as relações dos CT-e seguindo os passos:
1. No menu esquerdo: "Conhecimento de Transporte Eletrônico (CTe)" > "Consulta CT-e
Emitidos/Recebidos":
2. Em Tipo de Consulta, Selecionar: "Tomador";
3. Preencher a "Identificação do Tomador" de acordo com o item 4 do primeiro item;
4. No período, a Data Inicial e a Data Final devem ser o primeiro e o último dia do mês anterior,
respectivamente;
5. Clicar em "Consultar", logo após a geração da Consulta, clicar em "Mostrar Planilha";
6. Alterar o nome do arquivo para o seguinte padrão: CTe + Grupo + Filial + Mês + Ano;
7. Alterar a extensão de .XLS para .CSV;
8. Os arquivos devem ser salvos na subpasta separados por Grupo de Empresas, que será criado pelo RPA
todo mês cujo nome seguirá o padrão: Número do Mês - Mês, na pasta "Consulta de СТ-е
Emitida/Recebida" dentro do diretório SPED Fiscal.
Caso a filial tenha Inscrição Estadual também seguir esses passos:
1. No menu esquerdo acessar o caminho: "Sistema Conta Corrente Fiscal 3.0" > "Lançamento" > "Consultar
Lançamento";
2. Preencher o campo "Número do Documento" de acordo com a tabela SIGAEMP inserindo a Inscrição
3.
Estadual da filial consultada:
Nos campos "Período de Referência Inicial" e "Período de Referência Final" colocar o mês anterior ao
corrente e Pesquisar;
4. Após a pesquisa carregar, salvar a página como PDF, com o layout em Paisagem;
Salvar o arquivo no diretório SPED do Fiscal sob o nome especificado no próximo ponto deste



https://github.com/rafael6363/RPA_Sefaz.git
