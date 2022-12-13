#!/usr/bin/python3
import argparse
import sys
import os
import re
# --pattern,--replace,--mask: special charachters must be given \> as parameters, expr like \w must be given \\w 
# in expr  to read literal *,\\* must be given as arg 
#PRIORITY ORDER: delete-lines,replace,mask,list-lines,list,count

def find_match(file,regex,cflag=False,nflag=False,lflag=False):

	with open(file,'r') as input:
		if not nflag:
			if not lflag:
				only_match(input,regex,cflag)
			else:
				only_line(input,regex)
		else:
			with_line(input,regex,lflag) # use function for match/line if want to display with numbers

def only_match(input,regex,only_count):
	
	content=input.read()
	matches=re.findall(r'{}'.format(regex),content,re.IGNORECASE)
	total=len(matches)
	matches="\n".join(i for i in matches)
	print(matches) if not only_count else print('{} matches found on file'.format(total))

def only_line(input,regex):
	lines=input.readlines()
	for line in lines:
		
		match=re.search(r'{}'.format(regex),line,re.IGNORECASE)
		if match:
			print(line[:-1])

def with_line(input,regex,print_lines):
	
	lines=input.readlines()
	for count,line in enumerate(lines):
		matches=re.findall(r'{}'.format(regex),line,re.IGNORECASE)
			
		if matches: # arr of matches on the same line(count)
			display="".join("\n{} {}".format(count+1,match) for match in matches) if not print_lines else "{} {}".format(count+1,line)
			print(display,end='')
	if not print_lines: print("\n") 


def delete(file,regex,of):
	overwrite=''

	with open(file,'r+') as input:
		lines=input.readlines()
		for line in lines:
			match=re.search(r'{}'.format(regex),line,re.IGNORECASE)
			if not match:
				overwrite=overwrite+line # append lines with no matches

		if not of:
			trunc(input,overwrite) #write data without matches  and remove old
		else:
			write(of,overwrite)

def replace_match(file,regex,replacement,of,mask=False):
	with open(file,'r+') as input:

		lines=input.readlines()
		for count,line in enumerate(lines):
			match=re.findall(r'{}'.format(regex),line,re.IGNORECASE) 

			if match:
				if not mask: 
					lines=replace_regex(input,count,lines,match,replacement) #replace matches of specific line
				else:
					lines=replace_mask(input,count,lines,match,replacement) # mask matches of specific line
		
		if not of:
			trunc(input,lines) # write  changes to input file,delete old changes
		else:
			write(of,lines) # write changes to output file
		
def write(f,new_data):
	with open(f,'w') as output:
		output.writelines(new_data) if type(new_data) is not str  else output.write(new_data) # content as string or arr of lines

def trunc(input,new_data):
	
	data=input.read()
	input.seek(0)
	input.writelines(new_data) if type(new_data) is not str  else input.write(new_data) # content as string or arr of lines
	input.truncate() # truncate the old data

def replace_regex(f,number,flines,matches,repl): #replace matches of specific line

	for match in matches:
		flines[number]=flines[number].replace(match,repl)
	return flines

def replace_mask(f,number,flines,matches,repl):
 
	for mindex,_ in enumerate(matches):

		mchars=re.findall(r'[A-Za-z0-9$&+,:;=?@#<>.-^*()%!]',matches[mindex]) # arr of all chars of a match
		
		for index,_ in enumerate(mchars): # replace each char of match with mask char
			
			if mchars[index]!=' ':
				mchars[index]=repl

		s="".join(i for i in mchars)
		flines[number]=flines[number].replace(matches[mindex],s)

	return flines




parser = argparse.ArgumentParser (description ='Search a file for patterns and perform different operations')
parser.add_argument('--pattern','-p',metavar='PATTERN',type=str,nargs=1,help='regular expression to match file content to')
parser.add_argument('--list','-l',help='list matches in the file',action='store_true')
parser.add_argument('--list-lines',help='print lines that contain matches',action='store_true')
parser.add_argument('--number',help='Also print line numbers before matches',action='store_true')
parser.add_argument('--count','-c',help='only count matches in the file',action='store_true')
parser.add_argument('--delete-lines',help='delete line that contains matches in the file',action='store_true')
parser.add_argument('--replace','-r',metavar='REPLACE',type=str,nargs=1,help='string to replace matches with')
parser.add_argument('--mask',metavar='MASK',type=str,nargs=1,help='a charachter to mask matches with')
parser.add_argument('--out','-o',metavar='OUT',type=str,nargs=1,help='output file to write changes to instead of applying them to input file')

parser.add_argument('file',metavar='file',type=str,nargs=1,help='input file') 
args=parser.parse_args()



ifile=args.file[0] # input file with extension
ofile=args.out[0] if args.out else None 
pattern=args.pattern[0] if args.pattern else None 

if os.path.exists(ifile):
	if pattern:

		if args.delete_lines:
			delete(ifile,pattern,ofile)
		elif args.replace:
			replace=args.replace[0]
			replace_match(ifile,pattern,replace,ofile) 
		elif args.mask:
			replace=args.mask[0]
			if len(replace)==1:
				replace_match(ifile,pattern,replace,ofile,True)
			else:
				print('Error: mask arg must be a single charachter')
				exit
		elif args.list_lines:
			find_match(ifile,pattern,nflag=args.number,lflag=args.list_lines)
		elif args.list:
			find_match(ifile,pattern,nflag=args.number)
		elif args.count:
			find_match(ifile,pattern,cflag=args.count)
	else:
		print('Error: A pattern must be given in order to proceed with execution')
else:
	print('Error: Given input fileile does not exist')

