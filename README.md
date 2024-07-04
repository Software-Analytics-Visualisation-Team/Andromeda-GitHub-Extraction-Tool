# Extraction-Tool

## Description

The extraction tool takes as an input a Github URL and it returns a zip file that contains the repository provided, but the only files are of type *supported languages* (cpp and java).

## Set up:
1. Setup a local Galaxy instance.
2. Go to the directory `galaxy/tools/moonshot/` and clone this repository. (Create the moonshot directory if it doesn't exist yet)
3. Change the galaxy tool configuration at `galaxy/config/tool_conf.xml.sample` by adding:
   ```
   <section name="Moonshot" id="moonshot">
     <tool file="moonshot/Extraction-Tool/github_extraction.xml" />
   </section>
   ```
   
## How to use the tool:
1. Build and run Galaxy as normal.
2. Navigate on the left `Tools column > Moonshot > Extraction-Tool`.
3. Input a URL of a public GitHub repository.
4. Click on "Run Tool" button.

## How to run unit tests
Run the command: 
```
python -m unittest discover -s tests
```
Add `-v` flag at the end for more detailed testing <br/>
Depending on how your python environment is set up the command can also be:
```
python3 -m unittest discover -s tests
```

## Limitations

For now we did not find a good way of checking for the version support of the programming languages.
The only way we found so far was to run the files with the respective version of the programming language and check for errors, but this has the following problems:
- may be useless since we do not need versions to find metrics such LOC, CC, DIT and so on.
- may be useless since we do not need specific versions to find class, methods and variable names and inheritance between classes
- a lot of run-time overhead
- files that are executed have an unpredictable behaviour in the sense that they may create/delete other files, may depend on other files that our tool ignores etc. and it is impossible to deal with all the possible outcomes outside of such a file
- prone to attacks: if an attacker knows someone will use Moonshot to check their code, they can implement any attack hidden in a github repository knowing that their code will be ran if it is a java, C#, python or C++ file.

## Possible solution

Another possible solution of finding these versions would be reading the text in the files and checking for keywords that do not belong in that version of the programming language. According to our findings, we have the following:
- *Java 11* has the following keyword list that it does not support: switch
- *C++ 23* has the following keyword list that it does not support: -
- *Python 3.8* has the following keyword list that it does not support: async, await
- *C# 12* has the following keyword list that it does not support: -
A quick check for python files can be done this way, but, for previously mentioned reasons, it can still prove to be useless

## Dependencies

- git
