import pandas as pd

pd.set_option('display.max_columns', None)

df_dados = pd.read_csv('sindromegripais_sus.csv',encoding='UTF-8', delimiter=';', on_bad_lines='skip', low_memory=False)

df_dados[['dataNotificacao', 'dataInicioSintomas', 'dataEncerramento',
          'dataPrimeiraDose', 'dataSegundaDose', 'dataColetaTeste1',
          'dataColetaTeste2', 'dataColetaTeste3', 'dataColetaTeste4']] = \
df_dados[['dataNotificacao', 'dataInicioSintomas', 'dataEncerramento',
          'dataPrimeiraDose', 'dataSegundaDose', 'dataColetaTeste1',
          'dataColetaTeste2', 'dataColetaTeste3', 'dataColetaTeste4']]\
.apply(lambda col: pd.to_datetime(col, format='%Y-%m-%d', errors='coerce')
       .fillna(pd.Timestamp('2000-01-01'))
       .astype('datetime64[ns]'))

df_dados[['idade', 'municipioIBGE', 'municipioNotificacaoIBGE', 'codigoEstrategiaCovid',	'codigoBuscaAtivaAssintomatico',	'outroBuscaAtivaAssintomatico',
         'codigoTriagemPopulacaoEspecifica',	'outroTriagemPopulacaoEspecifica',	'codigoLocalRealizacaoTestagem',
         'outroLocalRealizacaoTestagem',	'codigoRecebeuVacina', 'codigoContemComunidadeTradicional',
         'totalTestesRealizados', 'codigoEstadoTeste1',	'codigoTipoTeste1',
         'codigoFabricanteTeste1',	'codigoResultadoTeste1',	'codigoEstadoTeste2',
         'codigoTipoTeste2',	'codigoFabricanteTeste2',	'codigoResultadoTeste2',
         'codigoEstadoTeste3',	'codigoTipoTeste3',	'codigoFabricanteTeste3',
         'codigoResultadoTeste3',	'codigoEstadoTeste4',	'codigoTipoTeste4',
         'codigoFabricanteTeste4',	'codigoResultadoTeste4']] = \
df_dados[['idade', 'municipioIBGE', 'municipioNotificacaoIBGE', 'codigoEstrategiaCovid',	'codigoBuscaAtivaAssintomatico',	'outroBuscaAtivaAssintomatico',
         'codigoTriagemPopulacaoEspecifica',	'outroTriagemPopulacaoEspecifica',	'codigoLocalRealizacaoTestagem',
         'outroLocalRealizacaoTestagem',	'codigoRecebeuVacina', 'codigoContemComunidadeTradicional',
         'totalTestesRealizados', 'codigoEstadoTeste1',	'codigoTipoTeste1',
         'codigoFabricanteTeste1',	'codigoResultadoTeste1',	'codigoEstadoTeste2',
         'codigoTipoTeste2',	'codigoFabricanteTeste2',	'codigoResultadoTeste2',
         'codigoEstadoTeste3',	'codigoTipoTeste3',	'codigoFabricanteTeste3',
         'codigoResultadoTeste3',	'codigoEstadoTeste4',	'codigoTipoTeste4',
         'codigoFabricanteTeste4',	'codigoResultadoTeste4']]\
         .apply(pd.to_numeric, errors='coerce').fillna(0).astype(int)

df_dados[['sintomas', 'profissionalSaude', 'racaCor',
          'outrosSintomas', 'outrasCondicoes', 'profissionalSeguranca',
          'cbo', 'condicoes', 'sexo', 'estado', 'estadoIBGE',
          'municipio', 'estadoNotificacao',	'municipioNotificacao',
          'evolucaoCaso',	'classificacaoFinal', 'codigoLaboratorioPrimeiraDose',
          'codigoLaboratorioSegundaDose',	'lotePrimeiraDose',	'loteSegundaDose',
          'source_id', 'codigoDosesVacina', 'estadoNotificacaoIBGE']] = \
df_dados[['sintomas', 'profissionalSaude', 'racaCor',
          'outrosSintomas', 'outrasCondicoes', 'profissionalSeguranca',
          'cbo', 'condicoes', 'sexo', 'estado', 'estadoIBGE',
          'municipio', 'estadoNotificacao',	'municipioNotificacao',
          'evolucaoCaso',	'classificacaoFinal', 'codigoLaboratorioPrimeiraDose',
          'codigoLaboratorioSegundaDose',	'lotePrimeiraDose',	'loteSegundaDose',
          'source_id', 'codigoDosesVacina', 'estadoNotificacaoIBGE']]\
        .fillna('não informado').astype(str)

caminho_dados_saida = "opendatasus_tratado.csv"
df_dados.to_csv(caminho_dados_saida, index=True, index_label='id')

df_dados_tratados = pd.read_csv('opendatasus_tratado.csv',encoding='UTF-8', delimiter=',', on_bad_lines='skip')

