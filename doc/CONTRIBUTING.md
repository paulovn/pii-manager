# Adding anonymization tasks

To add a new anonymization task to the package:

 1. If the task is a new one, add an identifier for it in [TaskEnum]
 2. If it is for a language not yet covered, add a new language subfolder
    undder the [lang] folder, using the [ISO 639-1] code for the language
 3. Then
    * If it is a country-independent PII, it goes into the `any` subdir 
	  (create that dieectory if it is not present)
    * if it is country-dependent, create a country subdir if not present, 
	  using a **lowercased version** of its [ISO 3166-1] country code
 4. Under the final chosen subfolder, add the task as a Python `taskname.py`
    module (the name of the file is not relevant). The module must contain:
	* The task implementation, which can have any of two flavours (regex or
	  function), see below
    * The task descriptor, a list with the (compulsory) name
      `ANONTASKS` (see below)
 5. Finally, add a unit test to check the validity for the task code, in the
    proper place under [test/unit/lang]. There should be at least a positive
	and a negative test

## Task implementation

A task can be implemented with either of two shapes:
 1. A RegEx string that matches a PII on the documents (it will be used to 
   perform a `re.sub` operation). Note that it must be present as the 
   *pattern* string, not the compiled regex (it will be automatically compiled
   by the main code when loading).
 2. A callable, for the cases that more sophisticated matching is neeeded. The
    callable will be called with a string argument, and it must return an 
    *iterable* of PII substrings matched inside the string. So its signature
    will be:
   
         task_executor(doc: str) -> Iterable[str]:
   
   
   
## Task descriptor

The task descriptor is a Python list that contains at least one tuple defining
the entry points for this task (there might be more than one, if the file
implements more than one PII).

* The name of the list **must be** `ANONTASKS`

* Each defined task must be a 4-element tuple, with these elements:
   - the PII identifier for the task: a member of [TaskEnum]
   - a function to be called for initialization of the task, if needed (use
     `None` if not needed). Task initializers must be able to accept
	 arbitrary keyword arguments (unused yet), i.e. its signature will be as:
	 
	     task_init(**kwargs)

   - the [task implementation]: either a Regex raw string or a function
   - a text description of the task (for documentation purposes)

 


[task implementation]: #task-implementation
[TaskEnum]: ../src/text_anonymizer/tasks.py
[lang]: ../src/text_anonymizer/lang
[test/unit/lang]: ../test/unit/lang
[ISO 639-1]: https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes
[ISO 3166-1]: https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2
