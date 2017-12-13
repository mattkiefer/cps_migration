from transfers.models import Student, District, School, Transfer, IncomingTransfer
from cps_migration.settings import BASE_DIR
from reports.reports import get_maj_race_schools
import csv

### START CONFIG ###
output_dir = BASE_DIR + '/graphics/data/'
low_income_threshold = 0.8
### END CONFIG ###

seg_schools = get_maj_race_schools()
seg_low_inc_schools = [x for x in seg_schools if x.low_income/float(x.housed) > low_income_threshold]


def interesting_cps_schools(schools=None,low_income_threshold=low_income_threshold):
    """
    return details on cps school transfers,
    defaults to all low-inc, black cps schools
    but you can pass in a custom list too
    """
    # query
    seg_schools = []
    if schools:
        pass
    else:
        schools = seg_low_inc_schools
    for school in schools:
        seg_schools.append({
                        'name': school.name,
                        'address': school.address,
                        'city': school.city,
                        'zip': school.zip_code,
                        'housed': school.housed,
                        'black': school.black,
                        'low_income': school.low_income,
                        'transfers': len(Transfer.objects.filter(from_serving_school=school,to_serving_school__isnull=False))
                       })
    sorted_seg_schools = sorted(seg_schools, key=lambda x: x['transfers']/float(x['housed']), reverse=True)

    # output
    output_filepath = output_dir + 'interesting_cps_schools.csv'
    output_file = open(output_filepath,'w')
    output_headers = ['name','address','city','zip','housed','black','low_income','transfers']
    output_csv = csv.DictWriter(output_file,output_headers)
    output_csv.writeheader()

    for seg_school in sorted_seg_schools:
        output_csv.writerow(seg_school)
    output_file.close()
    return sorted_seg_schools


def interesting_suburban_dists(schools=None,low_income_threshold=low_income_threshold):
    """
    """
    # query
    sub_dists = {}
    if not schools:
        schools = seg_low_inc_schools
    for school in schools:
        for transfer in Transfer.objects.filter(from_serving_school=school,to_serving_school__isnull=False):
            sub_school = transfer.to_serving_school
            sub_dist = sub_school.district
            if sub_dist: 
                if sub_dist not in sub_dists:
                    sub_dists[sub_dist] = {
                                           'transfers': 0,
                                          }
                sub_dists[sub_dist]['transfers'] += 1
    for d in sub_dists:
        sub_dists[d]['name'] = d.name
        sub_dists[d]['city(ies)'] = ', '.join(list(set([s.city for s in d.school_set.all()])))
        sub_dists[d]['housed'] = sum([x.housed for x in d.school_set.all()])
        sub_dists[d]['black'] = sum([x.black for x in d.school_set.all()])
        sub_dists[d]['low_income'] = sum([x.low_income for x in d.school_set.all()])
    try:
        sub_dists_sorted = sorted([sub_dists[x] for x in sub_dists], key = lambda z: z['transfers']/float(z['housed']), reverse = True)
    except Exception, e:
        import ipdb; ipdb.set_trace()
    # output
    output_filepath = output_dir + 'interesting_sub_dists.csv'
    output_file = open(output_filepath,'w')
    output_headers = ['name','city(ies)','housed','black','low_income','transfers']
    output_csv = csv.DictWriter(output_file,output_headers)
    output_csv.writeheader()
    for dist in sub_dists_sorted:
        output_csv.writerow(dist)
    output_file.close()

    return sub_dists_sorted

    



def cps_school_report(school):
    """
    for this cps school,
    break out outbound transfer counts 
    by suburban district
    """
    # query
    sub_dists = {}
    transfers = Transfer.objects.filter(from_serving_school=school,to_serving_school__isnull=False)
    for transfer in transfers:
        school = transfer.to_serving_school
        dist = school.district
        if dist not in sub_dists:
            sub_dists[dist] = {
                               'name': dist.name,
                               'city(ies)': ', '.join(list(set([s.city for s in dist.school_set.all()]))),
                               'housed': sum([x.housed for x in dist.school_set.all()]),
                               'black': sum([x.black for x in dist.school_set.all()]),
                               'low_income': sum([x.low_income for x in dist.school_set.all()]),
                               'transfers': 0,
                              }
        sub_dists[dist]['transfers'] += 1
    sub_dists_sorted = sorted([sub_dists[x] for x in sub_dists], key = lambda z: z['transfers'], reverse = True)

    # output
    output_filepath = output_dir + school.name.replace(' ','-') + '.csv'
    output_file = open(output_filepath,'w')
    output_headers = ['name','city(ies)','housed','black','low_income','transfers']
    output_csv = csv.DictWriter(output_file,output_headers)
    output_csv.writeheader()
    for dist in sub_dists_sorted:
        output_csv.writerow(dist)
    output_file.close()

    return sub_dists_sorted



def sub_dist_report(dist):
    """
    for this suburban district,
    break out inbound transfer counts
    by cps school
    """
    # query
    cps_schools = {}
    for school in dist.school_set.all():
        transfers = Transfer.objects.filter(to_serving_school=school)
        for transfer in transfers:
            school = transfer.from_serving_school
            if school: 
                if school not in cps_schools:
                    cps_schools[school] = {
                                           'name': school.name,
                                           'housed': school.housed,
                                           'black': school.black,
                                           'low_income': school.low_income,
                                           'transfers': 0,
                                          }
                cps_schools[school]['transfers'] += 1
    cps_schools_sorted = sorted([cps_schools[x] for x in cps_schools], key = lambda z: z['transfers'], reverse = True)

    # output
    output_filepath = output_dir + dist.name.replace(' ','-') + '.csv'
    output_file = open(output_filepath,'w')
    output_headers = ['name','housed','black','low_income','transfers']
    output_csv = csv.DictWriter(output_file,output_headers)
    output_csv.writeheader()
    for school in cps_schools_sorted:
        output_csv.writerow(school)
    output_file.close()

    return cps_schools_sorted



def sub_school_report(schools):
    """
    break out cps school counts for these sub schools
    """
    pass
