"""Deterministic, synthetic, contract-labelled examples. Never executes snippets."""
from pathlib import Path
import ast
import hashlib
import json

FAMILIES = [
    'mutable_default', 'unsafe_eval', 'unsafe_pickle', 'unsafe_yaml',
    'sql_injection', 'shell_injection', 'missing_timeout', 'broad_exception',
    'resource_leak', 'division_zero', 'off_by_one', 'none_check',
]

def outcome(code, marker=None, issue_type='none', severity='none',
            explanation='Pagal nurodytą sutartį nagrinėjamos problemos nerasta.',
            recommendation='Šiuo aspektu keitimas nereikalingas.', fixed=''):
    line = next((i for i, s in enumerate(code.splitlines(), 1) if marker and marker in s), None)
    return dict(has_issue=marker is not None, issue_type=issue_type,
                severity=severity, line=line,
                problematic_code=code.splitlines()[line-1].strip() if line else '',
                explanation=explanation, recommendation=recommendation,
                suggested_code=fixed if marker else '', confidence=1.0)

def example(family, i, buggy):
    f, v = f'review_{family}_{i}', f'value_{i}'
    suffix = f'\n# Scenario {i}: {family}\n'
    if family == 'mutable_default':
        contract = 'Kiekvienas kvietimas be bucket argumento turi gauti atskirą sąrašą.'
        bad = f'def {f}({v}, bucket=[]):\n    bucket.append({v})\n    return bucket\n'
        good = f'def {f}({v}, bucket=None):\n    if bucket is None:\n        bucket = []\n    bucket.append({v})\n    return bucket\n'
        marker, kind, sev = 'bucket=[]', 'correctness', 'medium'
        why, rec = 'Numatytasis sąrašas bendras keliems funkcijos kvietimams.', 'Naudoti None ir kiekvienam kvietimui sukurti sąrašą.'
    elif family == 'unsafe_eval':
        contract = 'Tekstas gaunamas iš nepatikimo naudotojo ir turi būti JSON duomenys.'
        bad = f'def {f}({v}):\n    return eval({v})\n'
        good = f'import json\ndef {f}({v}):\n    return json.loads({v})\n'
        marker, kind, sev = 'eval(', 'security', 'critical'
        why, rec = 'eval gali vykdyti nepatikimame tekste esantį Python kodą.', 'JSON duomenis apdoroti su json.loads.'
    elif family == 'unsafe_pickle':
        contract = 'Baitai gaunami iš nepatikimo tinklo kliento; leidžiami tik UTF-8 JSON duomenys.'
        bad = f'import pickle\ndef {f}({v}):\n    return pickle.loads({v})\n'
        good = f'import json\ndef {f}({v}):\n    return json.loads({v}.decode("utf-8"))\n'
        marker, kind, sev = 'pickle.loads', 'security', 'critical'
        why, rec = 'Nepatikimų pickle duomenų iškodavimas gali vykdyti kodą.', 'Naudoti duomenų formatą, kuris nevykdo Python objektų atkūrimo kodo.'
    elif family == 'unsafe_yaml':
        contract = 'YAML konfigūracija gaunama iš nepatikimo naudotojo; Python objektai neleidžiami.'
        bad = f'import yaml\ndef {f}({v}):\n    return yaml.load({v}, Loader=yaml.UnsafeLoader)\n'
        good = f'import yaml\ndef {f}({v}):\n    return yaml.safe_load({v})\n'
        marker, kind, sev = 'yaml.load(', 'security', 'critical'
        why, rec = 'UnsafeLoader leidžia nesaugią Python objektų deserializaciją.', 'Naudoti yaml.safe_load.'
    elif family == 'sql_injection':
        contract = 'name yra nepatikima įvestis; conn yra sqlite3 jungtis; ieškoma pagal tikslų vardą.'
        bad = f'def {f}(conn, name):\n    return conn.execute(f"SELECT id FROM users WHERE name = \'{{name}}\'").fetchall()\n'
        good = f'def {f}(conn, name):\n    return conn.execute("SELECT id FROM users WHERE name = ?", (name,)).fetchall()\n'
        marker, kind, sev = 'conn.execute(f', 'security', 'high'
        why, rec = 'Į SQL eilutę tiesiogiai įterpiama nepatikima reikšmė.', 'Naudoti sqlite3 parametrizuotą užklausą su ? žymekliu.'
    elif family == 'shell_injection':
        contract = 'target yra naudotojo įvestas failo kelias; reikia jį tiksliai perduoti ls, be shell interpretavimo.'
        bad = f'import subprocess\ndef {f}(target):\n    return subprocess.run("ls -- " + target, shell=True, check=True)\n'
        good = f'import subprocess\ndef {f}(target):\n    return subprocess.run(["ls", "--", target], check=True)\n'
        marker, kind, sev = 'shell=True', 'security', 'high'
        why, rec = 'Komandų interpretatorius apdoros nepatikimą įvestį kaip komandos dalį.', 'Perduoti argumentų sąrašą ir nenaudoti shell=True.'
    elif family == 'missing_timeout':
        contract = 'url yra patikimas; HTTP užklausa turi turėti aiškų 5 sekundžių prisijungimo ir skaitymo timeout.'
        bad = f'import requests\ndef {f}(url):\n    return requests.get(url).text\n'
        good = f'import requests\ndef {f}(url):\n    return requests.get(url, timeout=5).text\n'
        marker, kind, sev = 'requests.get(url)', 'reliability', 'medium'
        why, rec = 'Be timeout užklausa gali laukti neapibrėžtai ilgai.', 'Pridėti timeout=5; tai nėra bendros visos užklausos trukmės garantija.'
    elif family == 'broad_exception':
        contract = 'Konvertuoti eilutę į int; ValueError atveju grąžinti 0; kitų išimčių neslėpti.'
        bad = f'def {f}({v}):\n    try:\n        return int({v})\n    except Exception:\n        return 0\n'
        good = f'def {f}({v}):\n    try:\n        return int({v})\n    except ValueError:\n        return 0\n'
        marker, kind, sev = 'except Exception', 'reliability', 'medium'
        why, rec = 'Per platus išimties gaudymas slepia ir sutartyje nenumatytas klaidas.', 'Gaudyti tik ValueError.'
    elif family == 'resource_leak':
        contract = 'path yra patikimas; perskaityti UTF-8 failą ir garantuotai uždaryti jį, net įvykus išimčiai.'
        bad = f'def {f}(path):\n    stream = open(path, encoding="utf-8")\n    return stream.read()\n'
        good = f'def {f}(path):\n    with open(path, encoding="utf-8") as stream:\n        return stream.read()\n'
        marker, kind, sev = 'stream = open', 'reliability', 'medium'
        why, rec = 'Nėra aiškiai garantuoto failo uždarymo.', 'Naudoti with kontekstinį valdiklį.'
    elif family == 'division_zero':
        contract = 'a ir b yra skaičiai; kai b lygu 0, grąžinti None, kitu atveju a / b.'
        bad = f'def {f}(a, b):\n    return a / b\n'
        good = f'def {f}(a, b):\n    if b == 0:\n        return None\n    return a / b\n'
        marker, kind, sev = 'return a / b', 'runtime', 'high'
        why, rec = 'Kai b lygu 0, bus išmesta ZeroDivisionError.', 'Prieš dalybą patikrinti b ir grąžinti None, kai jis lygus nuliui.'
    elif family == 'off_by_one':
        contract = 'n yra neneigiamas int; grąžinti visus sveikus skaičius nuo 0 iki n imtinai.'
        bad = f'def {f}(n):\n    return list(range(n))\n'
        good = f'def {f}(n):\n    return list(range(n + 1))\n'
        marker, kind, sev = 'range(n)', 'correctness', 'medium'
        why, rec = 'range(n) neįtraukia n, nors sutartis to reikalauja.', 'Naudoti range(n + 1).'
    elif family == 'none_check':
        contract = 'Numatytą reikšmę 10 naudoti tik kai argumentas yra None; 0 turi likti 0.'
        bad = f'def {f}({v}):\n    if not {v}:\n        return 10\n    return {v}\n'
        good = f'def {f}({v}):\n    if {v} is None:\n        return 10\n    return {v}\n'
        marker, kind, sev = f'if not {v}', 'correctness', 'medium'
        why, rec = 'Bendras loginis tikrinimas atmeta ir teisėtą nulinę reikšmę.', 'Tikrinti is None.'
    else:
        raise ValueError(family)
    code = (bad if buggy else good) + suffix
    y = outcome(code, marker, kind, sev, why, rec, good) if buggy else outcome(code)
    return dict(id=f'{family}-{i:03d}-'+('issue' if buggy else 'clean'),
                family=family, source='synthetic_template', template_variant=i,
                x=dict(language='python', code=code, contract=contract), y=y)

