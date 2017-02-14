import sys, getopt
import datetime
from dateutil.parser import parse
from datetime import timedelta


def setTarget(arg = None):
   if arg == None:
      today = datetime.date.today()
   else:
      today = datetime.date(int(arg[:4]),int(arg[4:]),1)
   delta = timedelta(days = 31)
   target = today + delta

   return str(target.year) + str(target.month)


def validate(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y%m')
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYYMM")


def takeInput(argv):

   target = setTarget()
   
   try:
      opts, args = getopt.getopt(argv,"t:",["target="])
   except getopt.GetoptError:
      print 'pyArgs.py -t <yyyymm>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'pyArgs.py -t <yyyymm>'
         sys.exit()
      elif opt in ("-t", "--target"):
         validate(arg)
         target = setTarget(arg)
         # print parse(arg)
      else:
         print 'invalid input'

   print 'Target is ', target
   return target


def main(argv):

   target = takeInput(argv)
   
   os.chdir('/san-data/usecase/atlasid/new_data/output_file/')

if __name__ == "__main__":
   main(sys.argv[1:])