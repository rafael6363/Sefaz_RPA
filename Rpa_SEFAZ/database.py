import oracledb
import pandas

usernameBd = 'rpa' 
passwordBd= 'Rpa!2023'
#dsn = 'oracle.bomfuturo.local:1521/protheus'
dsn = 'oracledbdev.bomfuturo.local:1521/protheus'
connectionBd = oracledb.connect(user=usernameBd, password=passwordBd, dsn=dsn)
cursor = connectionBd.cursor()

def retornoCnpj():
    cursor.execute("""
            SELECT M0_CODIGO, M0_FILIAL, M0_CGC  from PROTHEUS11.sigaemp 
            WHERE LENGTH(trim(M0_CGC)) >= 12 
            --AND m0_insc not in ('ISENTO',' ')OR m0_insc = NULL
            """)
    # Usar fetchall() para pegar todas as linhas
    Resutadocnpj = cursor.fetchall()
    #print(type(Resutadocnpj))
    #for filial in Resutadocnpj:
    #    print(filial)
    
    #df = pandas.DataFrame(Resutadocnpj)
    #df.to_csv(fr'sequencianotas\cnpjFiliais\resultado.csv', index=False, header=False)
    
    return Resutadocnpj

if __name__ == "__main__":
    retornoCnpj()