#! /bin/bash

#add *.py files
find . -name '*.py' -not -path './.git/*' -exec git add {} \;

#add *.json files
find . -name '*.json' -not -path './.git/*' -exec git add {} \;

#add *.xls files
find . -name '*.xls' -not -path './.git/*' -exec git add {} \;

#add *.xlsx files
find . -name '*.xlsx' -not -path './.git/*' -exec git add {} \;

#add *.md files
find . -name '*.md' -not -path './.git/*' -exec git add {} \;

#add *.sh files
find . -name '*.sh' -not -path './.git/*' -exec git add {} \;

#add .gitignore 
git add .gitignore
