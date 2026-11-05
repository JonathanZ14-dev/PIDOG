"""Run: python3 check_exercises.py --student. TODOs fail until you complete them."""
import argparse
import importlib


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--student',action='store_true',help='Check your work in exercises/student.py')
    args=p.parse_args()
    m=importlib.import_module('exercises.student')
    cases=[('flat_index',(2,1,4),6),('flat_index',(0,0,4),0),
           ('marker_fraction',(3,12),.25),('marker_fraction',(0,8),0),
           ('marker_status',(.08,.5),'marker_present'),('marker_status',(.5,.05),'unknown'),
           ('marker_status',(.01,.5),'marker_absent')]
    for v in ('clear','blocked','unknown'):
        for s in ('clear','blocked','unknown'):
            expected='blocked' if 'blocked' in (v,s) else ('clear' if v==s=='clear' else 'unknown')
            cases.append(('fuse_evidence',(v,s),expected))
    failed=0
    for name,inputs,expected in cases:
        try:
            result=getattr(m,name)(*inputs)
            assert result==expected, f'{result!r} != {expected!r}'
            print('PASS',name,inputs)
        except Exception as e:
            failed+=1;print('FAIL',name,inputs,type(e).__name__,str(e))
    for inputs in ((1,0),(-1,4),(5,4)):
        try:
            m.marker_fraction(*inputs)
        except ValueError:
            print('PASS rejected',inputs)
        except Exception as e:
            failed+=1;print('FAIL expected ValueError:',type(e).__name__)
        else:
            failed+=1;print('FAIL accepted invalid counts',inputs)
    print('Failures:',failed)
    raise SystemExit(1 if failed else 0)


if __name__=='__main__':main()
