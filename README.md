**Description**

	Search a file for patterns and perform different operations
**Give permissions**

	- chmod 755 search.py

**Command Examples**

	- ./search.py -p \@+\[a-z]+\. --mask \* --out out.txt  test.txt


**Usage**

	search.py [-h] [--pattern PATTERN] [--list] [--list-lines] [--number] [--count] [--delete-lines] [--replace REPLACE]
                 [--mask MASK] [--out OUT]
                 file

	Search a file for patterns and perform different operations

	positional arguments:
  		file                  input file

	optional arguments:
  	-h, --help            show this help message and exit
  	--pattern PATTERN, -p PATTERN
                        regular expression to match file content to
  	--list, -l            list matches in the file
  	--list-lines          print lines that contain matches
  	--number              Also print line numbers before matches
  	--count, -c           only count matches in the file
  	--delete-lines        delete line that contains matches in the file
  	--replace REPLACE, -r REPLACE
                        string to replace matches with
  	--mask MASK           a charachter to mask matches with
  	--out OUT, -o OUT     output file to write changes to instead of applying them to input file

