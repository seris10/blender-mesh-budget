from pathlib import Path
import hashlib, json, subprocess, tempfile
root=Path(__file__).resolve().parents[1]
def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()
with tempfile.TemporaryDirectory(prefix="mesh-check-",dir=root) as folder:
    target=Path(folder)/"reduced.glb"
    base=["blender","--background","--python-exit-code","1","--python",str(root/"mesh_budget.py"),"--","--source",str(root/"examples/synthetic-fish.glb"),"--output",str(target)]
    first=subprocess.run(base+["--triangles","300"],capture_output=True,text=True)
    assert first.returncode==0, first.stdout+first.stderr
    report=json.loads(target.with_suffix(".decimation.json").read_text())
    assert report["final_triangles"]<=300
    before=digest(target)
    rejected=subprocess.run(base+["--triangles","100","--max-surface-error-fraction","0.000001"],capture_output=True,text=True)
    assert rejected.returncode!=0
    assert digest(target)==before
    print(json.dumps({"triangles":report["final_triangles"],"strict_budget_rejected":True,"existing_output_preserved":True}))
