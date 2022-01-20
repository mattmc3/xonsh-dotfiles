def xbench():
    """Benchmark xonsh by running it 10 times"""
    for i in range(10):
        /usr/bin/time xonsh -c "exit" > /dev/null
