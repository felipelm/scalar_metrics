class LoadMetrics:
    """ Read values from the yaml's files
    """
    prfx  = 'ql-'
    qa_name    = ['countpix', 'getbias', 'getrms'
                   , 'xwsigma', 'countbins', 'integ'
                   , 'skycont', 'skypeak', 'skyresid', 'snr']
    
    params_keys = [['NPIX_ALARM_RANGE', 'CUTHI', 'NPIX_WARN_RANGE', 'CUTLO']
               , ['DIFF_ALARM_RANGE', 'PERCENTILES', 'DIFF_WARN_RANGE']
               , ['RMS_ALARM_RANGE', 'RMS_WARN_RANGE']
               , ['B_PEAKS', 'R_PEAKS', 'XSHIFT_ALARM_RANGE', 'WSHIFT_ALARM_RANGE'
                              , 'Z_PEAKS', 'WSHIFT_WARN_RANGE', 'XSHIFT_WARN_RANGE']
               , ['CUTHI', 'CUTLO', 'CUTMED', 'NGOOD_ALARM_RANGE', 'NGOOD_WARN_RANGE']
               , ['MAGDIFF_ALARM_RANGE', 'MAGDIFF_WARN_RANGE']
               , ['SKYCONT_ALARM_RANGE', 'SKYCONT_WARN_RANGE', 'B_CONT', 'Z_CONT', 'R_CONT']
               , ['B_PEAKS', 'R_PEAKS', 'SUMCOUNT_WARN_RANGE', 'SUMCOUNT_ALARM_RANGE', 'Z_PEAKS']
               , ['PCHI_RESID', 'PER_RESID', 'SKY_ALARM_RANGE', 'SKY_WARN_RANGE', 'BIN_SZ']
               , ['FIDSNR_WARN_RANGE', 'FIDSNR_ALARM_RANGE', 'FIDMAG']]
    
    params_dict = {'countbins': ['CUTHI',  'CUTLO',  'CUTMED',  'NGOOD_ALARM_RANGE',  'NGOOD_WARN_RANGE'],
                'countpix': ['NPIX_ALARM_RANGE', 'CUTHI', 'NPIX_WARN_RANGE', 'CUTLO'],
                'getbias':  ['DIFF_ALARM_RANGE', 'PERCENTILES', 'DIFF_WARN_RANGE'],
                'getrms':   ['RMS_ALARM_RANGE', 'RMS_WARN_RANGE'],
                'integ':    ['MAGDIFF_ALARM_RANGE', 'MAGDIFF_WARN_RANGE'],
                'skycont':  ['SKYCONT_ALARM_RANGE', 'SKYCONT_WARN_RANGE',  'B_CONT',  'Z_CONT',  'R_CONT'],
                'skypeak':  ['B_PEAKS',  'R_PEAKS',  'SUMCOUNT_WARN_RANGE',  'SUMCOUNT_ALARM_RANGE',  'Z_PEAKS'],
                'skyresid': ['PCHI_RESID',  'PER_RESID',  'SKY_ALARM_RANGE',  'SKY_WARN_RANGE',  'BIN_SZ'],
                'snr':      ['FIDSNR_WARN_RANGE', 'FIDSNR_ALARM_RANGE', 'FIDMAG'],
                'xwsigma':  ['B_PEAKS',  'R_PEAKS',  'XSHIFT_ALARM_RANGE',  'WSHIFT_ALARM_RANGE'
                             ,  'Z_PEAKS',  'WSHIFT_WARN_RANGE',  'XSHIFT_WARN_RANGE']}

    def __init__(self, cam,exp,night):
        self.cam   = cam
        self.exp   = exp
        self.night = night
        
        # QA tests available for while
        self.metric_qa_list  = ['getbias','getrms','skycont', 'countbins', 'countpix', 'snr']
        self.metric_key_list = ['BIAS','RMS_OVER_AMP','SKYCONT','NGOODFIBERS', 'NPIX_LOW', 'ELG_FIDMAG_SNR']
        self.metric_dict     = dict(zip(self.metric_qa_list, self.metric_key_list))

        # try:
        self.metrics, self.tests = self.Load_metrics_n_tests(self.qa_name)
        # except:
        #     print('File not found' ) #for {}, {}, and {}'.format(self.cam, self.exp, self.night) )
        
        
    def Load_qa(self, qa, cam, exp, night):
        """loads a single yaml file ( rather time consuming!)
         
        Arguments
        ---------
        qa:
        cam:
        exp:
        night:
        Return
        ------
        y2: list
        """
        import yaml
        cam, exp, night = self.cam, self.exp, self.night
        # exp_folder = os.path.join(desi_spectro_redux, '/exposures/')
        exp_folder = './'
        aux = '{}{}/{}/{}{}-{}-{}.yaml'.format(exp_folder, night, exp, self.prfx, qa, cam,exp)
        y2 = yaml.load(open(aux, "r"))
        print(aux)
        print('{} loaded'.format(qa))
        return y2 

    
    def Load_metrics_n_tests(self,  qa_name):
        """ Gathers all the informations in 'METRICS' and 'PARAMS'
        and returns them in individual dictionaries
        Uses: Load_qa
        Arguments
        ---------
        cam: int
            Camera
        exp: int
            Exposition ID
        night: int
            Night of exposure
        qa_name: 
        Return
        ------
        dic_met: dictionary
            A dictionary 
        
        dic_test: dictionary
    
        """
        dic_met = {}
        dic_tst = {}
        
        if isinstance(self.qa_name, list):
            qa_list = self.qa_name
        elif isinstance(self.qa_name, string):
            qa_list = [self.qa_name]
        else:
            return "Invalid QA format"
            
        for i in qa_list:
            aux = self.Load_qa(i, self.cam, self.exp, self.night)
            dic_met.update({i: aux['METRICS']})
            dic_tst.update({i: aux['PARAMS']})
        return dic_met, dic_tst

    
    def keys_from_scalars(self, qa_name, params_keys):
        """Translates QA and test in yaml file to the keys 'warn' and 'alarm'.
        Arguments
        ---------
        qa_name: list
            A list of str w/ the QA names
        params_keys: list
            List of list of str w/ keys names contained in METRICS.    
        Return
        -------
        xx: dict
            A  dictionary of <qa_name>. For each 'qa_name' another dictionary with  {kind_of_test>,
            addressing a 'kind of test' to its equivalent key inside the yaml file.
        """       
        xx = {}
        qa_name, params_keys = self.qa_name, self.params_keys

        for index, scalar in enumerate(qa_name):
            if scalar=='xwsigma': # Redistrubuting xsigma and wsigma
                xx['xsigma'] = {'alarm':'XSHIFT_ALARM_RANGE', 'warn':'XSHIFT_WARN_RANGE'}
                xx['wsigma'] = {'alarm':'WSHIFT_ALARM_RANGE', 'warn':'WSHIFT_WARN_RANGE'}
                xx.update({'xsigma':{'alarm':'XSHIFT_ALARM_RANGE', 'warn':'XSHIFT_WARN_RANGE'}
                          ,'wsigma':{'alarm':'WSHIFT_ALARM_RANGE', 'warn':'WSHIFT_WARN_RANGE'}})
            else:
                for j in params_keys[index]:
                    #print j
                    if 'ALARM_RANGE' in j:
                        alarm_name =  j
                    
                    if 'WARN_RANGE' in j:
                        warn_name  = j
                try:
                    xx.update({scalar: {'alarm':alarm_name, 'warn':warn_name}})
                except:
                    print ('?!?')
        return xx   
    
    
    def Test_ranges(self, qa, kind_of_test):
        """ Read the yaml file and returns the range of a given test
        Dependencies: qa_name, params_keys, keys_from_scalats
        Arguments
        ---------
        qa: ?list
            ?d
        kind_of_test: ?list
            ?d
        Return
        ------
        test_range: list
            A list representing [min_value, max_value]
        """      
        self.qa = qa
        self.kot = kind_of_test
        qa_name  = ['countpix', 'getbias', 'getrms'
                   , 'xwsigma', 'countbins', 'integ'
                   , 'skycont', 'skypeak', 'skyresid', 'snr']
        
        metrics = self.metrics
        tests   = self.tests 

        self.par_k   = self.params_keys
        self.d  = self.keys_from_scalars(qa_name, self.par_k)
        qalist  = qa_name + ['xsigma', 'wsigma']
    
        if self.kot not in ['warn', 'alarm']:
            raise Exception('Error: Invalid test value:', self.kot)
        
        if   self.qa == 'xwsigma':
            raise Exception('Error: using either xsigma or wsigma.')  
        elif self.qa not in qalist: 
            raise Exception('Error: Invalid QA name:', qa)
        elif(self.qa in ['xsigma', 'wsigma']):
            qa_2       = 'xwsigma'        
            test_range = tests[qa_2][self.d[self.qa][self.kot]]
        else:
            test_range = tests[qa][self.d[self.qa][self.kot]]
        
        return test_range

       
    def qa_status(self, qa):
        """Returns the status of a given qa. A.K.A Tester
        uses my_metrics, metric_dict
        Arguments
        ---------
        Return
        ------
        status: str
            Possible values: 'NORMAL', 'WARN' or 'ALARM'
        """
        self.qa = qa
        #qa      = self.qa
        
        alarm = self.Test_ranges(qa,'alarm')
        warn  = self.Test_ranges(qa,'warn')
        val   = self.metrics[qa][self.metric_dict[qa]]
        
        if isinstance(val,float) or isinstance(val, int):
            pass
        elif isinstance(val, list): #check!
            pass
        else:
            raise Exception ("Invalid variable type", val)
        if (len(alarm) < 2): # Reported by Machado
            return 'UNKNOWN'
        elif ( val <= alarm[0] or val >= alarm[1]): # ">=" comes from pipeline definition!
            return 'ALARM'
        elif (val <= warn[0] or val >= warn[1]):
            return 'WARN' 
        else:
            return 'NORMAL'

        
if __name__=="__main__":
    cam, exp, night = 'z0', '00000003', '20190101'
    print("\n\nTests for the available scalars and using yaml output\n", "="*50)
    print("TO DO:\n *docs of functions \n *what more else?")
    
    # testing 01
    lm = LoadMetrics(cam, exp, night)
    print(lm.keys_from_scalars('getbias','warn'))
    print(lm.Test_ranges('getbias', 'warn'))
    print(lm.qa_status('countpix'))
    
    
    # testing 02: 
    print('\nEvaluated here:\n') 
    my_metrics = lm.metrics
    for i in lm.metric_qa_list:
        print('{}: \t{}'.format(i, lm.qa_status(i) ))
    
    print('\n\nFrom QL file:')
    #Reading form yaml files
    for j in list(my_metrics):
        for jj in list(my_metrics[j]):
            if '_ERR' in jj:
                print('In %s \t'%(j),)
            print('{}:\t {}'.format(jj, my_metrics[j][jj]))