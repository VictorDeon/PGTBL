function startHelp() {
    introJs().setOption(
        {'nextLabel': '>'},
        {'prevLabel': '<'},
        {'skipLabel': 'X'},
        {'doneLabel': 'OK'}
    ).start()
}