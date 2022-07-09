import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from pyensembl import EnsemblRelease


data = EnsemblRelease(77)


@csrf_exempt
def hello(request):
    r = HttpResponse(json.dumps("hello world"), content_type="application/json")
    r['Access-Control-Allow-Origin'] = '*'
    return r

#+17:7676012..7676031
@csrf_exempt
def get_id(request):
    cor = request.GET.get(r'coordinates')
    if cor.startswith ('+') or cor.startswith ('-'):
        print ( 'strand is defined')
    else:
        cor = '+'+cor
        print ( 'strand was not defined so we are defaulting to positive' )
    chrs = cor.split (':')[0]
    strand = chrs[0]
    chromosome = chrs[1:]
    coordinates = cor.split (':')[1].split ("..")   
    startCoord = coordinates[0]
    endCoord = coordinates[1]
    print ( startCoord )
    print ( endCoord )
    print ( chromosome )
    print ( strand )

    name = request.GET.get(r'name')
    if name is None:
        name = 'temp'
    if strand is None:
        strand = "+"
    
    gene_names = data.gene_ids_at_locus  (contig=chromosome, position=startCoord)
    
    j = {}

    j = { 'gene_names': gene_names }
    r = HttpResponse(json.dumps(j), content_type='application/json')
    r['Access-Control-Allow-Origin'] = '*'
    return r
