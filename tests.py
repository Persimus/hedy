import unittest
import hedy
import sys
import io
from contextlib import contextmanager

#this code let's us capture std out to also execute the generated Python
# and check its output
@contextmanager
def captured_output():
    new_out, new_err = io.StringIO(), io.StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err

def run_code(code):
    with captured_output() as (out, err):
        exec(code)
    return out.getvalue().strip()

class TestsLevel1(unittest.TestCase):

    def test_transpile_other(self):
        with self.assertRaises(Exception) as context:
            result = hedy.transpile("abc felienne 123", 1)
        self.assertEqual(str(context.exception), 'Invalid')

    def test_transpile_print(self):
        result = hedy.transpile("print Hallo welkom bij Hedy!", 1)
        self.assertEqual(result, "print('Hallo welkom bij Hedy!')")
        self.assertEqual(run_code(result), 'Hallo welkom bij Hedy!')

    def test_transpile_ask_Spanish(self):
        result = hedy.transpile("ask ask Cuál es tu color favorito?", 1)
        self.assertEqual(result, "answer = input('ask Cuál es tu color favorito?')")

    def test_lines_may_end_in_spaces(self):
        result = hedy.transpile("print Hallo welkom bij Hedy! ", 1)
        self.assertEqual(result, "print('Hallo welkom bij Hedy!')")
        self.assertEqual(run_code(result), 'Hallo welkom bij Hedy!')

    def test_transpile_empty(self):
        with self.assertRaises(hedy.HedyException) as context:
            result = hedy.transpile("", 1)

    def test_transpile_ask(self):
        result = hedy.transpile("ask wat is je lievelingskleur?", 1)
        self.assertEqual(result, "answer = input('wat is je lievelingskleur?')")

    def test_transpile_print_multiple_lines(self):
        result = hedy.transpile("print Hallo welkom bij Hedy\nprint Mooi hoor", 1)
        self.assertEqual(result, "print('Hallo welkom bij Hedy')\nprint('Mooi hoor')")

    def test_transpile_three_lines(self):
        input = """print Hallo
ask Wat is je lievelingskleur
echo je lievelingskleur is"""
        result = hedy.transpile(input, 1)
        self.assertEqual(result, "print('Hallo')\nanswer = input('Wat is je lievelingskleur')\nprint('je lievelingskleur is' + answer)")

    def test_transpile_echo(self):
        result = hedy.transpile("echo Jouw lievelingskleur is dus...", 1)
        self.assertEqual(result, "print('Jouw lievelingskleur is dus...' + answer)")