def create_dataset():
    return [example(family, i, buggy) for family in FAMILIES
            for i in range(50) for buggy in (False, True)]

def create_holdout():
    # Different wrappers and parameter names; same issue families. This is a
    # demonstration holdout, not proof of generalization to unseen projects.
    rows = []
    for family in FAMILIES:
        for buggy in (False, True):
            base = example(family, 9876, buggy)
            lines = base['x']['code'].splitlines()
            lines = [s for s in lines if not s.startswith('# Scenario')]
            renamed = '\n'.join(lines).replace('review_'+family+'_9876', 'inspect_payload').replace('value_9876', 'payload')
            imports = [s for s in renamed.splitlines() if s.startswith('import ')]
            body = [s for s in renamed.splitlines() if not s.startswith('import ')]
            code = '\n'.join(imports + ['class ReviewService:', '    @staticmethod'] + ['    '+s for s in body])+'\n'
            y = base['y'].copy()
            if buggy:
                original = base['x']['code'].splitlines()[y['line']-1].strip().replace('value_9876','payload').replace('review_'+family+'_9876', 'inspect_payload')
                y['line'] = next(i for i,s in enumerate(code.splitlines(),1) if s.strip()==original)
                y['problematic_code'] = original
                fixed = base['y']['suggested_code'].replace('review_'+family+'_9876', 'inspect_payload').replace('value_9876','payload')
                fi=[s for s in fixed.splitlines() if s.startswith('import ')]
                fb=[s for s in fixed.splitlines() if not s.startswith('import ')]
                y['suggested_code']='\n'.join(fi+['class ReviewService:', '    @staticmethod']+['    '+s for s in fb])+'\n'
            rows.append(dict(id=f'holdout-{family}-'+('issue' if buggy else 'clean'),
                        family=family, source='synthetic_holdout',
                        x={**base['x'], 'code':code}, y=y))
    return rows

def validate_rows(rows):
    hashes = set()
    for row in rows:
        code, y = row['x']['code'], row['y']
        ast.parse(code)
        if y['suggested_code']:
            ast.parse(y['suggested_code'])
        fingerprint = hashlib.sha256(code.encode()).hexdigest()
        assert fingerprint not in hashes, row['id']
        hashes.add(fingerprint)
        if y['has_issue']:
            assert code.splitlines()[y['line']-1].strip() == y['problematic_code']
        else:
            assert y['line'] is None and y['issue_type']=='none'
    return hashes

def save(path):
    path=Path(path)
    path.mkdir(parents=True, exist_ok=True)
    rows, test=create_dataset(), create_holdout()
    a,b=validate_rows(rows),validate_rows(test)
    assert a.isdisjoint(b)
    for name, content in [('examples.jsonl',rows),('holdout.jsonl',test)]:
        (path/name).write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in content),encoding='utf-8')
    return rows,test

if __name__=='__main__':
    import sys
    save(Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parents[1]/'data')
