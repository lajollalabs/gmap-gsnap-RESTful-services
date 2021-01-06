import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from bed import BEDTOOLS

@csrf_exempt
def hello(request):
    r = HttpResponse(json.dumps("hello world"), content_type="application/json")
    r['Access-Control-Allow-Origin'] = '*'
    return r

@csrf_exempt
def get_sequence_for_coordinates(request):
    startCoord = request.GET.get(r'start')
    endCoord = request.GET.get(r'end')
    chromosome = request.GET.get(r'chr')
    strand = request.GET.get(r'strand')
    name = request.GET.get(r'name')
   
    print ( chromosome )

    if name is None:
        name = 'temp'


    if strand is None:
        strand = "+"
    sg = BEDTOOLS()
    j = {}
    res = sg.get_sequence (chromosome, startCoord, endCoord, name, strand)
    lines = res.split ('\n')
    commentLine = lines[0]
    sequence = lines[1]

    j = { 'header': commentLine, 'sequence':sequence }
    r = HttpResponse(json.dumps(j), content_type='application/json')
    r['Access-Control-Allow-Origin'] = '*'
    return r
#

#+17:7676012..7676031

@csrf_exempt
def get_sequence_for_gsnap_coordinates(request):
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
    sg = BEDTOOLS()
    j = {}
    res = sg.get_sequence (chromosome, startCoord, endCoord, name, strand)
    lines = res.split ('\n')
    commentLine = lines[0]
    sequence = lines[1]

    j = { 'header': commentLine, 'sequence':sequence }
    r = HttpResponse(json.dumps(j), content_type='application/json')
    r['Access-Control-Allow-Origin'] = '*'
    return r





@csrf_exempt
def simple_gsnap(request):
    sequence = request.GET.get(r'sequence')
    type (sequence)
    sg = GSNAP ()
    j = {}
    res = sg.runGSNAP (str(sequence))
    lines = res.split ('\n')
    values = parseSimple(lines)
    j = { 'seq':sequence, 'res':values }
    r = HttpResponse(json.dumps(j), content_type='application/json')
    r['Access-Control-Allow-Origin'] = '*'
    return r
#	if sequence.find (',') > 0:
#		res = []
#		slist = sequence.split (',')
#		for s in slist:
#			r = sg.runGSNAP ( s )
#			lines = r.split ( '\n' )
#			values = parseSimple ( lines )
#			t = {
#				'seq':s,
#				'res':values
#			}
#			res.append (t)
#		j = {
#			'seq':sequence,
#			'count':len(slist),
#			'res':res
#		}
#	else:
#		res = sg.runGSNAP (sequence)
#		lines = res.split ('\n')
#                values=parseSimple(lines)
#		j = {
#			'seq':sequence,
#			'res':values
#		}
#	r = HttpResponse(json.dumps(j), content_type="application/json")
#	r['Access-Control-Allow-Origin'] = '*'
#	return r
#
def parseSimple(lines):
    r = []
    it = iter(lines)
    for l in it:
        l=l.strip()
        if l.startswith('input-sequence'):
            indexi = l.find(':')
            if indexi > 0:
                r.append({'input-sequence':l[indexi+1:]})
        elif l.startswith ( 'comment' ):
            indexi = l.find(':')
            if indexi > 0:
                test = l[indexi+1:]
            if len(test)>0:
                r.append({'comment':l[indexi+1:]})
        elif l.startswith ('>'):
            print ( 'skip line')
        else:
            c=parseSimpleRegion (l)
            if len(c) > 1:
                r.append (c)
    return r

def parseSimpleRegion ( l ):
    l = l.strip()
    d = l.split ('\t')
    j = {}
    if len(d) <= 1:
        return j
    sequence = d[0]
    basecount = d[1]
    coordinates = d[2]
    matchstrings = d[3]
    j['seq']=sequence
    j['base_index_range']=basecount
    j['coords']= coordStringToJSON(coordinates)
    j['match']=matchstrings
    return j