class TestsLevel2(unittest.TestCase):

    # some commands should not change:
    def test_transpile_other(self):
        with self.assertRaises(Exception) as context:
            result = hedy.transpile("abc felienne 123", 2)
        self.assertEqual(str(context.exception), 'Invalid')

    def test_transpile_ask_Spanish(self):
        result = hedy.transpile("ask ask Cuál es tu color favorito?", 2)
        self.assertEqual(result, "answer = input('ask Cuál es tu color favorito?')")


    def test_transpile_print(self):
        result = hedy.transpile("print Hallo welkom bij Hedy!", 2)
        self.assertEqual(result, "import random\nprint('Hallo'+' '+'welkom'+' '+'bij'+' '+'Hedy'+'!')")

    def test_transpile_ask(self):
        result = hedy.transpile("kleur is ask wat is je lievelingskleur?", 2)
        self.assertEqual(result, "import random\nkleur = input('wat is je lievelingskleur'+'?')")

    def test_transpile_ask_Spanish(self):
        result = hedy.transpile("color is ask ask Cuál es tu color favorito?", 2)
        self.assertEqual(result, "import random\ncolor = input('ask Cuál es tu color favorito'+'?')")

    def test_transpile_ask_with_print(self):
        result = hedy.transpile("kleur is ask wat is je lievelingskleur?\nprint kleur!", 2)
        self.assertEqual(result, "import random\nkleur = input('wat is je lievelingskleur'+'?')\nprint(kleur+'!')")


    def test_transpile_print_multiple_lines(self):
        result = hedy.transpile("print Hallo welkom bij Hedy!\nprint Mooi hoor", 2)
        self.assertEqual(result, "import random\nprint('Hallo'+' '+'welkom'+' '+'bij'+' '+'Hedy'+'!')\nprint('Mooi'+' '+'hoor')")
        self.assertEqual(run_code(result), "Hallo welkom bij Hedy!\nMooi hoor")

    def test_transpile_assign(self):
        result = hedy.transpile("naam is Felienne", 2)
        self.assertEqual(result, "import random\nnaam = 'Felienne'")

    def test_transpile_assign_2_integer(self):
        result = hedy.transpile("naam is 14", 2)
        self.assertEqual(result, "import random\nnaam = '14'")

    def test_transpile_assign_and_print(self):
        result = hedy.transpile("naam is Felienne\nprint naam", 2)
        self.assertEqual(result, "import random\nnaam = 'Felienne'\nprint(naam)")

    def test_transpile_assign_and_print_more_words(self):
        result = hedy.transpile("naam is Felienne\nprint hallo naam", 2)
        self.assertEqual(result, "import random\nnaam = 'Felienne'\nprint('hallo'+' '+naam)")

    def test_transpile_assign_and_print_punctuation(self):
        result = hedy.transpile("naam is Hedy\nprint Hallo naam!", 2)
        self.assertEqual(result, "import random\nnaam = 'Hedy'\nprint('Hallo'+' '+naam+'!')")

    def test_transpile_assign_and_print_in_sentence(self):
        result = hedy.transpile("naam is Hedy\nprint naam is jouw voornaam", 2)
        self.assertEqual(result, "import random\nnaam = 'Hedy'\nprint(naam+' '+'is'+' '+'jouw'+' '+'voornaam')")

    def test_transpile_assign_and_print_something_else(self):
        result = hedy.transpile("naam is Felienne\nprint Hallo", 2)
        self.assertEqual(result, "import random\nnaam = 'Felienne'\nprint('Hallo')")

    def test_set_list_var(self):
        result = hedy.transpile("dieren is Hond, Kat, Kangoeroe", 2)
        self.assertEqual(result, "import random\ndieren = ['Hond', 'Kat', 'Kangoeroe']")

    def test_print_with_list_var(self):
        result = hedy.transpile("dieren is Hond, Kat, Kangoeroe\nprint dieren at 1", 2)
        self.assertEqual(result, "import random\ndieren = ['Hond', 'Kat', 'Kangoeroe']\nprint(dieren[1])")
        self.assertEqual(run_code(result), "Kat")


    def test_print_with_list_var_random(self):
        result = hedy.transpile("dieren is Hond, Kat, Kangoeroe\nprint dieren at random", 2)
        self.assertEqual(result, "import random\ndieren = ['Hond', 'Kat', 'Kangoeroe']\nprint(random.choice(dieren))")
        self.assertIn(run_code(result), ['Hond', 'Kat', 'Kangoeroe'])

