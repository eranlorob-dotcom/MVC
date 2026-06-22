import json, numpy as np, pandas as pd, unicodedata
from shapely.geometry import shape
from scipy import stats

PARAMS = ['pct_alimentation','pct_service_garde','pct_ecole_prim','pct_ecole_sec','pct_nature',
          'pct_loisirs','pct_culture','pct_pharmacie','pct_sante','pct_transport','pct_autopartage','pct_cyclable']
ESSENTIAL = ['pct_alimentation','pct_service_garde','pct_ecole_prim','pct_ecole_sec','pct_pharmacie','pct_sante']

d = json.load(open('/mnt/user-data/uploads/mvc_laurentides_2026-06-19.geojson'))
rows=[]
for f in d['features']:
    p=f['properties']; c=shape(f['geometry']).centroid
    r={'mun':p['MUS_NM_MUN'],'mrc':p['MUS_NM_MRC'],'sup':p['superficie_km2'],
       'logements':p['nb_logements'],'score':p['score_mvc_pct'],'lat':c.y}
    for k in PARAMS: r[k]=p.get(k)
    rows.append(r)
df=pd.DataFrame(rows)

# scored, exclude Kanesatake (sup=0 -> no-data)
sc=df[df['score'].notna()].copy()
sc=sc[~sc['mun'].str.contains('Kanesatake',na=False)].copy()
sc['densite']=sc['logements']/sc['sup']
def milieu(dn): return 'dense' if dn>=100 else ('inter' if dn>=10 else 'rural')
sc['milieu']=sc['densite'].apply(milieu)
print("="*70)
print("BASE: scored units excl. Kanesatake =",len(sc))
print("Milieu split:",sc['milieu'].value_counts().to_dict())
print("Composite: median=%.1f mean=%.1f sd=%.1f min=%d max=%d"%(
    sc['score'].median(),sc['score'].mean(),sc['score'].std(),sc['score'].min(),sc['score'].max()))
for m in ['dense','inter','rural']:
    g=sc[sc['milieu']==m]['score']
    print("  %-6s n=%2d mean=%.1f median=%.1f"%(m,len(g),g.mean(),g.median()))

print("\n"+"="*70)
print("A1. WEIGHTING SENSITIVITY (equal vs essential-weighted ×2)")
sc['w_score']=(sc[ESSENTIAL].sum(axis=1)*2 + sc[[p for p in PARAMS if p not in ESSENTIAL]].sum(axis=1)*1)/(len(ESSENTIAL)*2+ (12-len(ESSENTIAL))*1)
rho,pv=stats.spearmanr(sc['score'],sc['w_score'])
print("Spearman rho(equal,weighted)=%.3f  p=%.2e"%(rho,pv))
def band(x): return 'complete' if x>=70 else ('developing' if x>=40 else 'incomplete')
sc['b_eq']=sc['score'].apply(band); sc['b_w']=sc['w_score'].apply(band)
chg=(sc['b_eq']!=sc['b_w']).sum()
print("Units changing 40/70 band under weighting: %d / %d (%.1f%%)"%(chg,len(sc),100*chg/len(sc)))
print("Mean abs score shift: %.2f pts"%(sc['score']-sc['w_score']).abs().mean())

print("\n"+"="*70)
print("A2. COMPLETENESS TARGET SENSITIVITY (60/70/80%)")
for t in [60,70,80]:
    comp=(sc['score']>=t).sum(); dev=((sc['score']>=40)&(sc['score']<t)).sum(); inc=(sc['score']<40).sum()
    print("  target %d%%: complete=%d developing=%d incomplete=%d"%(t,comp,dev,inc))

print("\n"+"="*70)
print("A3. MILIEU DENSITY-CUTOFF SENSITIVITY (#units changing milieu type)")
base=sc['milieu'].copy()
for lo,hi,lbl in [(8,80,'-20%'),(12,120,'+20%')]:
    alt=sc['densite'].apply(lambda dn: 'dense' if dn>=hi else ('inter' if dn>=lo else 'rural'))
    print("  cutoffs (%d,%d) [%s]: %d / %d change milieu"%(lo,hi,lbl,(alt!=base).sum(),len(sc)))

print("\n"+"="*70)
print("B. KRUSKAL-WALLIS across milieu types (composite)")
groups=[sc[sc['milieu']==m]['score'].values for m in ['dense','inter','rural']]
H,p=stats.kruskal(*groups)
N=len(sc); k=3
eps2=(H-k+1)/(N-k)
print("  H=%.3f  df=%d  p=%.4f  epsilon^2=%.3f"%(H,k-1,p,eps2))
print("  -> %s difference"%("SIGNIFICANT" if p<0.05 else "NO significant"))

