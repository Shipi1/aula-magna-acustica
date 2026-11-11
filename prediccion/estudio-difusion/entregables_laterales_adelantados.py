"""Vista y OBJ del segundo conjunto de paños, sin repetir la auditoría anterior."""
from pathlib import Path
B=Path(__file__).resolve().parent
source=(B/'entregables_d50_laterales.py').read_text(encoding='utf8')
source=source.replace("O=B/'d50-laterales'","O=B/'laterales-adelantados'").replace("keys=('R','Lneg','Lpos')","keys=('Lneg','Lpos')").replace('plt.subplots(1,3,figsize=(15,5)','plt.subplots(1,2,figsize=(13,5)').replace("'Lneg':'Lateral Y negativo','Lpos':'Lateral Y positivo'","'Lneg':'Lateral adelantado Y negativo','Lpos':'Lateral adelantado Y positivo'")
source=source.split('# Record candidate paths;')[0]
exec(compile(source,'entregables-adelantados','exec'),{'__file__':str(B/'entregables_d50_laterales.py')})
print('Vistas y OBJ de laterales adelantados generados.')
