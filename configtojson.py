import sys, tempfile, os, argparse

parser = argparse.ArgumentParser()

parser.add_argument("-i", "--Input", help = "Input file", required = False)

args = parser.parse_args()

if args.Input:
  try:
    in_file = open(args.Input,"r")
  except:
    # error opening input file, complain
    print("Unable to open input file given")
    exit(2)
else:
  in_file = sys.stdin

temp=tempfile.NamedTemporaryFile(mode='w')
  
sub_section=False
first_line=" "
first_section=" "
outfile=[]

outfile.append('{')

# read all input lines
for input_line in in_file:
  # strip leading/trailing whitespaces, and ignore lines that are comments
  input_line=input_line.strip()
  if (input_line[0:1] == "#"):
    pass
  else:
    # if input line not a section split line at equals and print json
    # put a comma at the start if not first line in section
    if (input_line.find('[') == -1):
      if (input_line.find('=') > -1):
        outfile.append("%s   \"%s\": \"%s\"" % (first_line,
                                       input_line[0:input_line.find('=')-1],
                                       input_line[input_line.find('=')+1:len(input_line)].strip()))
      # set up comma for subsequent lines in section
      if (first_line == " "):
        first_line=","
    else:
      # if section already started, close it off
      if (sub_section == True):
        outfile.append('  }')
  
      # format new object for the section
      outfile.append("%s \"%s\" : {" % (first_section, input_line[input_line.find('[')+1:input_line.find(']')]))
      sub_section=True
      first_line=" "
      first_section=","

# if file finished in a section close it off
if (sub_section == True):
  outfile.append('  }')
outfile.append('}')

for l in outfile:
  temp.write(l)

temp.seek(0)

os.system("cat %s|jq ." % (temp.name))
