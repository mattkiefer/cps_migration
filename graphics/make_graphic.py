from cps_migration.settings import BASE_DIR
from mapbox import Static 
from graphic_utils import get_boundary_feature, get_point_feature

### START CONFIG ###
# ugh ... so suburban schools use boundaries, which are named in shapefiles
# and cps schools use points, which are derived from address in data
map_data = {
            'thorton':
                      {
                       'sub_dists': ['Thornton Township High School District 205'],#['Thornton Twp HSD 205'],
                       'cps_schools': ['Chicago Vocational Career Acad HS','Morgan Park High School'],
                       'zoom': 1,
                      },
            'rockford':
                      {
                       'sub_dists': ['Rockford School District 205'],
                       'cps_schools': ['Bradwell Comm Arts & Sci Elem Sch'],
                       'zoom': 1,
                      }
           }
map_img = 'mapbox.streets'
maps_dir = BASE_DIR + '/graphics/maps/'
### END CONFIG ###

service = Static()

def make_all_maps():
    for map_datum in map_data:
        make_a_map(map_datum)


def make_a_map(map_datum):
    print map_datum
    features = []
    for sub_dist_name in map_data[map_datum]['sub_dists']:
        feature = get_boundary_feature(sub_dist_name)
        features.append(feature)
    for cps_school_name in map_data[map_datum]['cps_schools']:
        feature = get_point_feature(cps_school_name)
        features.append(feature)
    response = service.image(map_img,features=features,z=map_data[map_datum]['zoom'])
    map_file_path = maps_dir + map_datum + '.png'
    with open(map_file_path,'wb') as output:
        output.write(response.content)
    print map_file_path