caminho_dados_saida = "Dados_Tratados/dim_localidade.csv"
df_dim_localidade = ['estado', 'estadoIBGE', 'municipio', 'municipioIBGE', 'estadoNotificacao', 'municipioNotificacao', 'municipioNotificacaoIBGE']
dim_localidade = df_dados_tratados[df_dim_localidade]
dim_localidade.to_csv(caminho_dados_saida, index=True, index_label='id_localidade')

caminho_dados_saida = "Dados_Tratados/dim_paciente.csv"
df_dim_paciente = ['profissionalSaude', 'profissionalSeguranca', 'sexo', 'racaCor', 'idade']
dim_paciente = df_dados_tratados[df_dim_paciente]
dim_paciente.to_csv(caminho_dados_saida, index=True, index_label='id_paciente')

caminho_dados_saida = "Dados_Tratados/dim_sintomas.csv"
df_dim_sintomas = ['sintomas', 'outrosSintomas']
dim_sintomas = df_dados_tratados[df_dim_sintomas]
dim_sintomas.to_csv(caminho_dados_saida, index=True, index_label='id_sintoma')

caminho_dados_saida = "Dados_Tratados/dim_teste.csv"
df_dim_teste = ['codigoEstadoTeste1',	'codigoTipoTeste1',	'codigoFabricanteTeste1',
                'codigoResultadoTeste1', 'codigoEstadoTeste2',	'codigoTipoTeste2',
                'codigoFabricanteTeste2',	'codigoResultadoTeste2',	'codigoEstadoTeste3',
                'codigoTipoTeste3',	'codigoFabricanteTeste3',	'codigoResultadoTeste3',
                'codigoEstadoTeste4',	'codigoTipoTeste4', 'codigoFabricanteTeste4',
                'codigoResultadoTeste4',	'dataColetaTeste1',	'dataColetaTeste2',
                'dataColetaTeste3', 'dataColetaTeste4']
dim_teste = df_dados_tratados[df_dim_teste]
dim_teste.to_csv(caminho_dados_saida, index=True, index_label='id_teste')

caminho_dados_saida = "Dados_Tratados/dim_vacinacao.csv"
df_dim_vacinacao = ['codigoRecebeuVacina',	'codigoLaboratorioPrimeiraDose',	'codigoLaboratorioSegundaDose',
                    'lotePrimeiraDose',	'loteSegundaDose', 'dataPrimeiraDose',
                    'dataSegundaDose']
dim_vacinacao = df_dados_tratados[df_dim_vacinacao]
dim_vacinacao.to_csv(caminho_dados_saida, index=True, index_label='id_vacinacao')

df_localidade = pd.read_csv('Dados_Tratados/dim_localidade.csv',encoding='UTF-8', delimiter=',')
df_paciente = pd.read_csv('Dados_Tratados/dim_paciente.csv',encoding='UTF-8', delimiter=',')
df_sintomas = pd.read_csv('Dados_Tratados/dim_sintomas.csv',encoding='UTF-8', delimiter=',')
df_teste = pd.read_csv('Dados_Tratados/dim_teste.csv',encoding='UTF-8', delimiter=',')
df_vacinacao = pd.read_csv('Dados_Tratados/dim_vacinacao.csv',encoding='UTF-8', delimiter=',')

caminho_dados_saida = "Dados_Tratados/FatoCasos.csv"
df_fato_casos = ['sintomas', 'outrosSintomas', 'outrasCondicoes',
                 'condicoes', 'evolucaoCaso', 'classificacaoFinal',
                 'totalTestesRealizados', 'dataNotificacao', 'dataInicioSintomas',
                 'dataEncerramento', 'excluido', 'validado']
df_fato = df_dados_tratados[df_fato_casos]
df_fato['id_paciente'] = df_paciente['id_paciente']
df_fato.loc[:,'id_localidade'] = df_localidade['id_localidade']
df_fato.loc[:,'id_vacinacao'] = df_vacinacao['id_vacinacao']

nova_ordem = ['id_paciente', 'id_localidade', 'id_vacinacao'] + \
             [col for col in df_fato.columns if col not in ['id_paciente', 'id_localidade', 'id_vacinacao']]

df_fato = df_fato[nova_ordem]

df_fato.to_csv(caminho_dados_saida, index=True, index_label='id_caso')

df_caso = pd.read_csv('Dados_Tratados/FatoCasos.csv',encoding='UTF-8', delimiter=',')

caminho_dados_saida = "Dados_Tratados/FatoTestes.csv"

df_fato_teste = pd.DataFrame()
df_fato_teste ['id_caso'] = df_caso['id_caso']
df_fato_teste['id_teste'] = df_teste['id_teste']
df_fato_teste.to_csv(caminho_dados_saida, index=True, index_label='id_fatoTeste')