from uuid import uuid4

# generate referral code
def generate_ref_code():
  ref_code = str(uuid4()).replace('-', '')[:12]
  return ref_code

# choices for Quiz difficulty level
DIFF_CHOICES = (
    ('Easy', 'Easy'),
    ('Medium', 'Medium'),
    ('Hard', 'Hard'),
)

# choices for selecting standard
stdchoice = (
    ('0', '0'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
    ('6', '6'),
    ('7', '7'),
    ('8', '8'),
    ('9', '9'),
    ('10', '10'),
    ('11', '11'),
    ('12', '12'), 
    ('CET', 'CET'), 
    ('JEE', 'JEE'), 
    ('NEET', 'NEET'),
    ('Navodaya Vidyalaya', 'Navodaya Vidyalaya') ,
    ('12 COMBO', '12COMBO'),
)

