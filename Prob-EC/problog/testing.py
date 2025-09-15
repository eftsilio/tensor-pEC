from problog.program import PrologFile, PrologString
from problog.formula import LogicFormula
from problog.sdd_formula import SDD
from problog import get_evaluatable
from problog.engine import DefaultEngine


def main():

	engine = DefaultEngine()	

	f='/media/eftsilio/My_Data/oPIEC/probres/lib/python3.12/site-packages/problog/jonathan.pl'
	f2='/media/eftsilio/My_Data/oPIEC/probres/lib/python3.12/site-packages/problog/jonathan2.pl'
	program = PrologFile(f)
	db = engine.prepare(program)

	formula = LogicFormula.create_from(db)
	print(formula._nodes, formula._names)
	sdd = SDD.create_from(formula)
	print(sdd.evaluate())

	m2 = ''
	m2 += '0.3::happensAt(rain(id1), 1).\n'
	m2 += '0.3::happensAt(wind(id1), 1).\n'
	m2 = '\n' + m2 + '\n'
	
	m3 = """
query(raincoat(id1, T)).
query(raincoat(id4, T)).
"""
	
	db2 = db.extend()
	for statement in PrologString(m2):
		print(statement)
		db2 += statement

	for statement in PrologString(m3):
		db2 += statement

	formula2 = LogicFormula.create_from(db2)
	print('\n\n', formula2._nodes, '\n\n', formula2._names)	
	sdd = SDD.create_from(formula2)
	result = sdd.evaluate()
	for r in result:
		print(r, result[r])
	#p = formula.get_next_atom_identifier()
	#formula.add_atom(p, 0.5, name='wind(id1)')
	#print(formula._nodes, formula._names)
	#p = formula.get_next_atom_identifier()
	#formula.add_query('raincoat(id1)', 2)
	#print(formula._nodes, formula._names)
	#sdd = SDD.create_from(formula)
	#print(sdd.evaluate())


if __name__ == "__main__":
	main()