class TestsLevel3(unittest.TestCase):
    def test_transpile_other(self):
        with self.assertRaises(Exception) as context:
            result = hedy.transpile("abc felienne 123", 3)
        self.assertEqual(str(context.exception), 'Invalid')

    def test_transpile_print_level_2(self):
        with self.assertRaises(Exception) as context:
            result = hedy.transpile("print felienne 123", 3)
            self.assertEqual(str(context), 'First word is not a command') #hier moet nog we een andere foutmelding komen!

    def test_print(self):
        result = hedy.transpile("print 'hallo wereld!'", 3)
        self.assertEqual(result, "import random\nprint('hallo wereld!')")

    def test_print_with_comma(self):
        result = hedy.transpile("naam is Hedy\nprint 'ik heet ,'",3)
        self.assertEqual(result, "import random\nnaam = 'Hedy'\nprint('ik heet ,')")

    def test_print_with_single_quote(self):
        result = hedy.transpile("naam is Hedy\nprint 'ik heet \\''",3)
        self.assertEqual(result, "import random\nnaam = 'Hedy'\nprint('ik heet \\'')")

    def test_name_with_underscore(self):
        result = hedy.transpile("voor_naam is Hedy\nprint 'ik heet \\''",3)
        self.assertEqual(result, "import random\nvoor_naam = 'Hedy'\nprint('ik heet \\'')")


    def test_print_Spanish(self):
        result = hedy.transpile("print 'Cuál es tu color favorito?'", 3)
        self.assertEqual(result, "import random\nprint('Cuál es tu color favorito?')")

    def test_print_with_list_var(self):
        result = hedy.transpile("dieren is Hond, Kat, Kangoeroe\nprint dieren at 1", 3)
        self.assertEqual(result, "import random\ndieren = ['Hond', 'Kat', 'Kangoeroe']\nprint(dieren[1])")
        self.assertEqual(run_code(result), "Kat")

    def test_print_with_list_var_random(self):
        result = hedy.transpile("dieren is Hond, Kat, Kangoeroe\nprint dieren at random", 3)
        self.assertEqual(result, "import random\ndieren = ['Hond', 'Kat', 'Kangoeroe']\nprint(random.choice(dieren))")
        self.assertIn(run_code(result), ['Hond', 'Kat', 'Kangoeroe'])


    def test_transpile_ask_Spanish(self):
        result = hedy.transpile("color is ask Cuál es tu color favorito?", 3)
        self.assertEqual(result, "import random\ncolor = input('Cuál es tu color favorito?')")

    def test_print_2(self):
        result = hedy.transpile("print 'ik heet henk'", 3)
        self.assertEqual(result, """import random
print('ik heet henk')""")

    def test_print_with_var(self):
        result = hedy.transpile("naam is Hedy\nprint 'ik heet' naam", 3)
        self.assertEqual(result, "import random\nnaam = 'Hedy'\nprint('ik heet'+naam)")

    def test_transpile_ask_with_print(self):
        result = hedy.transpile("kleur is ask wat is je lievelingskleur?\nprint 'jouw lievelingskleur is dus' kleur '!'", 3)
        self.assertEqual(result, "import random\nkleur = input('wat is je lievelingskleur?')\nprint('jouw lievelingskleur is dus'+kleur+'!')")


