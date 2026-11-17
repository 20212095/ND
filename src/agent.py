"""One orchestrating review agent. Code inputs are treated as data, never run."""
from pathlib import Path
from typing import Literal
import ast
import json
import time
from datetime import datetime, timezone
from pydantic import BaseModel, ConfigDict, Field, model_validator

ROOT=Path(__file__).resolve().parents[1]

class Review(BaseModel):
    model_config=ConfigDict(extra='forbid', strict=True)
    has_issue: bool
    issue_type: Literal['none','security','runtime','correctness','reliability','maintainability']
    severity: Literal['none','low','medium','high','critical']
    line: int | None = Field(ge=1)
    problematic_code: str
    explanation: str
    recommendation: str
    suggested_code: str
    confidence: float = Field(ge=0,le=1)

    @model_validator(mode='after')
    def coherent(self):
        if self.has_issue:
            if self.line is None or self.issue_type=='none' or self.severity=='none' or not self.problematic_code.strip():
                raise ValueError('Problemos įrašui reikia eilutės, tipo, svarbos ir kodo.')
        elif self.issue_type!='none' or self.severity!='none' or self.line is not None or self.problematic_code or self.suggested_code:
            raise ValueError('Kai problemos nėra, tipo ir svarbos reikšmės turi būti none, eilutė null, kodo laukai tušti.')
        return self

def read_rows(name='examples.jsonl'):
    return [json.loads(s) for s in (ROOT/'data'/name).read_text(encoding='utf-8').splitlines() if s.strip()]

def understand(x):
    if x.get('language')!='python' or not x.get('code','').strip():
        raise ValueError('Reikalingas netuščias Python kodas.')
    if not x.get('contract','').strip():
        raise ValueError('Aprašykite tikėtiną kodo elgesį contract lauke.')
    syntax_error=None
    try:
        tree=ast.parse(x['code'])
        functions=[n.name for n in ast.walk(tree) if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))]
    except SyntaxError as e:
        syntax_error={'line':e.lineno,'message':e.msg}
        functions=[]
    return {'line_count':len(x['code'].splitlines()), 'functions':functions,
            'syntax_error':syntax_error, 'code_executed':False}

def build_prompt(x, examples=()):
    template=(ROOT/'prompts/template.txt').read_text(encoding='utf-8')
    context=[{'X':r['x'],'y':r['y']} for r in examples]
    return template.replace('{{EXAMPLES_JSON}}',json.dumps(context,ensure_ascii=False,indent=2)).replace(
        '{{INPUT_JSON}}',json.dumps(x,ensure_ascii=False,indent=2))

def validate_response(text, x):
    y=Review.model_validate_json(text)
    if y.line is not None:
        lines=x['code'].splitlines()
        if y.line>len(lines) or y.problematic_code.strip()!=lines[y.line-1].strip():
            raise ValueError('Atsakymo eilutė arba kodo fragmentas neatitinka įvesties.')
    return y

def generate(client, model, prompt, api_style='interactions'):
    system=(ROOT/'prompts/system.txt').read_text(encoding='utf-8')
    if api_style=='interactions':
        interaction=client.interactions.create(
            model=model, input=prompt, system_instruction=system,
            generation_config={'temperature':0},
            response_format={'type':'text','mime_type':'application/json','schema':Review.model_json_schema()})
        return interaction.output_text
    if api_style=='generate_content':
        from google.genai import types
        response=client.models.generate_content(model=model,contents=prompt,
            config=types.GenerateContentConfig(system_instruction=system,temperature=0,
                response_mime_type='application/json',response_schema=Review))
        return response.text
    raise ValueError('api_style turi būti interactions arba generate_content.')

def run_agent(x, client, model, mode='zero_shot', retriever=None,
              api_style='interactions', log_path=None):
    if mode not in ('zero_shot','few_shot','rag'):
        raise ValueError('Nežinomas režimas.')
    start=time.perf_counter()
    stages=[{'stage':'data_understanding','details':understand(x)}]
    selected=[]
    if mode=='few_shot':
        ids=json.loads((ROOT/'prompts/few_shot_ids.json').read_text())
        by_id={r['id']:r for r in read_rows()}
        selected=[by_id[i] for i in ids]
    elif mode=='rag':
        if retriever is None:
            raise ValueError('RAG režimui būtinas retriever.')
        selected=retriever.retrieve(x,3)
    stages.append({'stage':'context_selection','examples':[{
        'id':r['id'],'distance':r.get('distance')} for r in selected]})
    prompt=build_prompt(x, selected)
    stages.append({'stage':'prompt_preparation','prompt_chars':len(prompt),
                   'public_instruction':'Patikrinti kodą pagal sutartį ir pateikti trumpą išvadą su įrodymu.'})
    raw=generate(client,model,prompt,api_style)
    stages.append({'stage':'inference','model':model,'api_style':api_style})
    if not raw:
        raise ValueError('Modelis nepateikė tekstinio atsakymo; patikrinkite modelį ir atsakymo būseną.')
    y=validate_response(raw,x)
    stages.append({'stage':'output_generation','schema_valid':True})
    result={'timestamp':datetime.now(timezone.utc).isoformat(),'mode':mode,'model':model,
            'api_style':api_style,'x':x,'stages':stages,'prompt':prompt,
            'y':y.model_dump(),'elapsed_s':round(time.perf_counter()-start,3)}
    if log_path:
        path=Path(log_path)
        path.parent.mkdir(parents=True,exist_ok=True)
        with path.open('a',encoding='utf-8') as stream:
            stream.write(json.dumps(result,ensure_ascii=False)+'\n')
    return result
