import sqlite3

conn = sqlite3.connect('comunidade.db')
cursor = conn.cursor()

id_cliente = 8

# excluindo um registro da tabela
cursor.execute("""
DELETE FROM Foto
WHERE id = ?
""", (id_cliente,))

conn.commit()

print('Registro excluido com sucesso.')

conn.close()