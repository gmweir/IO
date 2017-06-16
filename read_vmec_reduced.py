# -*- coding: utf-8 -*-

# only read the following components from a NetCDF wout file:
# xm, xn, iasym
# bmnc, gmnc, bsubumnc, bsupvmnc, currumnc, currvmnc
# in case of iasym==1 also the following:
# bmns, gmns, bsubumns, bsubvmns, currumns, currvmns

from netCDF4 import Dataset
import numpy as np
#import pybaseutils.Struct as Struct

mu0=4*np.pi*1e-7

# Calculate Currents
def calc_curr(f):
    f['currumnc']=np.zeros([f['ns'], f['mnmax_nyq']])
    f['currvmnc']=np.zeros([f['ns'], f['mnmax_nyq']])
    
    ohs = f['ns']-1.0
    hs  = 1.0/np.double(ohs)
    ns = f['ns']
    
    shalf=np.zeros(ns)
    sfull=np.zeros(ns)
    for i in np.arange(1,ns):
        shalf[i] = np.sqrt(hs*(i-0.5))
        sfull[i] = np.sqrt(hs*(i-0.0))
        
    js1 = np.arange(2,ns-1)
    js  = np.arange(1,ns-2)
    
    for mn in np.arange(f['mnmax_nyq']):
        if (np.mod(f['xm_nyq'][mn],2) == 1):
            t1  = 0.5*(shalf[js1] * f['bsubsmns'][js1,mn] + 
                       shalf[js]  * f['bsubsmns'][js,mn]   ) / sfull[js]
            bu0 = f['bsubumnc'][js,mn]/shalf[js]
            bu1 = f['bsubumnc'][js1,mn]/shalf[js1]
            t2  = ohs*(bu1-bu0)*sfull[js]+0.25*(bu0+bu1)/sfull[js]
            bv0 = f['bsubvmnc'][js,mn]/shalf[js]
            bv1 = f['bsubvmnc'][js1,mn]/shalf[js1]
            t3  = ohs*(bv1-bv0)*sfull[js]+0.25*(bv0+bv1)/sfull[js]
        else:
            t1  = 0.5*(f['bsubsmns'][js1,mn]+f['bsubsmns'][js,mn])
            t2  = ohs*(f['bsubumnc'][js1,mn]-f['bsubumnc'][js,mn])
            t3  = ohs*(f['bsubvmnc'][js1,mn]-f['bsubvmnc'][js,mn])
        f['currumnc'][js,mn] = -np.double(f['xn_nyq'][mn])*t1 - t3
        f['currvmnc'][js,mn] = -np.double(f['xm_nyq'][mn])*t1 + t2
        
    f['currumnc'][0,:]=0.0
    f['currvmnc'][0,:]=0.0
    for i in range(f['mnmax_nyq']):
        if (f['xm_nyq'][i]<=1):
            f['currumnc'][0,i]=2*f['currumnc'][1,i]-f['currumnc'][2,i]
            f['currvmnc'][0,i]=2*f['currvmnc'][1,i]-f['currvmnc'][2,i]
    
    f['currumnc'][:,f['ns']]=2*f['currumnc'][:,f['ns']-1]-f['currumnc'][:,f['ns']-2]
    f['currvmnc'][:,f['ns']]=2*f['currumnc'][:,f['ns']-1]-f['currvmnc'][:,f['ns']-2]
    f['currumnc']=f['currumnc']/mu0;
    f['currvmnc']=f['currvmnc']/mu0;
#    if f.iasym
#        f.currumns=zeros(f.mnmaxnyq,f.ns);
#        f.currvmns=zeros(f.mnmaxnyq,f.ns);
#        for mn = 1:f.mnmax_nyq
#            if (mod(f.xm_nyq,2) == 1)
#                t1  = 0.5.*(shalf(js1).*f.bsubsmnc(mn,js1)+...
#                    shalf(js).*f.bsubsmnc(mn,js))./sfull(js);
#                bu0 = f.bsubumns(mn,js)./shalf(js);
#                bu1 = f.bsubumns(mn,js1)./shalf(js1);
#                t2  = ohs.*(bu1-bu0).*sfull(js)+0.25.*(bu0+bu1)./sfull(js);
#                bv0 = f.bsubvmns(mn,js)./shalf(js);
#                bv1 = f.bsubvmns(mn,js1)./shalf(js1);
#                t3  = ohs.*(bv1-bv0).*sfull(js)+0.25.*(bv0+bv1)./sfull(js);
#            else
#                t1  = 0.5.*(f.bsubsmnc(mn,js1)+f.bsubsmnc(mn,js));
#                t2  = ohs.*(f.bsubumns(mn,js1)+f.bsubumns(mn,js));
#                t3  = ohs.*(f.bsubvmns(mn,js1)+f.bsubvmns(mn,js));
#            end
#            f.currumns(mn,js) = -double(f.xn_nyq(mn)).*t1 - t3;
#            f.currvmns(mn,js) = -double(f.xn_nyq(mn)).*t1 + t2;
#        end
#        % OLD WAY
#        %for i=2:f.ns-1
#        %    f.currumns(:,i)= double(f.xnnyq)'.*f.bsubsmnc(:,i)-(f.ns-1).*(f.bsubvmns(:,i+1)-f.bsubvmns(:,i));
#        %    f.currvmns(:,i)= double(f.xmnyq)'.*f.bsubsmnc(:,i)+(f.ns-1).*(f.bsubumns(:,i+1)-f.bsubumns(:,i));
#        %end
#        f.currumns(:,1)=0.0;
#        f.currvmns(:,1)=0.0;
#        for i=1:f.mnmax_nyq
#            if (f.xm_nyq(i)==0)
#                f.currumns(i,1)=2.*f.currumns(i,2)-f.currumns(i,3);
#                f.currvmns(i,1)=2.*(f.ns-1).*f.bsubumns(i,2);
#            end
#        end
#        f.currumns(:,f.ns)=2.*f.currumns(:,f.ns-1)-f.currumns(:,f.ns-2);
#        f.currvmns(:,f.ns)=2.*f.currvmns(:,f.ns-1)-f.currvmns(:,f.ns-2);
#        f.currumns=f.currumns./mu0;
#        f.currvmns=f.currvmns./mu0;
#    end
    
    #return f.dict_from_class()
    return f

