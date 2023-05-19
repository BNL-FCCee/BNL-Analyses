import ROOT



if __name__ == '__main__':


    # Open the input file
    input_file = ROOT.TFile.Open("most_recent_ScottSamples/hinvjj_500.root", "READ")

    event_collection = input_file.Get("events")

    num_events = event_collection.GetEntries()

    #"TightSelectedPandoraPFOs"

    #event_collection = event.getCollection("MyTrackCollection")


    for entry in event_collection:

        for x in entry.TightSelectedPandoraPFOs: x.type

        import pdb; pdb.set_trace() # import the debugger and instruct it to stop here


    # Loop over the events
    for event_index in range(num_events):
        # Get the event object
        #event = event_collection[event_index]

        AAA = event_collection.GetEntry(event_index)






        import pdb; pdb.set_trace() # import the debugger and instruct it to stop here
