import fs from 'node:fs';
import {evaluateCatalogRubricAssessment} from '/Users/georgele/Developer/Projects/tools/dev/formseed-game-assets/packages/mcp-server/src/rubrics.ts';
const G='/Users/georgele/Developer/Projects/tools/dev/formseed-game-assets',D='/Users/georgele/Developer/Projects/tools/dev/formseed/projects/uk-comet-i-conversions/delivery';
const b=JSON.parse(fs.readFileSync(D+'/assessments/bindings.json','utf8'));let results=[];
for(const row of b.assessments){const a=JSON.parse(fs.readFileSync(D+'/'+row.assessment,'utf8'));const {result}=await evaluateCatalogRubricAssessment(G,a);const p=row.assessment.replace('.json','-result.json');fs.writeFileSync(D+'/'+p,JSON.stringify(result,null,2)+'\n');results.push({assessment:row.assessment,resultPath:p,...result});}
fs.writeFileSync(D+'/assessments/evaluation-summary.json',JSON.stringify({authority:'Local deterministic rubric evaluation only; no human approval or backend gate',results},null,2)+'\n');console.log(JSON.stringify({count:results.length,go:results.filter(r=>r.recommendation==='go').length,noGo:results.filter(r=>r.recommendation==='no-go').length}));
