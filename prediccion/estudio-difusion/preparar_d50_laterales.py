"""Malla común independiente: fondo y dos laterales, paños de igual área."""
import preparar_localizado as mesh
mesh.O=mesh.B/'d50-laterales'
mesh.O.mkdir(exist_ok=True)
if __name__=='__main__':mesh.prepare(include_laterals=True)
