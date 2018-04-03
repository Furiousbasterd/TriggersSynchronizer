# TriggersSynchronizer
Simple script to synchronize triggers on a new timeline

# Basically how it works
Provided with a trigger and an artifact file, this script will reconstitute a timeline by adding up any bits of time
delimited by the artifacts boundaries. While the timeline is calculated, any triggers contained in an artifact boundaries
is keeped. A new "Time(s)" value is allocated to that trigger, synchronizing it with the new continuous timeline.

# what's necessary
Pandas library, and files must use the Microsoft Excel filename extension. This script only uses the excel reader for now.
Files must have at least these columns:
  - artifacts:
    - Startkeep(s)
    - Endkeep(s)
  - triggers:
    - Time(s)
    - Event (only if you want to keep an eye on wich trigger is wich)

# How to use
For now, you only have to add the path to your files and provide a path for the export. All methods names should
be clear on what they does. If not, the main method is already written to synchronize file. Just c/p path to 
your files in those variables:
  - a : path to artifacts file
  - t : path to triggers file
  - o : path to your output file (must end with a name for your file such as /my/path/output.xlsx)

# What it will give to you
Provided you choose to export the results, an excel document will be generated.
It will contain 3 sheets:
  - synchronized : the keeped triggers synchronized on the new continuous timeline
  - keeped : the keeped triggers with the original artifacts boundaries in which it is contained and its original "Time(s)"
  - rejected : the triggers that were not contained in any of the artifacts boundaries.

# If something seems fishy with the result
Give a try to the coverage function to see if every triggers are tested (keeped + rejected should give you 100%).
Maybe I forgot something in my code, then let me know it by letting an issue ticket here.