class TestsLevel4(unittest.TestCase):
    #ask and print should still work as in level 4
    def test_print_with_var(self):
        result = hedy.transpile("naam is Hedy\nprint 'ik heet' naam", 4)
        self.assertEqual(result, "import random\nnaam = 'Hedy'\nprint('ik heet'+naam)")

    def test_print_with_comma(self):
        result = hedy.transpile("naam is Hedy\nprint 'ik heet,' naam", 4)
        self.assertEqual(result, "import random\nnaam = 'Hedy'\nprint('ik heet,'+naam)")



    def test_transpile_ask_with_print(self):
        result = hedy.transpile("kleur is ask wat is je lievelingskleur?\nprint 'jouw lievelingskleur is dus' kleur '!'", 4)
        self.assertEqual(result, "import random\nkleur = input('wat is je lievelingskleur'+'?')\nprint('jouw lievelingskleur is dus'+kleur+'!')")

    def test_transpile_ask_Spanish(self):
        result = hedy.transpile("color is ask Cuál es tu color favorito?", 4)
        self.assertEqual(result, "import random\ncolor = input('Cuál es tu color favorito'+'?')")

    def test_save_list_access_to_var(self):
        result = hedy.transpile("dieren is Hond, Kat, Kangoeroe\ndier is dieren at random\nprint dier", 4)
        self.assertEqual(result, "import random\ndieren = ['Hond', 'Kat', 'Kangoeroe']\ndier=random.choice(dieren)\nprint(dier)")
        self.assertIn(run_code(result), ['Hond', 'Kat', 'Kangoeroe'])

    def test_print_Spanish(self):
        result = hedy.transpile("print 'Cuál es tu color favorito?'", 4)
        self.assertEqual(result, "import random\nprint('Cuál es tu color favorito?')")

    #now adds if
    def test_print_if_else(self):
        result = hedy.transpile("""naam is Hedy
print 'ik heet' naam
if naam is Hedy print 'leuk' else print 'minder leuk'""", 4)

        expected_result = """import random
naam = 'Hedy'
print('ik heet'+naam)
if naam == 'Hedy':
  print('leuk')
else:
  print('minder leuk')"""
        self.assertEqual(expected_result, result)

    def test_print_if_else_with_ask(self):
        result = hedy.transpile("""kleur is ask Wat is je lievelingskleur?
if kleur is groen print 'mooi!' else print 'niet zo mooi'""", 4)

        expected_result = """import random
kleur = input('Wat is je lievelingskleur?')
if kleur == 'groen':
  print('mooi!')
else:
  print('niet zo mooi')"""

        self.assertEqual(expected_result, result)

    #steen schaar papier
    def test_print_if_else_with_ask(self):
        result = hedy.transpile("""jouwkeuze is steen
computerkeuze is schaar
if computerkeuze is schaar and jouwkeuze is steen print 'jij wint'""", 4)

        expected_result = """import random
jouwkeuze = 'steen'
computerkeuze = 'schaar'
if computerkeuze == 'schaar' and jouwkeuze == 'steen':
  print('jij wint')"""
        self.assertEqual(expected_result, result)
        self.assertEqual(run_code(result),'jij wint')

    def test_print_if_with_var(self):
        result = hedy.transpile("""jouwkeuze is schaar
computerkeuze is schaar
if computerkeuze is jouwkeuze print 'gelijkspel!'""", 4)

        expected_result = """import random
jouwkeuze = 'schaar'
computerkeuze = 'schaar'
if computerkeuze == jouwkeuze:
  print('gelijkspel!')"""
        self.assertEqual(expected_result, result)
        self.assertEqual(run_code(result),'gelijkspel!')

class TestsLevel5(unittest.TestCase):
    #print should still work
    def test_print_with_var(self):
        result = hedy.transpile("naam is Hedy\nprint 'ik heet' naam", 5)
        self.assertEqual(result, "import random\nnaam = 'Hedy'\nprint('ik heet'+naam)")

    def test_print_with_comma(self):
        result = hedy.transpile("naam is Hedy\nprint 'ik heet,' naam", 5)
        self.assertEqual(result, "import random\nnaam = 'Hedy'\nprint('ik heet,'+naam)")

    def test_print_Spanish(self):
        result = hedy.transpile("print 'Cuál es tu color favorito?'", 5)
        self.assertEqual(result, "import random\nprint('Cuál es tu color favorito?')")

    def test_transpile_ask_Spanish(self):
        result = hedy.transpile("color is ask Cuál es tu color favorito?", 5)
        self.assertEqual(result, "import random\ncolor = input('Cuál es tu color favorito'+'?')")

    #todo: a few more things repeated from 4 here?

    #now add repeat
    def test_repeat_basic_print(self):
        result = hedy.transpile("repeat 5 times print 'me wants a cookie!'", 5)
        self.assertEqual(result, """import random
for i in range(5):
  print('me wants a cookie!')""")
        self.assertEqual(run_code(result),'me wants a cookie!\nme wants a cookie!\nme wants a cookie!\nme wants a cookie!\nme wants a cookie!')

    def test_repeat_nested_in_if(self):
        result = hedy.transpile("kleur is ask Wat is je lievelingskleur?\nif kleur is groen repeat 3 times print 'mooi!'", 5)
        self.assertEqual(result, """import random
kleur = input('Wat is je lievelingskleur'+'?')
if kleur == 'groen':
  for i in range(3):
    print('mooi!')""")

    def test_repeat_over_9_times(self):
        result = hedy.transpile("repeat 10 times print 'me wants a cookie!'", 5)
        self.assertEqual(result, """import random
for i in range(10):
  print('me wants a cookie!')""")
        self.assertEqual(run_code(result),'me wants a cookie!\nme wants a cookie!\nme wants a cookie!\nme wants a cookie!\nme wants a cookie!\nme wants a cookie!\nme wants a cookie!\nme wants a cookie!\nme wants a cookie!\nme wants a cookie!')

