from proyectos.models.documento import Documento, Documento_metadato
from proyectos.models.proyecto import Proyecto_metadato



# from proyectos.models.funciones import tabla
# p = Proyecto.objects.get(id=4)

def tabla(proyecto,no_disponible='valor desconocido'):
   
    metas = []
    metas_id = []
    #metas_id = list(proyecto.metas_proyecto.all().order_by('id').values_list('id'))
    for m in proyecto.metas_proyecto.all().order_by('id'):
        vals = list(Documento_metadato.objects.filter(proyecto_metadato=m).distinct('valor').order_by('valor').values_list('valor',flat=True))
        metas.append([m, vals])
        metas_id.append(m.id)

    total_metas = len(metas_id)

    # metas contiene metadato object y lista de valores existentes para ese metadato (distintos):
    # [
    #    [<Proyecto_metadato: Corpus de las Sexualidades de México Lengua (obligatorio)>, ['Español', 'español', 'español1']],
    #    [<Proyecto_metadato: Corpus de las Sexualidades de México Tipo (obligatorio)>, ['Científico', 'Entrevista', 'Ficción', 'Foros', 'Foros ', 'Informativo', 'mx', 'tesina', 'tesina1']]
    #    ....
    # ]

    documentos = Documento.objects.filter(proyecto=proyecto)
    docs_y_metas = []
    for d in documentos:
        ms = list(d.documento_metadatos.all().order_by('proyecto_metadato__id').values_list('proyecto_metadato','valor'))
        if len(ms) != total_metas:
            #hay metas optativos que no existen para ese docmuento
            k = 0
            while k<total_metas:
                if k >= len(ms) or metas_id[k] != ms[k][0]:
                    # no existe el meta_id y es necesario agregarlo (aunque sea vacio)
                    nuevo_m = Proyecto_metadato.objects.get(id=metas_id[k])
                    ms.insert(k,(nuevo_m,no_disponible))
                k += 1
            # la lista de metas obligatorios y optativos está competa
        docs_y_metas.append([d,ms])

    # doc_y_metas contiene documento object y lista de metadatos (solo valores y en el mismo orden de metas por eso no se proporciona mas informacion)
    # [
    #    [
    #        <Documento: Corpus de las Sexualidades de México *Comportamiento_informativo_12.txt>, 
    #        [(22, 'Español'), (23, 'La sexualidad: un campo de estudio permanente'), (24, 'José Gerardo Velasco Castañón'), (25, '2007'), (27, 'Informativo'), (28, 'Medicina Universitaria'), (29, 'https://www.imbiomed.com.mx/articulo.php?id=5370'), (30, 'Comportamiento')]
    #    ]
    #    [
    #        <Documento: Corpus de las Sexualidades de México *Consulta_zoofilica.txt>, 
    #        [(22, 'Español'), (23, 'Consulta zoofilica'), (24, 'Fsamanes00'), (25, '2021'), (27, 'Foros'), (28, 'Sexo sin tabues '), (29, 'https://sexosintabues30.com/foros-sexo/zoofilia/consulta-zoofilica/'), (30, 'Parafilias ')]
    #    ]
    #    ....
    # ]

    return metas,docs_y_metas

