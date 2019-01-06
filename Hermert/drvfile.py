from getcmd import getcmd
import os, sys


# get all file names
# get input/output informations
class drvfile(object):

    def __init__(self, name):
        self.name = name
        self.apr_filename = ''
        self.site_listname = ''
        self.in_listname = ''
        self.out_filename = ''
        self.est_parfile = ''
        self.internal_consname = ''
        self.res_filename = ''
        self.geocenter_filename = ''

    def read_drvfile(self):
        wcmd = ''
        lcmd = 0
        job = 1
        # priori coordinate and velocity file
        wcmd = getcmd(self.name, 'apriori')

        self.apr_filename = wcmd[0]
        # print(self.apr_filename)
        wcmd = ''
        # site list file
        wcmd = getcmd(self.name, 'site_list')
        self.site_listname = wcmd[0]
        wcmd = ''
        # input (qob data file) list file name (mandatory)
        wcmd = getcmd(self.name, 'in_list')
        self.in_listname = wcmd[0]
        wcmd = ''
        # estimate paramter list file (mandatroy)
        wcmd = getcmd(self.name, 'est_par')
        self.est_parfile = wcmd[0]
        wcmd = ''
        # output site_xyz and site_enu for combination station only

        # internal constraint list file
        wcmd = getcmd(self.name, 'internal')
        self.internal_consname = wcmd[0]
        wcmd = ''
        print(self.internal_consname)
        # output file
        wcmd = getcmd(self.name, 'output')
        self.out_filename = wcmd[0]

        # Transformed parameter file
        wcmd = getcmd(self.name, 'trans_par_out')
        self.transform_parameter_file = wcmd[0]

        wcmd = getcmd(self.name, 'residual_file')
        self.res_filename = wcmd[0]

        wcmd = getcmd(self.name, 'geocenter_file')
        self.geocenter_filename = wcmd[0]
        wcmd = ''
        # print(self.out_filename)
