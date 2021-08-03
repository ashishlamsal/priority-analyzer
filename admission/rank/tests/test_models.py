from django.test import TestCase
from rank.models import Program, College, CollegeProgram, Addmission


class ProgramTest(TestCase):
    """ Test module for Program model """

    def setUp(self):
        Program.objects.create(code='BCT', name='Computer Engineering')
        Program.objects.create(code='BCE', name='Civil Engineering')

    def test_program_str_(self):
        bct = Program.objects.get(code='BCT')
        self.assertEqual(bct.__str__(), "Computer Engineering (BCT)")

    def test_program_name(self):
        bce = Program.objects.get(code='BCE')
        self.assertEqual(bce.name, "Civil Engineering")


class CollegeTest(TestCase):
    """ Test module for College model """

    def setUp(self):
        College.objects.create(code='PUL', name='Pulchowk Campus')
        College.objects.create(code='PAS', name='Paschimanchal Campus')

    def test_program_str_(self):
        college = College.objects.get(code='PUL')
        self.assertEqual(college.__str__(), "Pulchowk Campus (PUL)")

    def test_program_name(self):
        college = College.objects.get(code='PAS')
        self.assertEqual(college.name, "Paschimanchal Campus")


class CollegeProgramTest(TestCase):
    """ Test module for CollegeProgram model """

    def setUp(self):
        p1 = Program.objects.create(code='BCT', name='Computer Engineering')
        p2 = Program.objects.create(code='BCE', name='Civil Engineering')
        c1 = College.objects.create(code='PUL', name='Pulchowk Campus')
        c2 = College.objects.create(code='PAS', name='Paschimanchal Campus')

        CollegeProgram.objects.create(
            college=c1, program=p1, seats=12, cutin=150, cutoff=568, type='R')
        CollegeProgram.objects.create(
            college=c2, program=p2, seats=24, cutin=351, cutoff=814, type='F')
        CollegeProgram.objects.create(
            college=c2, program=p2, seats=24, cutin=490, cutoff=239, type='R')

    def test_program_str_(self):
        college = College.objects.get(code='PUL')
        program = Program.objects.get(code='BCT')
        cp = CollegeProgram.objects.get(
            college=college, program=program, type='R')
        self.assertEqual(cp.__str__(), "PUL|BCT|R (seat=12 | range=150-568)")
        self.assertNotEqual(
            cp.__str__(), "PUL|BCT|F (seat=12 | range=150-568)")

    def test_valid_range(self):
        college = College.objects.get(code='PAS')
        program = Program.objects.get(code='BCE')
        cp = CollegeProgram.objects.get(
            college=college, program=program, type='F')
        self.assertTrue(cp.is_valid_range())

    def test_invalid_range(self):
        college = College.objects.get(code='PAS')
        program = Program.objects.get(code='BCE')
        cp = CollegeProgram.objects.get(
            college=college, program=program, type='R')
        self.assertFalse(cp.is_valid_range())


class AddmissionTest(TestCase):
    """ Test module for Addmission model """

    def setUp(self):
        p1 = Program.objects.create(code='BCT', name='Computer Engineering')
        p2 = Program.objects.create(code='BCE', name='Civil Engineering')
        c1 = College.objects.create(code='PUL', name='Pulchowk Campus')
        c2 = College.objects.create(code='PAS', name='Paschimanchal Campus')

        cp1 = CollegeProgram.objects.create(
            college=c1, program=p2, seats=12, cutin=1, cutoff=200, type='R')
        cp2 = CollegeProgram.objects.create(
            college=c2, program=p1, seats=24, cutin=351, cutoff=814, type='F')

        Addmission.objects.create(
            first_name='Suman',
            middle_name='',
            last_name='Tamang',
            gender='M',
            batch='2077',
            collegeprogram=cp1,
            quota='NOR',
            score=131.2,
            rank=1
        )

        Addmission.objects.create(
            first_name='Subarna',
            middle_name='',
            last_name='Regmi',
            gender='M',
            batch='2077',
            collegeprogram=cp2,
            quota='NOR',
            score=104.6,
            rank=400
        )

    def test_program_str_(self):
        student1 = Addmission.objects.get(rank=1)
        student2 = Addmission.objects.get(rank=400)
        self.assertEqual(student1.__str__(),
                         "[1] Suman  Tamang | PUL | Civil Engineering | 2077")
        self.assertEqual(
            student2.__str__(), "[400] Subarna  Regmi | PAS | Computer Engineering | 2077")
        self.assertNotEqual(
            student1.__str__(), "[400] Subarna  Regmi | PAS | Computer Engineering | 2077")
