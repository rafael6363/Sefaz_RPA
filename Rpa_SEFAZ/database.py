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
    Resutadocnpj = cursor.fetchall()
    return Resutadocnpj

def retornoInscEstd():
    cursor.execute("""
            SELECT m0_insc, M0_FILIAL from PROTHEUS11.sigaemp 
            WHERE LENGTH(trim(M0_CGC)) >= 12 AND 
            m0_insc not in ('ISENTO',' ') OR m0_insc = null 
            """)
    ResutadoInscEstd= cursor.fetchall()
    return ResutadoInscEstd


if __name__ == "__main__":
    retornoCnpj()
    retornoInscEstd()