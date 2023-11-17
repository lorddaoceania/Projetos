import gzip
 
def descompactar_arquivos_gz(arquivo_gz, arquivo_saida):
        with gzip.open(arquivo_gz, 'rb') as entrada:
            with open(arquivo_saida, 'wb') as saida:
                saida.write(entrada.read())
               
arquivo_comprimido = 'sensor_aplications_step_5.pkl.gz'
nome_saida = 'sensor_aplications_step_5_pkl'
 
descompactar_arquivos_gz(arquivo_comprimido, nome_saida)