def read_vmec(filename):
    rootgrp = Dataset(filename, 'r')
    vmec_data=dict()
    
    #version=rootgrp['/version_'][0]    
    
    vmec_data['xm']=rootgrp['/xm'][:]
    vmec_data['xm']=vmec_data['xm'][:,np.newaxis]
    vmec_data['xn']=-rootgrp['/xn'][:]
    vmec_data['xn']=vmec_data['xn'][:,np.newaxis]
    vmec_data['mpol']=rootgrp['/mpol'][0]
    vmec_data['ntor']=rootgrp['/ntor'][0]
    vmec_data['nfp']=rootgrp['/nfp'][0]
    vmec_data['iasym']=rootgrp['/lasym__logical__'][0]
    
    vmec_data['rmnc']=rootgrp['/rmnc'][:,:]
    vmec_data['zmns']=rootgrp['/zmns'][:,:]
    
    # for currumnc,... calculation
    vmec_data['mnmax_nyq']=rootgrp['/mnmax_nyq'][0]    
    vmec_data['ns']=rootgrp['/ns'][0]
    ns=vmec_data['ns']
    
    vmec_data['xm_nyq']=rootgrp['/xm_nyq'][:]
    vmec_data['xn_nyq']=rootgrp['/xn_nyq'][:]
    
    vmec_data['bmnc']=rootgrp['/bmnc'][:,:]
    vmec_data['gmnc']=rootgrp['/gmnc'][:,:] 
    
    vmec_data['bsubsmns']=rootgrp['/bsubsmns'][:,:]
    vmec_data['bsubumnc']=rootgrp['/bsubumnc'][:,:]
    vmec_data['bsubvmnc']=rootgrp['/bsubvmnc'][:,:]
    
    # not tested yet...    
    if (vmec_data['iasym']):
        vmec_data['bmns']=rootgrp['/bmns'][:,:]
        vmec_data['gmns']=rootgrp['/gmns'][:,:]
        
        vmec_data['bsubsmnc']=rootgrp['/bsubsmnc'][:,:]
        vmec_data['bsubumns']=rootgrp['/bsubumns'][:,:]
        vmec_data['bsubvmns']=rootgrp['/bsubvmns'][:,:]        
    
    # we are finished reading the file
    rootgrp.close()
    
    # calc currumnc, currvmnc
    # important: do this _BEFORE_ you transform the half-mesh quantities onto
    # the full mesh !!!!!!!!!
    currents=calc_curr(vmec_data)
    
    # Put matrix quantities on full grid
    for key in ['bmnc','gmnc','bsubsmns','bsubumnc','bsubvmnc']:
        vmec_data[key][0,:] = 1.5 * vmec_data[key][1,:] - 0.5 * vmec_data[key][2,:]
        vmec_data[key][1:ns-2,:] = 0.5 * (vmec_data[key][1:ns-2,:] + vmec_data[key][2:ns-1,:])
        vmec_data[key][ns-1,:] = 2.0 * vmec_data[key][ns-2,:] - vmec_data[key][ns-3,:]    
    if vmec_data['iasym']:
        for key in ['bmns','gmns','bsubsmnc','bsubumns','bsubvmns']:
            vmec_data[key][0,:] = 1.5 * vmec_data[key][1,:] - 0.5 * vmec_data[key][2,:]
            vmec_data[key][1:ns-2,:] = 0.5 * (vmec_data[key][1:ns-2,:] + vmec_data[key][2:ns-1,:])
            vmec_data[key][ns-1,:] = 2.0 * vmec_data[key][ns-2,:] - vmec_data[key][ns-3,:]

    vmec_data['currumnc']=currents['currumnc']
    vmec_data['currvmnc']=currents['currvmnc']
    if (vmec_data['iasym']):
        vmec_data['currumns']=currents['currumns']
        vmec_data['currvmns']=currents['currvmns']

    return vmec_data