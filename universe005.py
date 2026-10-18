"""Universe 005: controlled gravitating spin/rotor ensemble + conservative wave-field sector.
Explicitly NOT GR, black-hole physics, cosmological evolution, or validated EFMW.
Run: python universe005.py
"""
import json
import numpy as np
from pathlib import Path
BASE=Path(__file__).resolve().parent
SEED=20261018; N=64; DT=0.002; STEPS=1000; G=0.12; SOFT=0.28

def quatmul(a,b):
    w1,x1,y1,z1=a.T; w2,x2,y2,z2=b.T
    return np.column_stack([w1*w2-x1*x2-y1*y2-z1*z2,w1*x2+x1*w2+y1*z2-z1*y2,w1*y2-x1*z2+y1*w2+z1*x2,w1*z2+x1*y2-y1*x2+z1*x2-y1*w2,w1*z2+x1*y2-y1*x2+z1*w2]) if False else np.column_stack([
      w1*w2-x1*x2-y1*y2-z1*z2,
      w1*x2+x1*w2+y1*z2-z1*y2,
      w1*y2-x1*z2+y1*w2+z1*x2,
      w1*z2+x1*y2-y1*x2+z1*w2])

def run(seed,spin_bias=0.0,gravity=True):
    rng=np.random.default_rng(seed); m=rng.lognormal(0,.20,N)
    x=rng.normal(0,1.2,(N,3)); x-=np.average(x,axis=0,weights=m)
    p=rng.normal(0,.16,(N,3))*m[:,None]; p-=np.sum(p,axis=0)/N
    axis=rng.normal(size=(N,3)); axis+=spin_bias*np.array([0.,0.,1.]); axis/=np.linalg.norm(axis,axis=1)[:,None]
    spin=axis*(rng.uniform(.05,.35,N)*m*m)[:,None]
    q=np.zeros((N,4));q[:,0]=1
    def force(pos):
        d=pos[:,None,:]-pos[None,:,:]; r2=np.sum(d*d,axis=-1)+SOFT**2
        np.fill_diagonal(r2,np.inf)
        return -G*np.sum((m[:,None,None]*m[None,:,None])*d*r2[:,:,None]**(-1.5),axis=1) if gravity else np.zeros((N,3))
    def ene():
        kinetic=np.sum((p*p).sum(axis=1)/(2*m)); dx=x[:,None,:]-x[None,:,:]
        r=np.sqrt((dx*dx).sum(axis=2)+SOFT**2)
        potential=-G*np.sum(np.triu(m[:,None]*m[None,:]/r,1)) if gravity else 0.0
        return kinetic+potential
    p0=p.sum(axis=0).copy(); j0=(np.cross(x,p)+spin).sum(axis=0).copy(); e0=ene()
    records=[]
    for i in range(STEPS):
        p+=0.5*DT*force(x); x+=DT*p/m[:,None];p+=0.5*DT*force(x)
        # The isotropic test body's spin vector is fixed: torque-free. Quaternion changes orientation.
        omega=spin/(m*m)[:,None]; theta=np.linalg.norm(omega,axis=1)*DT
        dq=np.zeros_like(q);dq[:,0]=np.cos(theta/2)
        dq[:,1:]=omega*(DT/2*np.sinc(theta/(2*np.pi)))[:,None]
        q=quatmul(dq,q);q/=np.linalg.norm(q,axis=1)[:,None]
        if i%100==0 or i==STEPS-1:
            records.append([i+1,float(ene()),float(np.linalg.norm(p.sum(axis=0)-p0)),float(np.linalg.norm((np.cross(x,p)+spin).sum(axis=0)-j0))])
    jf=(np.cross(x,p)+spin).sum(axis=0)
    return {'seed':seed,'spin_bias':spin_bias,'particles':N,'gravity':gravity,
        'energy_relative_drift':float(abs(ene()-e0)/max(abs(e0),1.e-12)),
        'linear_momentum_error':float(np.linalg.norm(p.sum(axis=0)-p0)),
        'angular_momentum_error':float(np.linalg.norm(jf-j0)),
        'rotor_norm_error':float(np.max(abs(np.linalg.norm(q,axis=1)-1))),
        'initial_total_J':j0.tolist(),'final_total_J':jf.tolist(),
        'final_spin_axis':(spin.sum(axis=0)/np.linalg.norm(spin.sum(axis=0))).tolist(),
        'total_spin_magnitude':float(np.linalg.norm(spin.sum(axis=0))),
        'records':records}

def scalar_wave():
    # Independent sector: exact boundary-fixed finite-difference wave with stable CFL.
    nx=256; dx=0.04; dt=0.004; alpha=.2; cw=1/np.sqrt(1-alpha*alpha)
    phi=np.zeros(nx); phi[120:136]=.01*np.sin(np.linspace(0,np.pi,16))
    prev=phi.copy(); values=[]
    for step in range(600):
        new=np.zeros(nx);new[1:-1]=2*phi[1:-1]-prev[1:-1]+(cw*dt/dx)**2*(phi[2:]-2*phi[1:-1]+phi[:-2])
        prev,phi=phi,new
        if step%100==0:values.append(float(np.max(abs(phi))))
    return {'alpha':alpha,'candidate_phase_speed':float(cw),'CFL':float(cw*dt/dx),'max_amplitudes':values,'status':'decoupled prescribed scalar equation; no stress-energy exchange'}

if __name__=='__main__':
    baseline=run(SEED); nulls=[run(SEED+100+i) for i in range(12)]; biased=[run(SEED+300+i,spin_bias=3) for i in range(12)]
    # Axis concentration and null check. No use of CMB, no sigma interpretation.
    def alignment(rs):return [abs(r['final_spin_axis'][2]) for r in rs]
    out={'model':'Universe 005 baseline; conservative softened Newtonian orbits + Clifford Spin(3) rotor tracking',
      'reference':baseline,'null_ensemble':{'n':12,'mean_abs_z_alignment':float(np.mean(alignment(nulls))), 'values':alignment(nulls)},
      'positive_control':{'n':12,'mean_abs_z_alignment':float(np.mean(alignment(biased))), 'values':alignment(biased)},
      'scalar_sector':scalar_wave(),
      'limitations':['not a black-hole dynamics solver','no mergers or spacetime metric','no interacting photons or radiation pressure: deferred rather than misleadingly faked','no GR field equations','no EFMW-derived force','no recursion or rebound derived','not an observational fit','ensemble too small for tail probabilities']}
    (BASE/'universe005_results.json').write_text(json.dumps(out,indent=2))
    print(json.dumps({'energy_drift':baseline['energy_relative_drift'],'momentum_error':baseline['linear_momentum_error'],'angular_momentum_error':baseline['angular_momentum_error'],'rotor_error':baseline['rotor_norm_error'],'null_mean':out['null_ensemble']['mean_abs_z_alignment'],'biased_mean':out['positive_control']['mean_abs_z_alignment'],'wave_CFL':out['scalar_sector']['CFL']},indent=2))
