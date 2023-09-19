import ROOT



if __name__ == '__main__':


    # Open the input file
    inputFileLocation = "/gpfs/mnt/atlasgpfs01/usatlas/data/gdamen/FCC/CLICPerformance/Hinv_studies/reconstruction/hinvee_runs/final/hinvee_380GeV.root"
    input_file = ROOT.TFile.Open(inputFileLocation, "READ")

    event_collection = input_file.Get("events")


    event_collection.GetListOfBranches()

    print( "Available branches >>>>>>>>")
    for branch in event_collection.GetListOfBranches(): print(branch.GetName())
    print( "<<<<<<<< Available branches ")


    num_events = event_collection.GetEntries()

    #import pdb; pdb.set_trace() # import the debugger and instruct it to stop here

    #"TightSelectedPandoraPFOs"

    #event_collection = event.getCollection("MyTrackCollection")


    for entry in event_collection:


        MCParticles = entry.MCParticles # this is a C++ vector, one can index it



        for index, particle in enumerate(MCParticles): 
            print( index, particle.PDG, particle.mass)

        #for x in entry.TightSelectedPandoraPFOs: x.type



        import pdb; pdb.set_trace() # import the debugger and instruct it to stop here


    ## Loop over the events
    #for event_index in range(num_events):
    #    # Get the event object
    #    #event = event_collection[event_index]
    #    AAA = event_collection.GetEntry(event_index)






        import pdb; pdb.set_trace() # import the debugger and instruct it to stop here
