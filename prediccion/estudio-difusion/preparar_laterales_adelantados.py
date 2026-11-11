"""Sectores adelantados y bajos: malla propia, sin alterar ensayos anteriores."""
import preparar_localizado as mesh
mesh.O=mesh.B/'laterales-adelantados'
mesh.O.mkdir(exist_ok=True)
if __name__=='__main__':mesh.prepare(include_laterals=True,lateral_bounds=(19.,27.,4.2,6.6))