print("\n"+"="*70)
print("C. NORTH-SOUTH GRADIENT (Spearman composite vs latitude)")
rho2,p2=stats.spearmanr(sc['score'],sc['lat'])
print("  rho=%.3f  p=%.4f  (n=%d)  negative rho => scores fall going north"%(rho2,p2,len(sc)))
print("  MRC medians (south->north by latitude):")
mrc=sc.groupby('mrc').agg(n=('score','size'),med=('score','median'),meanlat=('lat','mean')).sort_values('meanlat',ascending=False)
for m,row in mrc.iterrows(): print("   %-22s n=%2d median=%.1f"%(m,row['n'],row['med']))

print("\n"+"="*70)
print("D. WILCOXON paired: municipal vs urban-perimeter (principal PU)")
pu=pd.read_csv('/mnt/user-data/uploads/lacunes_MVC_tous_perimetres__2_.csv')
pu.columns=[c.strip() for c in pu.columns]
pu['Municipalité']=pu['Municipalité'].astype(str).str.strip()
pu['Score %']=pd.to_numeric(pu['Score %'],errors='coerce')
pu['Nb logements']=pd.to_numeric(pu['Nb logements'],errors='coerce')
print("  perimeters in CSV:",len(pu),"| PU score median=%.1f mean=%.1f"%(pu['Score %'].median(),pu['Score %'].mean()))
# principal perimeter per municipality = largest by dwellings
princ=pu.sort_values('Nb logements',ascending=False).groupby('Municipalité',as_index=False).first()
def norm(s): return unicodedata.normalize('NFKD',str(s)).encode('ascii','ignore').decode().lower().strip()
sc['key']=sc['mun'].apply(norm); princ['key']=princ['Municipalité'].apply(norm)
m=sc.merge(princ[['key','Score %','Nb logements']],on='key',how='inner')
print("  matched municipalities with a perimeter:",len(m))
diff=m['Score %']-m['score']
W,pw=stats.wilcoxon(m['Score %'],m['score'])
n=len(m); z=stats.norm.isf(pw/2); r=z/np.sqrt(n)
print("  municipal median=%.1f  PU(principal) median=%.1f"%(m['score'].median(),m['Score %'].median()))
print("  Wilcoxon V=%.1f  p=%.2e  effect r=%.3f  (n=%d pairs)"%(W,pw,r,n))
print("  PU higher in %d/%d pairs; mean gain=%.1f pts"%((diff>0).sum(),n,diff.mean()))

print("\n"+"="*70)
print("E. CORRECTED TABLE 5 — per-parameter (municipal n=78 ; PU n=%d)"%len(pu))
LAB={'pct_alimentation':'Food retail','pct_service_garde':'Childcare','pct_ecole_prim':'Primary school',
'pct_ecole_sec':'Secondary school','pct_nature':'Green/natural','pct_loisirs':'Recreation/sport',
'pct_culture':'Cultural','pct_pharmacie':'Pharmacy','pct_sante':'Healthcare','pct_transport':'Public transit',
'pct_autopartage':'Shared mobility','pct_cyclable':'Cycling'}
pucol={'pct_alimentation':'Alimentation %','pct_service_garde':'Service de garde %','pct_ecole_prim':'École primaire %',
'pct_ecole_sec':'École secondaire %','pct_nature':'Espaces naturels %','pct_loisirs':'Loisirs et sport %',
'pct_culture':'Équipements culturels %','pct_pharmacie':'Pharmacie %','pct_sante':'Soins de santé 1re ligne %',
'pct_transport':'Transport en commun %','pct_autopartage':'Mobilité partagée %','pct_cyclable':'Réseau cyclable %'}
for c in pu.columns: pass
print("%-17s %7s %7s %9s %8s %9s"%("Parameter","MuMean","MuMed","Mu>=70","PUmed","PU>=70"))
for k in PARAMS:
    mm=sc[k].mean(); md=sc[k].median(); mge=(sc[k]>=70).sum()
    pc=pucol[k]; pcol=pd.to_numeric(pu[pc],errors='coerce') if pc in pu.columns else None
    if pcol is not None: pmd=pcol.median(); pge=(pcol>=70).sum()
    else: pmd=float('nan'); pge=-1
    print("%-17s %7.1f %7.0f %6d/78 %8.0f %6d/%d"%(LAB[k],mm,md,mge,pmd,pge,len(pu)))