def coordStringToJSON ( cstring ):
    strand =  cstring[:1]
    col = cstring.find (':')
    ensembleId = cstring[1:col]
    coord_range = cstring[(col+1):]
    f = coord_range.find ( '..' )
    start = int(coord_range[:f])
    end = int (coord_range[(f+2):])


    if strand == '+':
        strand = '1'
    else:
        strand = '-1'
    js = {
	    'strand':strand,
	    'coord_system':ensembleId,
	    'start':start,
	    'end':end,
	    'coord_range': coord_range
    }
    print (' cstring ', cstring )
    return js



#
#@csrf_exempt
#def gsnap_cdna_to_genomic(request):
#	sequence = request.GET.get('sequence')
#	sg = GSNAP ()
#	res = sg.runGSNAP (sequence)
#	print ' res is : ', res
#	line = res.split ('\n')
#	tabs = line[2].split ()
#	t = tabs[2]
#	t = convertGMAP_CDNA_FORMAT_TO_ENSEMBL_FORMAT ( t )
#	jc = getGenomicFromCDNA ( t )
#	j = {'res': jc}	
#	r = HttpResponse(json.dumps(j), content_type="application/json")
#	r['Access-Control-Allow-Origin'] = '*'
#	return r
#
#
#def convertGMAP_CDNA_FORMAT_TO_ENSEMBL_FORMAT( cdna ):
#	# split hte numbers 
#	print cdna 
#	print '------------' 
#	number_start = cdna.index(':')
#	numbers = cdna[number_start+1:]
#	idstring = cdna[1:number_start]
#
#	if idstring.index ('.') > 0:
#		idi = idstring.index ('.')
#		idstring = idstring[:idi]
#
#
#	n=numbers.split ('..')
#	start = int(n[0])
#	stop = int(n[1])
#	direction = cdna[0:1]
#	if start > stop:
#		temp = start
#		start = stop
#		stop = temp
#	return idstring + '/' + str(start) + '..' + str(stop)
#
#
#def getGenomicFromCDNA ( cdna ):
#    #http://rest.ensembl.org/map/cdna/ENST00000233242.5/3249..3268
#	print ' cdna ', cdna 
#	contents = urllib2.urlopen("http://rest.ensembl.org/map/cdna/" + str(cdna));
#	ensemble_response =contents.read()
#	lines = ensemble_response.split ('\n')
#	it = iter (lines)
#	reg = []
#	index = 0;
#	for l in it:
#		l = l.strip()
#		#print ' line ', l 
#		if l.startswith ('-'):
#			parseRegion ( it, reg )
#	return reg
#
#
#def parseRegion (it, reg):
#	ig = {}
#	for s in it:
#		s=s.strip()	
#		iv = s.find(':')
#		if iv > 0:
#			vals = s.split (':')
#			if vals[0]=='start' or vals[0]=='end':
#				ig[vals[0].strip()]=int(vals[1].strip())	
#			else:
#				ig[vals[0].strip()]=vals[1].strip()	
#		else:
#			reg.append ( ig )
#			ig = {}
#	return reg
#
#
#@csrf_exempt
#def save(request):
#    json_data = str(request.body)
#    print str ( json_data )
#    value = json.loads(json_data)
#    user = value.get(r"user_id")
#    rule = value.get(r"rule_value")
#    name = value.get(r"rule_name")
#    type = value.get(r"rule_type")
#    input_label = None;
#    if "input_label" in value:
#        input_label = value.get(r"input_label")
#    else:
#        input_label = "undefined"
#    print (' user ', user, ' name ', name, ' rule ', rule, 'type ', type)
#    if type is None or name is None or user is None or rule is None:
#        j = {
#            'msg': 'Information incomplete; not saved'
#        }
#        r = HttpResponse(json.dumps(j), content_type="application/json")
#        r['Access-Control-Allow-Origin'] = '*'
#        return r
#    j = {
#        'msg': 'Saved'
#    }
#    r = HttpResponse(json.dumps(j), content_type="application/json")
#    r['Access-Control-Allow-Origin'] = '*'
#    return r
#
#    return r
