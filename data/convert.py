from csvkit.utilities import in2csv
import csv

### START CONFIG ###
data_dir = '/home/matt/chicago-reporter/cps_migration/cps_migration/data/source/'
enrollment_in_path = data_dir + '2016-17 fall enrollment count ISBE.xls'
enrollment_out_path = enrollment_in_path.replace(' ','_').replace('source','processed').replace('xls','csv')
rcdts_in_path = data_dir + 'RCDTS all.xls'
transfers_in_paths = [data_dir + x for x in 
        #['ISBE CPS TRANSFER DATA 2013 to 2017.xlsx','ISBE CPS TRANSFER DATA 2009 to 2013.xlsx']
        ['18-073-belsha-follow up doc 2009 to 2017.xlsx']
        ]
### END CONFIG ###


def convert_enrollment():
    args = [enrollment_in_path,'-K','1'] # skip the first line
    # come up with a clean output filename, on the right path
    in2csv.In2CSV(args,output_file=open(enrollment_out_path,'w')).main()
    for line_break in ['Housed']:
        # get rid of inline line breaks
        text_buffer = open(enrollment_out_path).read().replace(line_break + ' \n', line_break + ' ')
        writer = open(enrollment_out_path,'w')
        writer.write(text_buffer)
        writer.close()

        # cut off before null byte
        csv_data = csv.DictReader(open(enrollment_out_path))
        data = [x for x in csv_data]
        bad_line = [x for x in data if 'Total in Other Attendance Sites' in x['School Name']][0]
        bad_line_no = data.index(bad_line)
        new_data = data[0:bad_line_no]
        writer = open('/tmp/enrollment.csv','w') # race condition when you re-use the filename
        csv_writer = csv.DictWriter(writer,csv_data.fieldnames)
        csv_writer.writeheader()
        csv_writer.writerows(new_data)
        writer.close()

        # validate
        csv_infile = csv.DictReader(open('/tmp/enrollment.csv'))
        validated_data = [x for x in csv_infile if x['Reg/Cty/ Dist/Type']]
        writer = open(enrollment_out_path,'w')
        csv_outfile = csv.DictWriter(writer, csv_infile.fieldnames)
        csv_outfile.writeheader()
        for datum in validated_data:    
            csv_outfile.writerow(datum)
            print datum
        writer.close()

def convert_rcdts():
    sheet_names = ["Public Dist & Sch",
                   "Spec Educ Dist & Sch",
                   "ISC, ROE, Reg Prg",
                   "Voc Tech",
                   "Non Pub Sch",
                   "SpEdPrivFac"]
    for sheet in sheet_names:
        out_path = rcdts_in_path.replace('.xls','').replace('source','processed') + "__" + sheet + ".csv"
        out_path = out_path.replace(' ','_')
        args = [rcdts_in_path,'--sheet',sheet]
        in2csv.In2CSV(args,output_file=open(out_path,'w')).main()
        for line_break in ['Region-2','County-3','District-4']:
            text_buffer = open(out_path).read().replace(line_break + '\n',line_break + ' ')
            writer = open(out_path,'w')
            writer.write(text_buffer)
            writer.close()


def convert_transfers():
    for transfers_in_path in transfers_in_paths:
        sheet_names = ["CPS Enrollment",
                       "Year After CPS"]
        for sheet in sheet_names:
            out_path = transfers_in_path.replace('.xlsx','').replace('source','processed') + "__" + sheet + ".csv"
            out_path = out_path.replace(' ','_')
            args = [transfers_in_path,'--sheet',sheet]
            in2csv.In2CSV(args,output_file=open(out_path,'w')).main()


def init():
    convert_enrollment()
    convert_rcdts()
    convert_transfers()
