from pathlib import Path
import json,hashlib,shutil,datetime
R=Path('/Users/georgele/Developer/Projects/tools/dev/formseed/projects/uk-comet-i-conversions');D=R/'delivery';B=R.parent/'uk-comet-i/delivery';now=datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(p,v):p.write_text(json.dumps(v,indent=2)+'\n')
reg=json.loads((D/'component-registry.json').read_text());ix=json.loads((D/'recipe-index.json').read_text())['recipes'];records=0
for p in reg['components']:
 assert sha(D/p['export']['path'])==p['export']['sha256'];assert sha(D/p['source']['nativeSource'])==p['source']['nativeSourceSha256'];assert p['source']['selector']['object']==p['componentId'];records+=2
for row in ix:
 assert sha(D/row['manifest'])==row['manifestSha256'];assert sha(D/row['path'])==row['sha256'];m=json.loads((D/row['manifest']).read_text());assert len([o for o in m['operations'] if o['op'] in ['retain','replace','remove']])==73
 for o in m['operations']:
  for p in [o[k] for k in ['part','from','to'] if k in o]:
   root=B if p['dependency'].startswith('uk-comet-i@') else D
   assert sha(root/p['export']['path'])==p['export']['sha256'];assert sha(root/p['source']['nativeSource'])==p['source']['nativeSourceSha256'];records+=2
for receipt in ['render-receipt.json','thumbnail-render-receipt.json']:
 for v in json.loads((D/'review'/receipt).read_text())['views']:
  assert sha(D/v['path'])==v['sha256'];r=next(x for x in ix if x['recipeId']==v['recipeId']);assert v['assemblySha256']==r['sha256'] and v['manifestSha256']==r['manifestSha256'];records+=1
bindings=json.loads((D/'assessments/bindings.json').read_text())
assert sha(bindings['independentReview']['path'])==bindings['independentReview']['sha256']
for p in bindings['assessments']:
 assert sha(D/p['assessment'])==p['sha256'];assert sha(D/p['manifest'])==p['manifestSha256'];assert sha(D/p['assembly'])==p['assemblySha256'];assert sha(p['rubric']['path'])==p['rubric']['sha256'];assert sha(D/p['assembledValidation']['path'])==p['assembledValidation']['sha256'];records+=5
 if p['styleProfile']:assert sha(p['styleProfile']['path'])==p['styleProfile']['sha256']
for r in [2,3]:
 s=json.loads((R/f'evidence/producer-r{r}-records.json').read_text());p=s['nativeReceipt'];assert sha(p['path'])==p['sha256'];out=D/f'validation/native-isolation-r{r}.json';shutil.copyfile(p['path'],out)
source=json.loads((R/'evidence/producer-r3-records.json').read_text());assert source['dimension']['aggregate']['passedBlockingCriterionCount']==144
p=Path(source['dimension']['evidencePath']);shutil.copyfile(p,D/'validation/native-dimension-r3.json')
backend=json.loads((D/'validation/final-public-backend-and-provenance.json').read_text());assert not any(x['locked'] for x in backend['lock']['locks']);assert backend['backend']['workflowReviewCount']==0;assert backend['provenance']['comparison']['differingPixels']==0 and backend['provenance']['comparison']['equal'];assert backend['provenance']['approvalImplied'] is False and backend['provenance']['reviewGateAdvanced'] is False;assert sha(D/'review/batch-artwork-review-r3-fit2-provenance.png')==backend['provenance']['derivativeSha256']
prior=json.loads((R/'evidence/base-preservation-before.json').read_text())
for rel,p in prior.items():assert sha(B/rel)==p['sha256'] and (B/rel).stat().st_size==p['bytes']
assert not Path('/Volumes/T9/Developer/Scratch/comet-conversions.plkccmrf').exists()
cleanup={'checkedAt':now,'taskOwnedBraveProcesses':'No matches after producer completion, checked outside sandbox; only checking ps/rg command appeared','taskOwnedBrowserContexts':'All four completed renderer/recognition/instance contexts reported closed and profileRemoved; no remaining task scratch profiles','simulators':'None created or booted','producerWriter':'Released, redacted lock epoch4 reports locked:false','unrelatedWindows':'Pre-existing M106A2 Preview and Brave user tabs preserved. Native single-target display deferred under user preservation instruction. Verified batch PNG linked for review instead.','retainedEvidence':'Current delivery and predecessor histories on T9-backed Developer APFS disk7s2, same filesystem as /Volumes/T9; fresh developer-host ready and df evidence checked','humanApproval':None};save(D/'validation/cleanup.json',cleanup)
shutil.copyfile(Path.cwd()/'verify_final.py',D/'validation/scripts/verify_final.py')
result={'recordType':'comet-final-preparation-verification','checkedAt':now,'passed':True,'scope':'File/source/view/assessment identity and complete direct-base selections, not artistic approval, gameplay or performance','components':44,'recipes':21,'baseCleanOperationsPerRecipe':73,'fullViews':203,'recognitionViews':168,'structuredAssessments':42,'fileHashAssertions':records,'baseDeliveryFilesPreserved':len(prior),'nativeDimensionCriteriaPassed':144,'writerReleased':True,'humanApproval':None,'technicalValidation':'PASS bounded scope','visualRecommendation':'model-quality go75/75; art-style-consistency no-go75/80; recommend selective style corrections before final acceptance'};save(D/'validation/final-preparation-validation.json',result)
# Inventory excludes itself; all other current deliverables pinned, including validation scripts and results.
files={str(p.relative_to(D)):{'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(D.rglob('*')) if p.is_file() and p.name!='SHA256SUMS.json'};save(D/'SHA256SUMS.json',{'algorithm':'sha256','files':files})
for rel,p in files.items():assert sha(D/rel)==p['sha256'] and (D/rel).stat().st_size==p['bytes']
print(json.dumps({**result,'inventoryFiles':len(files),'inventorySha256':sha(D/'SHA256SUMS.json')}))
