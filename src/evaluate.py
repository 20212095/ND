"""Paired zero-shot/RAG evaluation. All API failures remain in denominators."""
import json
from pathlib import Path
from statistics import mean
from .agent import run_agent

def evaluate(rows, client, model, retriever, api_style='interactions', repeats=1, output_dir=None):
    records=[]
    for repeat in range(repeats):
        for row in rows:
            for mode in ('zero_shot','rag'):
                record={'id':row['id'],'repeat':repeat,'mode':mode,'model':model,
                        'api_style':api_style,'family':row['family'],
                        'expected_issue':row['y']['has_issue'],'expected_type':row['y']['issue_type']}
                try:
                    result=run_agent(row['x'],client,model,mode,retriever,api_style)
                    y=result['y']
                    record.update(schema_valid=True,predicted_issue=y['has_issue'],
                        predicted_type=y['issue_type'],prediction=y,
                        detection_correct=y['has_issue']==row['y']['has_issue'],
                        type_correct=y['issue_type']==row['y']['issue_type'],
                        line_correct=y['line']==row['y']['line'],elapsed_s=result['elapsed_s'])
                except Exception as exc:
                    # Never serialize full API errors which may contain request details.
                    record.update(schema_valid=False,predicted_issue=None,
                        detection_correct=False,type_correct=False,line_correct=False,
                        error_type=type(exc).__name__)
                records.append(record)
    summaries=[]
    for mode in ('zero_shot','rag'):
        part=[r for r in records if r['mode']==mode]
        tp=sum(r['expected_issue'] and r['predicted_issue'] is True for r in part)
        fp=sum(not r['expected_issue'] and r['predicted_issue'] is True for r in part)
        fn=sum(r['expected_issue'] and r['predicted_issue'] is not True for r in part)
        precision=tp/(tp+fp) if tp+fp else 0
        recall=tp/(tp+fn) if tp+fn else 0
        summaries.append({'mode':mode,'n':len(part),
            'valid_output_rate':mean(r['schema_valid'] for r in part),
            'detection_accuracy':mean(r['detection_correct'] for r in part),
            'type_accuracy':mean(r['type_correct'] for r in part),
            'precision':precision,'recall':recall,
            'f1':2*precision*recall/(precision+recall) if precision+recall else 0,
            'mean_valid_elapsed_s':mean([r['elapsed_s'] for r in part if r['schema_valid']])
                if any(r['schema_valid'] for r in part) else None})
    if output_dir:
        import pandas as pd
        path=Path(output_dir); path.mkdir(parents=True,exist_ok=True)
        (path/'evaluation_raw.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
        pd.DataFrame(summaries).to_csv(path/'evaluation_summary.csv',index=False)
    return records,summaries