class TestsLevel6(unittest.TestCase):
    def test_print_with_var(self):
        result = hedy.transpile("naam is Hedy\nprint 'ik heet' naam", 6)
        self.assertEqual("import random\nnaam = 'Hedy'\nprint('ik heet'+str(naam))",result)

    def test_repeat_nested_in_if(self):
            result = hedy.transpile("kleur is ask Wat is je lievelingskleur?\nif kleur is groen repeat 3 times print 'mooi!'", 6)
            self.assertEqual(result, """import random
kleur = input('Wat is je lievelingskleur'+'?')
if str(kleur) == str('groen'):
  for i in range(3):
    print('mooi!')""")

    #new tests for calculations
    def test_simple_calculation(self):
        result = hedy.transpile("nummer is 4 + 5", 6)
        self.assertEqual('import random\nnummer = int(4) + int(5)', result)

    def test_calculation_and_printing(self):
        result = hedy.transpile("nummer is 4 + 5\nprint nummer", 6)
        self.assertEqual('import random\nnummer = int(4) + int(5)\nprint(str(nummer))', result)
        self.assertEqual(run_code(result), "9")

    def test_calculation_with_vars(self):
        result = hedy.transpile("""nummer is 5
nummertwee is 6
getal is nummer * nummertwee
print getal""", 6)
        self.assertEqual("""import random
nummer = '5'
nummertwee = '6'
getal = int(nummer) * int(nummertwee)
print(str(getal))""", result)
        self.assertEqual(run_code(result), "30")

    def test_print_calculation_directly(self):
        result = hedy.transpile("""nummer is 5
nummertwee is 6
print nummer * nummertwee""", 6)
        self.assertEqual("""import random
nummer = '5'
nummertwee = '6'
print(str(int(nummer) * int(nummertwee)))""", result)
        self.assertEqual(run_code(result), "30")


# class TestsLevel7(unittest.TestCase):
#     def test_print(self):
#         result = hedy.transpile("print 'ik heet'", 7)
#         self.assertEqual("import random\nprint('ik heet')",result)
#
#     def test_print_with_var(self):
#         result = hedy.transpile("naam is Hedy\nprint 'ik heet' naam", 7)
#         self.assertEqual("import random\nnaam = 'Hedy'\nprint('ik heet'+str(naam))",result)
#
#     def test_if_with_indent(self):
#         result = hedy.transpile("""if naam is Hedy
#     print 'koekoek'""", 7)
#         self.assertEqual("""
# import random
# if naam == 'Hedy':
#     print('koekoek')""", result)
#
#     def test_repeat_with_indent(self):
#         result = hedy.transpile("""repeat 5 times
#     print 'koekoek'""", 7)
#         self.assertEqual("""
# import random
# for i in range(5):
#     print('koekoek')""",result)
#
#     def test_repeat_nested_in_if(self):
#         result = hedy.transpile("""if kleur is groen
#     repeat 3 times
#         print 'mooi'""", 7)
#         self.assertEqual(result, """import random
# if kleur == 'groen':
#   for i in range(3):
#     print('mooi')""")
#
#     def test_repeat_basic_print(self):
#         result = hedy.transpile("repeat 5 times print 'me wants a cookie'", 7)
#         self.assertEqual(result, """import random
# for i in range(5):
#   print('me wants a cookie')""")
#         self.assertEqual(run_code(result),'me wants a cookie!\nme wants a cookie!\nme wants a cookie!\nme wants a cookie!\nme wants a cookie!')
#




if __name__ == '__main__':
    unittest.main()



    # python = transpile(tree)
    # print(python)
    #
    # exec(python)
