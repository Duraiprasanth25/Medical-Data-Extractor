import re
from backend.src.parser_generic import MedicalDocParser

class PatientDetailsParser(MedicalDocParser):
    def __init__(self, text):
        MedicalDocParser.__init__(self,text)

    def parse(self):
        return{
            'patient_name': self.get_patient_name(),
            'phone_number': self.get_phone_number(),
            'medical_problems': self.get_medical_problems(),
            'hepatitis_b_vaccination': self.get_hepatitis_b_vaccination()
        }

    # def get_field(self, field_name):
    #     pattern_dict = {
    #         "patient_name": {"pattern": "Date\n+([a-zA-A]+\s+[a-zA-A]+).\D{3}"},
    #         "phone_number": {"pattern": "(\(\d{3}\) \d{3}-\d{4}).+Weight"},
    #         "medical_problems": {"pattern": "headaches\):n+(D+?)\n"},
    #         "hepatitis_b_vaccination": {"pattern": "vaccination\?\n+(Yes|No)"}
    #     }

    def get_patient_name(self):
        pattern = r'Patient Information(.*?)\(\d{3}\)'
        matches = re.findall(pattern,self.text, flags=re.DOTALL)
        name = ''
        if matches:
            name = self.remove_noise_from_name(matches[0])
        return name

    def get_phone_number(self):
        pattern = 'Patient Information(.*?)(\(\d{3}\) \d{3}-\d{4})'
        matches = re.findall(pattern, self.text, flags=re.DOTALL)
        if matches:
            return matches[0][-1]
        else:
            return None
    def remove_noise_from_name(self,name):
        name = name.replace("Birth Date", "").strip()
        date_pattern = '((Jan|Feb|March|April|May|June|July|Aug|Sep|Oct|Nov|Dec)[ \d]+)'
        date_matches = re.findall(date_pattern, name)
        if date_matches:
           date = date_matches[0][0]
           name = name.replace(date, '').strip()
        return name

    def get_medical_problems(self):
        pattern = 'List any Medical Problems .*?:(.*)'
        matches = re.findall(pattern, self.text, flags=re.DOTALL)
        if matches:
            return matches[0].strip()

    def get_hepatitis_b_vaccination(self):
        pattern = r'Have you had the Hepatitis B vaccination\?.*(Yes|No)'
        matches = re.findall(pattern, self.text, flags=re.DOTALL)
        if matches:
            return matches[0].strip()


if __name__ == '__main__':
    text_1 = '''
    17/12/2020

    Patient Medical Record

    Patient Information Birth Date
    Kathy Crawford May 6 1972
    (737) 988-0851 Weight’
    9264 Ash Dr 95
    New York City, 10005 ,
    United States Height:
    190
    In Casc of Emergency
    oe _
    Simeone Crawford 9266 Ash Dr
    New York City, New York, 10005
    Home phone United States
    (990) 375-4621
    Work phone

    Genera! Medical History

    cece

    — se en ee

    eee een a

    Chicken Pox (Varicella): Measles:

    IMMUNE IMMUNE

    Have you had the Hepatitis B vaccination?

    No

    List any Medical Problems (asthma, seizures, headaches):

    Migraine

    '''

    text_2= '''
    17/12/2020

    Patient Medical Record

    Patient Information Birth Date
    Jerry Lucas May 2 1998
    (279) 920-8204 " Weight:
    4218 Wheeler Ridge Dr $7
    anaes 14201 Height:

    In Case of Emergency
    meee

    Joe Lucas 4218 Wheeler Ridge Dr
    Buffalo, New York, 14201
    Home phone United States
    Work phone

    General Medical History

    Chicken Pox (Varicelia): Measles:

    IMMUNE NOT IMMUNE
    Have you had the Hepatitis B vaccination?
    Yes ,

    List any Medical Problems (asthma, seizures, headaches):
    N/A

    '''


    

    pdp_1 = PatientDetailsParser(text_1)
    pdp_2 = PatientDetailsParser(text_2)


    print(pdp_1.parse())
    print(pdp_2.parse())






